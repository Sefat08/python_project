import os
import re
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from docx import Document
from docx.document import Document as DocxDocument
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph
from docx.oxml.text.paragraph import CT_P
from docx.oxml.table import CT_Tbl
from openai import OpenAI


# ============================================================
# 1. Project paths
# ============================================================

PROJECT_DIR = Path(__file__).parent

INPUT_DIR = PROJECT_DIR / "input"
OUTPUT_DIR = PROJECT_DIR / "output"

# GitHub-style output structure
DOCS_DIR = PROJECT_DIR / "docs"
IMAGES_DIR = DOCS_DIR / "images"

SOURCE_DOCX = INPUT_DIR / "source.docx"
TEMPLATE_MD = INPUT_DIR / "template.md"

# Final GitHub Markdown output
FINAL_MD = DOCS_DIR / "final.md"

# Debug/intermediate outputs
EXTRACTED_MD = OUTPUT_DIR / "extracted_source.md"
MAPPING_JSON = OUTPUT_DIR / "section_mapping.json"

OUTPUT_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)


# ============================================================
# 2. OpenAI setup
# ============================================================

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.2")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing. Please add it to your .env file.")

client = OpenAI(api_key=OPENAI_API_KEY)


# ============================================================
# 3. OpenAI helper
# ============================================================

def call_openai_text(instructions: str, user_input: str, max_retries: int = 3) -> str:
    for attempt in range(1, max_retries + 1):
        try:
            response = client.responses.create(
                model=OPENAI_MODEL,
                instructions=instructions,
                input=user_input,
            )
            return response.output_text
        except Exception as e:
            print(f"OpenAI API error on attempt {attempt}: {e}")
            if attempt == max_retries:
                raise
            print("Waiting 5 seconds before retrying...")
            time.sleep(5)

    raise RuntimeError("OpenAI call failed unexpectedly.")


def extract_json_from_text(text: str):
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    array_match = re.search(r"\[.*\]", text, re.DOTALL)
    if array_match:
        return json.loads(array_match.group(0))

    object_match = re.search(r"\{.*\}", text, re.DOTALL)
    if object_match:
        return json.loads(object_match.group(0))

    raise ValueError(f"Could not parse JSON from model output:\n{text}")


# ============================================================
# 4. DOCX extraction in original order
# ============================================================

