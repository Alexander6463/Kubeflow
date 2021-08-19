"""Module implement text page extractor"""
import logging
from pathlib import Path
from typing import Optional, List

from poppler.page import Page
from pydantic import BaseModel, Field

logger = logging.getLogger("logger")


class PopplerBoundingBox(BaseModel):
    x: float = Field(alias="left")
    y: float = Field(alias="top")
    height: float
    width: float


class PopplerTextField(BaseModel):
    bbox: PopplerBoundingBox
    text: str


class PopplerPage(BaseModel):
    bbox: PopplerBoundingBox
    page_num: int
    orientation: str
    text_fields: Optional[List[PopplerTextField]] = Field(alias="blocks")


def get_poppler_text_field(text_list: Page.text_list) -> List[PopplerTextField]:
    """Return array of text_fields from page"""
    res = []
    for text in text_list:
        bound = PopplerBoundingBox(
            left=text.bbox.x,
            top=text.bbox.y,
            height=text.bbox.height,
            width=text.bbox.width,
        )
        res.append(PopplerTextField(bbox=bound, text=text.text))
    return res


def extract_text(
    page: Page,
    dir_to_save: Path,
    page_number: int,
) -> None:
    """Save text from page into JSON file"""
    logger.info("Start to extract text")
    page_data = PopplerPage(
        bbox=PopplerBoundingBox(
            left=page.page_rect().x,
            top=page.page_rect().y,
            height=page.page_rect().height,
            width=page.page_rect().width,
        ),
        page_num=page_number,
        orientation=str(page.orientation),
        blocks=[i for i in get_poppler_text_field(page.text_list())],
    )
    with open((dir_to_save / str(page_number)), "w") as file_to_save:
        file_to_save.write(page_data.json(by_alias=True))
