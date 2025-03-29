import dataclasses
import enum

from typing import TypedDict
from selenium import webdriver


class WebElement(TypedDict):
    name: str | None
    xpath: str


class ActionType(enum.Enum):
    CLICK = "click"
    MOVE = "move"
    INPUT = "input"


@dataclasses.dataclass
class SimpleInstruction:
    element: WebElement | None
    timeout: int = 10
    value: str | webdriver.Keys | None = None