def iter_block_items(parent):
    """
    Yield paragraphs and tables in the same order as they appear in the DOCX.
    """

    if isinstance(parent, DocxDocument):
        parent_element = parent.element.body
    elif isinstance(parent, _Cell):
        parent_element = parent._tc
    else:
        raise ValueError("Unsupported parent type")

    for child in parent_element.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def get_heading_level(style_name: str) -> Optional[int]:
    match = re.search(r"Heading\s+(\d+)", style_name or "", re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None


def clean_cell_text(text: str) -> str:
    text = text.replace("\n", "<br>")
    text = text.replace("|", "\\|")
    return text.strip()


def table_to_markdown(table: Table) -> str:
    rows = []

    for row in table.rows:
        cells = [clean_cell_text(cell.text) for cell in row.cells]
        rows.append(cells)

    if not rows:
        return ""

    max_cols = max(len(row) for row in rows)

    normalized_rows = []
    for row in rows:
        normalized_rows.append(row + [""] * (max_cols - len(row)))

    header = normalized_rows[0]
    separator = ["---"] * max_cols
    body = normalized_rows[1:]

    md_lines = []
    md_lines.append("| " + " | ".join(header) + " |")
    md_lines.append("| " + " | ".join(separator) + " |")

    for row in body:
        md_lines.append("| " + " | ".join(row) + " |")

    return "\n".join(md_lines)

def clear_images_folder():
    """
    Deletes old extracted images before each new run.
    This prevents old images from staying in docs/images after reruns.
    """
    if not IMAGES_DIR.exists():
        IMAGES_DIR.mkdir(parents=True, exist_ok=True)
        return

    for file in IMAGES_DIR.iterdir():
        if file.is_file():
            file.unlink()


def get_image_extension(content_type: str) -> str:
    """
    Convert image MIME type to a file extension.
    """
    content_type = content_type.lower()

    if "png" in content_type:
        return "png"
    if "jpeg" in content_type or "jpg" in content_type:
        return "jpg"
    if "gif" in content_type:
        return "gif"
    if "bmp" in content_type:
        return "bmp"
    if "tiff" in content_type:
        return "tiff"
    if "webp" in content_type:
        return "webp"

    return "png"


def extract_images_from_paragraph(
    paragraph: Paragraph,
    image_counter: int,
    current_section_id: str,
) -> tuple[list[str], int]:
    """
    Extract images from a Word paragraph.

    Saves images to:
        docs/images/

    Adds Markdown links like:
        ![Figure 1](images/source_001_figure_1.png)

    The path is correct because final.md is saved inside docs/.
    """

    image_markdown_links = []

    # Word stores normal embedded images inside <a:blip> elements.
    drawing_elements = paragraph._element.xpath(".//a:blip")

    for blip in drawing_elements:
        embed_id = blip.get(
            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
        )

        if not embed_id:
            continue

        image_part = paragraph.part.related_parts[embed_id]
        content_type = image_part.content_type
        extension = get_image_extension(content_type)

        image_counter += 1

        image_filename = f"{current_section_id}_figure_{image_counter}.{extension}"
        image_path = IMAGES_DIR / image_filename

        with open(image_path, "wb") as image_file:
            image_file.write(image_part.blob)

        markdown_link = f"![Figure {image_counter}](images/{image_filename})"
        image_markdown_links.append(markdown_link)

    return image_markdown_links, image_counter


def extract_docx_sections(docx_path: Path) -> List[Dict[str, Any]]:
    """
    Extract the DOCX as source sections.

    Important:
    - Keeps original section order.
    - Keeps tables near their original position.
    - Extracts images into docs/images/.
    - Inserts GitHub-compatible Markdown image links into the content.
    - Does not summarize.
    """

    if not docx_path.exists():
        raise FileNotFoundError(f"Word document not found: {docx_path}")

    doc = Document(docx_path)

    sections = []

    current_section = {
        "source_id": "source_000",
        "heading": "Front Matter",
        "level": 1,
        "order": 0,
        "content_parts": []
    }

    section_counter = 0
    block_counter = 0
    image_counter = 0

    for block in iter_block_items(doc):
        block_counter += 1

        if isinstance(block, Paragraph):
            text = block.text.strip()

            style_name = block.style.name if block.style else ""
            heading_level = get_heading_level(style_name)

            # If the paragraph is a Word heading, start a new source section.
            if text and heading_level is not None:
                if current_section["content_parts"]:
                    sections.append(current_section)

                section_counter += 1

                current_section = {
                    "source_id": f"source_{section_counter:03d}",
                    "heading": text,
                    "level": heading_level,
                    "order": block_counter,
                    "content_parts": []
                }

                # Headings normally do not contain images.
                # Continue to avoid adding heading text as body content.
                continue

            # Add normal paragraph text.
            if text:
                current_section["content_parts"].append(text)

            # Extract images from this paragraph and add Markdown links in-place.
            image_links, image_counter = extract_images_from_paragraph(
                paragraph=block,
                image_counter=image_counter,
                current_section_id=current_section["source_id"],
            )

            for image_link in image_links:
                current_section["content_parts"].append(image_link)

        elif isinstance(block, Table):
            table_md = table_to_markdown(block)

            if table_md.strip():
                current_section["content_parts"].append(table_md)

    if current_section["content_parts"]:
        sections.append(current_section)

    for section in sections:
        section["content"] = "\n\n".join(section["content_parts"]).strip()
        del section["content_parts"]

    return sections


def source_sections_to_markdown(sections: List[Dict[str, Any]]) -> str:
    parts = []

    for section in sections:
        level = min(max(section["level"], 1), 6)
        hashes = "#" * level

        parts.append(
            f"{hashes} {section['heading']}\n\n"
            f"<!-- source_id: {section['source_id']} | order: {section['order']} -->\n\n"
            f"{section['content']}"
        )

    return "\n\n---\n\n".join(parts)


# ============================================================
# 5. Template parsing
# ============================================================

def read_template(template_path: Path) -> str:
    if not template_path.exists():
        raise FileNotFoundError(f"Template file not found: {template_path}")
    return template_path.read_text(encoding="utf-8")


def extract_template_title(template: str) -> str:
    for line in template.splitlines():
        if line.startswith("# "):
            return line.strip()
    return "# Architecture & Design Document"


def parse_template_sections(template: str) -> List[Dict[str, Any]]:
    """
    Extract numbered template sections.

    Example:
    ### 1. Document Metadata
    ### 2. Problem Statement
    """

    heading_pattern = re.compile(r"^(#{1,6})\s+(\d+)\.\s+(.+?)\s*$")

    sections = []
    current = None

    for line in template.splitlines():
        match = heading_pattern.match(line)

        if match:
            if current:
                sections.append(current)

            hashes, number, title = match.groups()

            current = {
                "target_id": number,
                "title": title.strip(),
                "level": len(hashes),
                "instructions": []
            }
        else:
            if current:
                current["instructions"].append(line)

    if current:
        sections.append(current)

    for section in sections:
        section["instructions"] = "\n".join(section["instructions"]).strip()

    if not sections:
        raise ValueError(
            "No numbered template sections found. "
            "Your template needs headings like '### 1. Document Metadata'."
        )

    return sections


# ============================================================
# 6. LLM mapping only, no rewriting
# ============================================================

def map_sections_only(
    source_sections: List[Dict[str, Any]],
    template_sections: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """
    The LLM only maps sections.
    It is NOT allowed to rewrite content.
    """

    target_text = "\n".join(
        [
            f"{section['target_id']}. {section['title']}\n"
            f"Instruction: {section['instructions'][:400]}"
            for section in template_sections
        ]
    )

    mappings = []
    batch_size = 15

    for start in range(0, len(source_sections), batch_size):
        batch = source_sections[start:start + batch_size]

        source_preview = []

        for section in batch:
            source_preview.append(
                {
                    "source_id": section["source_id"],
                    "heading": section["heading"],
                    "order": section["order"],
                    "preview": section["content"][:1200],
                }
            )

        instructions = """
You are a mapper, not a writer.

Your job is only to decide whether each original source section matches one of the target template sections.

Return only valid JSON.

Rules:
1. Do not rewrite the content.
2. Do not create new sections.
3. Do not invent information.
4. Do not summarize.
5. If the source section clearly matches a template section, return that target_id.
6. If the source section does not clearly match a template section, return KEEP_AS_IS.
7. Use KEEP_AS_IS often when unsure.
8. The final document must preserve the original source document flow.
9. Use the exact source_id values provided.
"""

        user_input = f"""
TARGET TEMPLATE SECTIONS:
{target_text}

SOURCE SECTIONS:
{json.dumps(source_preview, indent=2)}

Return JSON in this exact format:
[
  {{
    "source_id": "source_001",
    "target_id": "1 or 2 or 3 or KEEP_AS_IS",
    "confidence": "high or medium or low",
    "reason": "short reason"
  }}
]
"""

        print(f"Mapping sections {start + 1} to {start + len(batch)}...")

        output = call_openai_text(instructions, user_input)
        batch_mappings = extract_json_from_text(output)

        mappings.extend(batch_mappings)

    return mappings


# ============================================================
# 7. Build final Markdown in original flow
# ============================================================

def markdown_heading(level: int, title: str) -> str:
    level = min(max(level, 2), 6)
    return f"{'#' * level} {title}"


def build_final_markdown_flow_first(
    template: str,
    template_sections: List[Dict[str, Any]],
    source_sections: List[Dict[str, Any]],
    mappings: List[Dict[str, Any]],
) -> str:
    """
    Build one final Markdown file by merging:
    1. Template section order
    2. Original source document flow

    Final behavior:
    - All template sections appear in template order.
    - Empty template sections appear in their proper template position.
    - Source sections that map to a template are placed under that template section.
    - Source sections that do not map to a template are inserted as their own numbered sections
      at the same point in the original document flow.
    - Final numbering is newly generated: 1, 2, 3, ...
    - Original source content is preserved as extracted.
    """

    title = extract_template_title(template)

    template_sections_ordered = template_sections

    target_by_id = {
        str(section["target_id"]): section
        for section in template_sections_ordered
    }

    template_position_by_id = {
        str(section["target_id"]): index
        for index, section in enumerate(template_sections_ordered)
    }

    mapping_by_source = {
        mapping["source_id"]: mapping
        for mapping in mappings
    }

    # Separate source sections into:
    # 1. matched template content
    # 2. source-only content
    matched_sources_by_template_id = {
        str(section["target_id"]): []
        for section in template_sections_ordered
    }

    source_only_sections = []

    for source in sorted(source_sections, key=lambda x: x["order"]):
        source_id = source["source_id"]

        mapping = mapping_by_source.get(source_id, {})
        target_id = str(mapping.get("target_id", "KEEP_AS_IS")).strip()
        confidence = str(mapping.get("confidence", "low")).strip().lower()

        has_valid_template_match = (
            target_id in target_by_id
            and confidence in ["high", "medium"]
        )

        if has_valid_template_match:
            matched_sources_by_template_id[target_id].append(source)
        else:
            source_only_sections.append(source)

    # For every source-only section, decide where it should be inserted
    # relative to the template sections.
    #
    # Rule:
    # Look at the nearest previous matched source section in the original document.
    # Insert the source-only section after that template section.
    #
    # If there is no previous matched source section, insert before the first template section.
    source_only_by_insert_after_template_index = {}

    last_seen_template_index = -1

    for source in sorted(source_sections, key=lambda x: x["order"]):
        source_id = source["source_id"]

        mapping = mapping_by_source.get(source_id, {})
        target_id = str(mapping.get("target_id", "KEEP_AS_IS")).strip()
        confidence = str(mapping.get("confidence", "low")).strip().lower()

        has_valid_template_match = (
            target_id in target_by_id
            and confidence in ["high", "medium"]
        )

        if has_valid_template_match:
            last_seen_template_index = template_position_by_id[target_id]
        else:
            source_only_by_insert_after_template_index.setdefault(
                last_seen_template_index,
                []
            ).append(source)

    final_parts = []

    final_parts.append(title)
    final_parts.append("")
    final_parts.append(
        "> Migrated from source Word document. Original information flow is preserved. "
        "Images are stored in the `images/` folder and referenced from this Markdown file."
    )
    final_parts.append("")

    chronological_section_number = 1

    def emit_source_only_sections_after(template_index: int):
        nonlocal chronological_section_number

        source_only_list = source_only_by_insert_after_template_index.get(
            template_index,
            []
        )

        for source in sorted(source_only_list, key=lambda x: x["order"]):
            final_parts.append(
                f"## {chronological_section_number}. {source['heading']}"
            )
            final_parts.append("")
            chronological_section_number += 1

            if source["content"]:
                final_parts.append(source["content"])
                final_parts.append("")

    # Source-only sections that appear before any matched template section
    emit_source_only_sections_after(-1)

    # Emit every template section in template order.
    # This guarantees all template sections are present and in order.
    for template_index, template_section in enumerate(template_sections_ordered):
        target_id = str(template_section["target_id"])

        final_parts.append(
            f"## {chronological_section_number}. {template_section['title']}"
        )
        final_parts.append("")
        chronological_section_number += 1

        matched_sources = matched_sources_by_template_id.get(target_id, [])

        # Add original source sections under this template section.
        for source in sorted(matched_sources, key=lambda x: x["order"]):
            final_parts.append(f"### {source['heading']}")
            final_parts.append("")

            if source["content"]:
                final_parts.append(source["content"])
                final_parts.append("")

        # After this template section, insert any source-only sections that appeared
        # after source content belonging to this template section in the original document.
        emit_source_only_sections_after(template_index)

    return "\n".join(final_parts).strip() + "\n"

# ============================================================
# 8. Main
# ============================================================

def main():
    print("Reading template...")
    print("Clearing old extracted images...")
    clear_images_folder()
    template = read_template(TEMPLATE_MD)

    print("Parsing template sections...")
    template_sections = parse_template_sections(template)
    print(f"Found {len(template_sections)} template sections.")

    print("Extracting DOCX in original order...")
    source_sections = extract_docx_sections(SOURCE_DOCX)
    print(f"Extracted {len(source_sections)} source sections.")

    print("Saving extracted source for manual checking...")
    extracted_md = source_sections_to_markdown(source_sections)
    EXTRACTED_MD.write_text(extracted_md, encoding="utf-8")
    print(f"Saved: {EXTRACTED_MD}")

    print("Mapping sections only. No rewriting will be done...")
    mappings = map_sections_only(source_sections, template_sections)

    print("Saving mapping JSON...")
    MAPPING_JSON.write_text(json.dumps(mappings, indent=2), encoding="utf-8")
    print(f"Saved: {MAPPING_JSON}")

    print("Building final Markdown in original source flow...")
    final_md = build_final_markdown_flow_first(
        template=template,
        template_sections=template_sections,
        source_sections=source_sections,
        mappings=mappings,
    )

    FINAL_MD.write_text(final_md, encoding="utf-8")

    print("")
    print("DONE.")
    print(f"Final Markdown created here: {FINAL_MD}")
    print("")


if __name__ == "__main__":
    main()

    