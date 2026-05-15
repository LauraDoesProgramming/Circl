from __future__ import annotations
from enum import Enum, auto
import math
from copy import copy
from typing import TYPE_CHECKING, Any, cast, Callable
from unittest import case
from circl.source_info import SourcecodeInfo

from .circl import Circl

type Point = int | float | bool | str  # primitive types

class ExpressionType(Enum):
    POINT = auto()
    CIRCL = auto()
    OPERATOR = auto()
    UNKNOWN = auto()


class ExpressionIterator:
    def __init__(self, expression: Expression):
        self.expression = expression
        self.index = 0

    def __iter__(self) -> ExpressionIterator:
        return self

    def __next__(self) -> Expression:
        if self.index < len(self.expression.value):
            result = self.expression.value[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration


class Expression:
    def apply_binary_operation(self, other: Expression, operation: Callable[[Expression, Exception], Expression], error_string1: str, error_string2: str) ->  Circl | Point:
        if not isinstance(other, Expression):
            other = Expression(other)
        match self.type:
            case ExpressionType.CIRCL:
                match other.type:
                    case ExpressionType.CIRCL:
                        self.value = cast(Circl, self.value)
                        other.value = cast(Circl, other.value)
                        return Circl([operation(a, b) for (a, b) in zip(self.value, other.value)])
                    case ExpressionType.POINT:
                        self.value = cast(Circl, self.value)
                        other.value = cast(Point, other.value)
                        return Circl([operation(x, other.value) for x in self.value])
                    case ExpressionType.OPERATOR:
                        raise TypeError(f"Cannot {error_string1} operator {other.value} {error_string2} circl {self.value}")
                    case ExpressionType.UNKNOWN:
                        raise TypeError(f"Cannot {error_string1} unknown expression {other.value} {error_string2} circl {self.value}")
            case ExpressionType.POINT:
                match other.type:
                    case ExpressionType.CIRCL: 
                        self.value = cast(Point, self.value)
                        other.value = cast(Circl, other.value)
                        return Circl([operation(self.value, x) for x in other.value])
                    case ExpressionType.POINT:
                        self.value = cast(Point, self.value)
                        other.value = cast(Point, other.value)
                        return operation(self.value, other.value)
                    case ExpressionType.OPERATOR:
                        raise TypeError(f"Cannot {error_string1} operator \"{other.value}\" {error_string2} point {self.value}")
                    case ExpressionType.UNKNOWN:
                        raise TypeError(f"Cannot {error_string1} unknown expression {other.value} {error_string2} point {self.value}")
            case ExpressionType.OPERATOR:
                raise TypeError(f"Cannot {error_string1} anything {error_string2} operator \"{self.value}\"")
            case ExpressionType.UNKNOWN:
                raise TypeError(f"Cannot {error_string1} anything {error_string2} unknown expression {self.value}")
    
    def apply_unary_operation(self, operation: Callable[[Expression, Exception], Expression], error_string: str) -> Circl | Point:
        match self.type:
            case ExpressionType.CIRCL:
                self.value = cast(Circl, self.value)
                return Circl([operation(x) for x in self.value])
            case ExpressionType.POINT:
                self.value = cast(Point, self.value)
                return operation(self.value)
            case ExpressionType.OPERATOR:
                raise TypeError(f"Cannot {error_string} operator \"{self.value}\"")
            case ExpressionType.UNKNOWN:
                raise TypeError(f"Cannot {error_string} unknown expression {self.value}")
                
    def __init__(self, value: Point | Circl | str | Expression, is_operator: bool = False, source_info: SourcecodeInfo | None = None) -> None:
        if isinstance(value, Expression):
            self.type = value.type
            self.value = copy(value.value)
            self.source_info = copy(value.source_info)
            return
        
        self.type: ExpressionType
        match value:
            case Circl():
                self.type = ExpressionType.CIRCL
            case str() if is_operator:
                self.type = ExpressionType.OPERATOR
            case int() | float() | bool() | str():
                self.type = ExpressionType.POINT
            case _:
                self.type = ExpressionType.UNKNOWN
        self.value: Point | Circl | str = value
        self.source_info: SourcecodeInfo | None = source_info
    
    def __copy__(self) -> Expression:
        return Expression(copy(self.value), self.type == ExpressionType.OPERATOR)
    
    def __iter__(self) -> ExpressionIterator:
        match self.type:
            case ExpressionType.CIRCL:
                return ExpressionIterator(self)
            case ExpressionType.POINT if isinstance(self.value, str):
                return ExpressionIterator(self)
            case ExpressionType.POINT:
                raise TypeError(f"Cannot iterate over Point {self.value}")
            case ExpressionType.OPERATOR:
                raise TypeError(f"Cannot iterate over operator \"{self.value}\"")
            case ExpressionType.UNKNOWN:
                raise TypeError(f"Cannot iterate over unknown Expression {self.value}")

    def __repr__(self) -> str:
        match self.type:
            case ExpressionType.CIRCL:
                return f"Expression(Circl({self.value}))"
            case ExpressionType.OPERATOR:
                return f"Expression(Operator({self.value}))"
            case ExpressionType.POINT:
                return f"Expression(Point({self.value}))"
            case ExpressionType.UNKNOWN:
                return f"Expression(_Unknown({self.value}))"
    
    def __add__(self, other: Expression ) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a + b, "add", "to")

    def __iadd__(self, other: Expression) -> Expression:
        self.value = self + other
        return self

    def __sub__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a - b, "subtract", "from")

    def __isub__(self, other: Expression) -> Expression:
        self.value = self - other
        return self
    
    def __mul__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a * b, "multiply", "with")


    def __imul__(self, other: Expression) -> Expression:
        self.value = self * other
        return self
    
    def __mod__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a % b, "modulo", "by")
    
    def __imod__(self, other: Expression) -> Expression:
        self.value = self % other
        return self

    def __truediv__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a / b, "divide", "by")

    def __itruediv__(self, other: Expression) -> Expression:
        self.value = self / other
        return self

    def __floordiv__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a // b, "floor divide", "by")

    def __ifloordiv__(self, other: Expression) -> Expression:
        self.value = self // other
        return self

    def __pow__(self, other: Expression) -> Circl | float:
        return self.apply_binary_operation(other, lambda a, b: a ** b, "raise", "to")

    def __ipow__(self, other: Expression) -> Expression:
        self.value = self**other
        return self

    def __neg__(self) -> Circl | float:
        return self.apply_unary_operation(lambda x: -x, "negate")

    def __abs__(self) -> Circl | float:
        return self.apply_unary_operation(abs, "take absolute value")
    
    def __pos__(self) -> Circl | float:
        return self.apply_unary_operation(lambda x: +x, "apply unary plus to")

    def __round__(self) -> Circl | float:
        return self.apply_unary_operation(round, "round")

    def __floor__(self) -> Circl | float:
        return self.apply_unary_operation(math.floor, "floor")

    def __ceil__(self) -> Circl | float:
        return self.apply_unary_operation(math.ceil, "ceil")
    
    def __bool__(self) -> Circl | bool:
        return self.apply_unary_operation(bool, "convert to boolean")

    def __and__(self, other: Expression) -> Circl | int:
        return self.apply_binary_operation(other, lambda a, b: a & b, "&", "with")
    
    def __iand__(self, other: Expression) -> Expression:
        self.value = self & other
        return self

    def __or__(self, value: Expression) -> Circl | int:
        return self.apply_binary_operation(value, lambda a, b: a | b, "|", "with")
    
    def __ior__(self, value: Expression):
        self.value = self | value
        return self
    
    def __xor__(self, value: Expression) -> Circl | int:
        return self.apply_binary_operation(value, lambda a, b: a ^ b, "^", "with")
    
    def __ixor__(self, value: Expression) -> Expression:
        self.value = self ^ value
        return self
    
    def __invert__(self) -> Circl | Any:
        return self.apply_unary_operation(lambda x: ~x, "invert")
    
    def __lshift__(self, other: Expression) -> Circl | int:
        return self.apply_binary_operation(other, lambda a, b: a << b, "<<", "with")
    
    def __ilshift__(self, other: Expression) -> Expression:
        self.value = self << other
        return self
    
    def __rshift__(self, other: Expression) -> Circl | int:
        return self.apply_binary_operation(other, lambda a, b: a >> b, ">>", "with")
    
    def __irshift__(self, other: Expression) -> Expression:
        self.value = self >> other
        return self
    
    def __int__(self) -> Circl | int:
        return self.apply_unary_operation(int, "convert to int")
    
    def __float__(self) -> Circl | float:
        return self.apply_unary_operation(float, "convert to float")

    def __trunc__(self) -> Circl | float:
        return self.apply_unary_operation(math.trunc, "truncate")

    def __contains__(self, item) -> Circl | bool:
        return self.apply_binary_operation(item, lambda a, b: b in a, "check if", "is in")

    def radius(self) -> float:
        match self.type:
            case ExpressionType.CIRCL:
                return len(cast(Circl, self.value)) / (2 * math.pi)
            case ExpressionType.POINT:
                if isinstance(self.value, str):
                    return len(self.value) / (2 * math.pi)
                elif isinstance(self.value, (int, float)):
                    return self.value / (2 * math.pi)
                elif self.value:
                    return 1 / (2 * math.pi)
                else:
                    return 0
            case ExpressionType.OPERATOR:
                raise TypeError(f"Cannot get radius of operator {self.value}")
            case ExpressionType.UNKNOWN:
                raise TypeError(f"Cannot get radius of unknown expression {self.value}")
        
    

    def get_error_location(self) -> str | None:
        if self.source_info is not None:
            line_info: str
            if self.source_info.from_line == self.source_info.to_line:
                line_info = f"line {self.source_info.from_line}"
            else:
                line_info = f"lines {self.source_info.from_line} to {self.source_info.to_line}"

            position_info: str
            if self.source_info.from_position == self.source_info.to_position:
                position_info = f"at position {self.source_info.from_position}"
            else:
                position_info = f"from {self.source_info.from_position} to {self.source_info.to_position}"

            return f"in {self.source_info.file} on {line_info} {position_info}"
        return None