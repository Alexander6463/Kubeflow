import logging
import os
from pathlib import Path
from typing import Optional

from poppler import load_from_file, PageRenderer
from text_extractor import extract_text
from poppler.page import Page

DPI = 120  # DPI for extracting image

logger = logging.getLogger("logger")


class LockDocumentError(Exception):
    ...


def preprocess(
        path_to_file: Path,
        output_img_path: Path,
        output_text_path: Path,
        start: int = 0,
        stop: int = -1,
        owner_password: Optional[str] = None,
        user_password: Optional[str] = None,
) -> None:
    """Check PDF and call extract_image and extract_text for each page"""
    logger.info(
        f"Start doing {path_to_file}, pages "
        + f"{start}-{stop if stop != -1 else 'end'}, "
        + f"output_img_path: {str(output_img_path)}, "
        + f"output_text_path: {str(output_text_path)}, "
        + f"owner_password: {owner_password}, user_password: {user_password}"
    )
    pdf_document = load_from_file(path_to_file, owner_password, user_password)
    if pdf_document.is_locked():
        logger.error(f"PDF {pdf_document.title} is locked")
        raise LockDocumentError("Document is locked")

    os.makedirs(output_img_path, exist_ok=True)
    os.makedirs(output_text_path, exist_ok=True)

    if stop == -1 or stop > pdf_document.pages:
        stop = pdf_document.pages

    renderer = PageRenderer()
    for page_number in range(start, stop):
        logger.info(f"Processing page {page_number}")
        page = pdf_document.create_page(page_number)
        render_image(page, output_img_path, page_number, renderer)
        extract_text(page, output_text_path, page_number)
    logger.info(f"Finish with {path_to_file}")


def render_image(
        page: Page, output_img_path: Path, page_number: int, renderer: PageRenderer
) -> bool:
    """Render page and save it as output_img_path/page_number.png"""
    logger.info("Start extracting image")
    image = renderer.render_page(page, xres=DPI, yres=DPI)
    if not image.is_valid:
        logger.error("Image is invalid")
        return False
    image.save(str(output_img_path) + f"/{page_number}.png", "png", DPI)
    return True
