from __future__ import annotations
from copy import copy
import math
from pathlib import Path
from typing import TYPE_CHECKING

from .source_info import SourcecodeInfo

if TYPE_CHECKING:
    from .Expression import Expression
else:
    class Expression:
        pass

type Point = int | float | bool | str  # primitive types

class Circl(list[Expression]):
    def __repr__(self) -> str:
        as_list = super().__repr__()
        return "Ͼ " + as_list[1:-1] + " Ͽ"

    def __str__(self) -> str:
        return self.__repr__()

    def __getitem__(self, index: int) -> Expression:
        return super().__getitem__(index % len(self))

    def pop(self, index: int = -1) -> Expression:
        return super().pop(index % len(self))

    def insert(self, index: int, obj) -> Expression:
        return super().insert(index % len(self), Expression(obj))
    
    def append(self, object):
        return super().append(Expression(object))
    
    def __copy__(self) -> Circl:
        return Circl([copy(i) for i in self])

    def __init__(self, circls_or_points: list[Expression | Point | Circl] = ()) -> None:
        super().__init__([Expression(i) if not isinstance(i, Expression) else i for i in circls_or_points])
        self.stdout_copy = ""