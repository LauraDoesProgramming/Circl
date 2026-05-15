import math
import random
from copy import copy
from collections.abc import Callable
from typing import Dict, cast
import re

from .Expression import Expression, ExpressionType, Point
from .circl import Circl
from .program import main_program

var_circl = Circl()  # TODO: Please find a better way to do this

class Identifier(Expression):
    def __hash__(self):
        return hash(str(self))

def helper_just_T[T](T: type[T], x: Expression, operation: Callable[[T], Point]) -> Expression:
    match x.type:
        case ExpressionType.POINT if isinstance(x.value, T):
            return Expression(operation(x.value))
        case ExpressionType.POINT:
            raise TypeError(f"Expected {T}, got {type(x.value)}")
        case _ as other:
            raise TypeError(f"Expected Point, got {other}")

def helper_T_circl_or_just_T[T](T: type[T], x: Expression, operation: Callable[[T], Point | Circl]):
    match x.type:
        case ExpressionType.CIRCL:
            result = []
            for i, value in enumerate(x.value):
                if not value.type == ExpressionType.POINT:
                    raise TypeError(f"1st argument at {i}: Expected Point, got {value.type}")
                if not isinstance(value.value, T):
                    raise TypeError(f"1st argument at {i}: Expected {T}, got {type(value.value)}")
                result.append(operation(value))
            return Expression(Circl(result))
        case ExpressionType.POINT if isinstance(x.value, T):
            return Expression(operation(x.value))
        case ExpressionType.POINT:
            raise TypeError(f"1st argument: Expected {T}, got {type(x.value)}")
        case _ as other:
            raise TypeError(f"1st argument: Expected Circl Point, got {other}")

def helper_1st_is_T_circl_or_just_T_2nd_is_T[T](T: type[T], a: Expression, b: Expression, operation: Callable[[T, T], Point | Circl]) -> Expression:
    if not b.type == ExpressionType.POINT:
        raise TypeError(f"2nd argument: Expected Point, got {b.type}")
    if not isinstance(b.value, T):
        raise TypeError(f"2nd argument: Expected {T}, got {type(b.value)}")
    match a.type:
        case ExpressionType.CIRCL:
            result = []
            for i, x in enumerate(a.value):
                if not x.type == ExpressionType.POINT:
                    raise TypeError(f"1st argument at {i}: Expected Point, got {x.type}")
                if not isinstance(b.value, T):
                    raise TypeError(f"1st argument at {i}: Expected {T}, got {type(x.value)}")
                result.append(operation(x.value, b.value))
            return Expression(Circl(result))
        case ExpressionType.POINT if isinstance(a.value, T):
            return Expression(operation(a.value, b.value))
        case ExpressionType.POINT:
            raise TypeError(f"1st argument: Expected {T}, got {type(a.value)}")
        case _ as other:
            raise TypeError(f"1st argument: Expected Circl Point, got {other}")

def c_halt(main_circl: Circl):
    main_circl.clear()

def c_read_input(main_circl: Circl):
    main_circl.append(input())


def c_pi(main_circl: Circl):
    main_circl.append(math.pi)
        


def c_e(main_circl: Circl):
    main_circl.append(math.e)

def c_inf(main_circl: Circl):
    main_circl.append(math.inf)

def c_duplicate(main_circl: Circl):
    main_circl.append(copy(main_circl[-1]))


def c_pop(main_circl: Circl) -> Expression:
    return main_circl.pop()


def c_cycle_back(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    to_operate3 = main_circl.pop()
    main_circl.append(to_operate2)
    main_circl.append(to_operate1)
    main_circl.append(to_operate3)


def c_cycle_forward(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    to_operate3 = main_circl.pop()
    main_circl.append(to_operate1)
    main_circl.append(to_operate3)
    main_circl.append(to_operate2)


def c_swap_last(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1)
    main_circl.append(to_operate2)


def c_move_top(main_circl: Circl):
    main_circl.append(main_circl[helper_just_T(int, main_circl.pop(), lambda x: -x + 1).value])

def c_println(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.stdout_copy += str(to_operate1) + '\n'
    print(to_operate1)


def c_print(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.stdout_copy += str(to_operate1)
    print(to_operate1, end="")

def c_helper_read_file(main_circl: Circl, filename: str) -> None:
    with open(filename, "r") as f:
        main_circl.append(f.read())

def c_read_file(main_circl: Circl):
    main_circl.append(helper_just_T(str, main_circl.pop(), lambda x: c_helper_read_file(main_circl, x) ))

def c_helper_write_file(main_circl: Circl, filename: str, content: Expression) -> None:
    with open(filename, "w") as f:
        f.write(str(content))


def c_write_file(main_circl: Circl):
    filename = main_circl.pop()
    to_operate1 = main_circl.pop()
    helper_just_T(str, filename, lambda x: c_helper_write_file(main_circl, x, to_operate1))


def c_length(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(len(to_operate1))


def c_radius(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(to_operate1.radius())


def c_cast_float(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(float(to_operate1))


def c_cast_int(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(int(to_operate1))



def c_to_precision(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(helper_1st_is_T_circl_or_just_T_2nd_is_T(str, to_operate1, to_operate2, lambda a, b: f"{a:.{b}f}"))


def c_ordinal(main_circl: Circl):
    main_circl.append(helper_T_circl_or_just_T(str, main_circl.pop(), ord))


def c_cast_char(main_circl: Circl):
    main_circl.append(helper_T_circl_or_just_T(int, main_circl.pop(), chr))


def c_rnd(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(random.choice(to_operate1.value))
    else:
        if not isinstance(to_operate1.value, int):
            raise TypeError(f"Expected integer, got {type(to_operate1.value)}")
        if to_operate1.value == 1:
            main_circl.append(random.random())
        else:
            main_circl.append(random.randint(0, to_operate1.value))


def c_logical_not(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(not to_operate1)


def c_logical_and(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1 and to_operate2)

def c_logical_or(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1 or to_operate2)


def c_logical_xor(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1 ^ to_operate2)


def c_left_shift(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 << to_operate1)


def c_right_shift(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 >> to_operate1)


def c_equals(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1 == to_operate2)


def c_not_equals(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate1 != to_operate2)


def c_lower_than(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 < to_operate1)


def c_greater_than(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 > to_operate1)


def c_lower_than_equal(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 <= to_operate1)


def c_greater_than_equal(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 >= to_operate1)


def c_jump_if_true(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1:
        main_program.increment_counter(to_operate2)


def c_jump_if_false(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if not to_operate1:
        main_program.increment_counter(to_operate2)


def c_increment_program_counter_by(main_circl: Circl):
    main_program.increment_counter(helper_just_T(int, main_circl.pop(), lambda x: x).value)



def c_decrement_program_counter_by(main_circl: Circl):
    main_program.decrement_counter(helper_just_T(int, main_circl.pop(), lambda x: x - 1).value)


def c_execute_as_circl(main_circl: Circl, exec_subroutine):
    to_operate1 = main_circl.pop()
    if to_operate1.type != ExpressionType.CIRCL:
        raise TypeError(f"Expected Circl, got {to_operate1.type}")
    exec_subroutine(to_operate1.value)
    main_circl.stdout_copy += to_operate1.stdout_copy

def c_remove_nth_element(main_circl: Circl):
    n = main_circl.pop()
    if not isinstance(n.value, int):
        raise
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        n = n % len(to_operate1)
        main_circl.append(Circl(to_operate1[n:] + to_operate1[:n]))
    else:
        n = n % len(to_operate1) if to_operate1 else 0
        main_circl.append(to_operate1[n:] + to_operate1[:n])


def c_remove_negative_nth_element(main_circl: Circl):
    n = main_circl.pop()
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        items = to_operate1
        n = n % len(items) if items else 0
        main_circl.append(Circl(items[-n:] + items[:-n]) if n else Circl(items))
    else:
        n = n % len(to_operate1) if to_operate1 else 0
        main_circl.append((to_operate1[-n:] + to_operate1[:-n]) if n else to_operate1)


def c_set_index_zero(main_circl: Circl):
    n = main_circl.pop()
    length = len(main_circl)
    n %= length
    items = main_circl
    rotated = items[n:] + items[:n]
    main_circl.clear()
    for item in rotated:
        main_circl.append(item)
    main_program.set_counter((main_program.get_counter() - n) % length - 1)


def c_append_range(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        # TODO: add step argument
        main_circl.append(Circl([x for x in range(to_operate1[0], to_operate1[1])]))
    else:
        main_circl.append(Circl([x for x in range(to_operate1)]))


def c_append_range_circl(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl(Circl(x for x in range(i)) for i in to_operate1))
    else:
        main_circl.append(Circl(x for x in range(to_operate1)))


def c_square(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i**2 for i in to_operate1]))
    else:
        main_circl.append(to_operate1**2)


def c_sqrt(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i**0.5 for i in to_operate1]))
    else:
        main_circl.append(to_operate1**0.5)


def c_pow(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2.value**to_operate1.value)


def c_floor(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(math.floor(to_operate1))


def c_ceil(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(math.ceil(to_operate1))


def c_round(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(round(to_operate1))


# TODO: make this max over both operators
def c_max(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    match to_operate1.type:
        case ExpressionType.CIRCL:
            match to_operate2.type:
                case ExpressionType.CIRCL:
                    main_circl.append(max(max(i.value for i in to_operate1), max(i.value for i in to_operate2)))
                case _:
                    main_circl.append(max(max(i.value for i in to_operate1), to_operate2.value))
        case _:
            match to_operate2.type:
                case ExpressionType.CIRCL:
                    main_circl.append(max(to_operate1.value, max(i.value for i in to_operate2)))
                case _:
                    main_circl.append(max(to_operate1.value, to_operate2.value))


# TODO: make this min over both operators
def c_min(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    match to_operate1.type:
        case ExpressionType.CIRCL:
            match to_operate2.type:
                case ExpressionType.CIRCL:
                    main_circl.append(min(min(i.value for i in to_operate1), min(i.value for i in to_operate2)))
                case _:
                    main_circl.append(min(min(i.value for i in to_operate1), to_operate2.value))
        case _:
            match to_operate2.type:
                case ExpressionType.CIRCL:
                    main_circl.append(min(to_operate1.value, min(i.value for i in to_operate2)))
                case _:
                    main_circl.append(min(to_operate1.value, to_operate2.value))


def c_abs(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(abs(to_operate1))


def c_logn(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([math.log(i) for i in to_operate1]))
    else:
        main_circl.append(math.log(to_operate1))


def c_log10(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([math.log10(i) for i in to_operate1]))
    else:
        main_circl.append(math.log10(to_operate1))


def c_sin(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([math.sin(i) for i in to_operate1]))
    else:
        main_circl.append(math.sin(to_operate1))


def c_cos(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([math.cos(i) for i in to_operate1]))
    else:
        main_circl.append(math.cos(to_operate1))


def c_tan(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([math.tan(i) for i in to_operate1]))
    else:
        main_circl.append(math.tan(to_operate1))


def c_split(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([Circl(list(i)) for i in to_operate1]))
    else:
        main_circl.append(Circl(list(to_operate1)))


def c_slice(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    to_operate3 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl(to_operate1[to_operate3:to_operate2]))
    else:
        main_circl.append(to_operate1[to_operate3:to_operate2])


def c_replace_string(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    to_operate3 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl(
            [
                i.replace(to_operate3.value, to_operate2.value) if type(i) is str else i
                for i in to_operate1
            ]
        ))
    else:
        main_circl.append(to_operate1.replace(to_operate3.value, to_operate2.value))


def c_uppercase(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i.value.upper() for i in to_operate1]))
    else:
        main_circl.append(to_operate1.value.upper())


def c_lowercase(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i.value.lower() for i in to_operate1]))
    else:
        main_circl.append(to_operate1.value.lower())


def c_sum(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(sum(i.value for i in to_operate1))
    else:
        main_circl.append(to_operate1.value)

def c_product(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        result = 1.0
        for i in to_operate1:
            result *= i
        main_circl.append(result)
    else:
        main_circl.append(to_operate1)


def c_contains(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 in to_operate1)


def c_not_contains(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(to_operate2 not in to_operate1)


def c_indexof(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    match to_operate1.type:
        case ExpressionType.CIRCL:
            main_circl.append(
            to_operate1.index(to_operate2)
            )
        case ExpressionType.STRING if isinstance(to_operate1.value, str) and to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, str):
            main_circl.append(to_operate1.value.find(to_operate2.value))
        case _:
            raise TypeError(f"Expected Circl or string, got {to_operate1.type}")



def c_intersection(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i for i in to_operate2.value if i in set(to_operate1)]))
    elif to_operate1.type == ExpressionType.CIRCL:
        main_circl.append("".join(i for i in to_operate2.value if i.value in set(to_operate1.value)))
    elif to_operate2.type == ExpressionType.CIRCL:
        main_circl.append("".join(i for i in to_operate1.value if i.value in set(to_operate2.value)))
    else:
        main_circl.append("".join(i for i in to_operate2.value if i.value in to_operate1.value))


def c_union(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.CIRCL:
        seen = set()
        result = []
        for i in to_operate2.value + to_operate1.value:
            if i not in seen:
                seen.add(i)  # TODO: fix this method.
                result.append(i)
        main_circl.append(Circl(result))
    else:
        seen = set()
        result = []
        for i in (
            to_operate2.value
            if to_operate2.type == ExpressionType.POINT and type(to_operate2.value) is str
            else (
                "".join(to_operate2.value) + to_operate1.value
                if to_operate1.type == ExpressionType.POINT and type(to_operate1.value) is str
                else "".join(to_operate1.value)
            )
        ):
            if i not in seen:
                seen.add(i)
                result.append(i)
        main_circl.append("".join(result))


def c_difference(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.CIRCL:
        main_circl.append(Circl([i for i in to_operate2.value if i not in set(to_operate1.value)]))
    elif to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append("".join(i for i in to_operate2.value if i not in set(to_operate1.value)))
    elif to_operate2.type == ExpressionType.CIRCL and to_operate1.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append(Circl([i for i in to_operate2.value if i != to_operate1.value]))
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1, str) and to_operate2.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append("".join(i for i in to_operate2.value if i not in to_operate1.value))
    else:
        if to_operate1.type == ExpressionType.CIRCL or isinstance(to_operate1.value, str):
            raise TypeError(f"Expected Circl or string, got {to_operate2.type}")
        elif to_operate2.type == ExpressionType.CIRCL or isinstance(to_operate2.value, str):
            raise TypeError(f"Expected Circl or string, got {to_operate1.type}")
        else:
            raise TypeError(f"Expected Circl or string, got {to_operate1.type} and {to_operate2.type}")
        
def c_zip(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.CIRCL:
        main_circl.append(
            Circl([Circl([a, b]) for a, b in zip(to_operate2.value, to_operate1.value)])
        )
    elif to_operate1.type == ExpressionType.CIRCL and to_operate2.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append(
            Circl([Circl([a, b]) for a, b in zip(list(to_operate2.value), to_operate1.value)])
        )
    elif to_operate2.type == ExpressionType.CIRCL and to_operate1.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append(
            Circl([Circl([a, b]) for a, b in zip(to_operate2.value, list(to_operate1.value))])
        )
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1, str) and to_operate2.type == ExpressionType.POINT and isinstance(to_operate1, str):
        main_circl.append(
            Circl([Circl([a, b]) for a, b in zip(list(to_operate2.value), list(to_operate1.value))])
        )
    else: 
        if to_operate1.type == ExpressionType.CIRCL or isinstance(to_operate1.value, str):
            raise TypeError(f"Expected Circl or string, got {to_operate2.type}")
        elif to_operate2.type == ExpressionType.CIRCL or isinstance(to_operate2.value, str):
            raise TypeError(f"Expected Circl or string, got {to_operate1.type}")
        else:
            raise TypeError(f"Expected Circl or string, got {to_operate1.type} and {to_operate2.type}")

def c_stack_size(main_circl: Circl):
    main_circl.append(len(main_circl))


def c_sort(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(
            Circl(sorted(to_operate1.value, key=lambda x: x.value))
        )
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1.value, str):
        main_circl.append("".join(sorted(to_operate1.value)))
    else:
        raise TypeError(f"Expected Circl or string, got {to_operate1.type}")


def c_reverse(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        main_circl.append(Circl(list(reversed(to_operate1.value))))
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1.value, str):
        main_circl.append(to_operate1[::-1])
    else:
        raise TypeError(f"Expected Circl or string, got {to_operate1.type}")


def c_replace(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    to_operate3 = main_circl.pop()
    if not to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, int):
        raise TypeError(f"Expected int, got {type(to_operate2)}")
    if to_operate1.type == ExpressionType.CIRCL:
        to_operate1[to_operate2] = to_operate3
        main_circl.append(to_operate1)
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1.value, str):
        if not to_operate2.type == ExpressionType.POINT:
            raise TypeError(f"Expected str, got {to_operate3.type}")
        if not isinstance(to_operate2.value, str):
            raise TypeError(f"Expected str, got {type(to_operate3.value)}")
        lst = list(to_operate1)
        lst[to_operate2] = to_operate3
        main_circl.append("".join(lst))


def c_all_elements_equal(main_circl: Circl):
    to_operate1 = main_circl.pop()
    first = None
    for value in to_operate1:
        if first is None:
            first = value
        elif value != first:
            main_circl.append(False)
            break
    else:
        main_circl.append(True)


def c_circlify(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(Circl(to_operate1))


def c_uncirclify(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        for i in to_operate1:
            main_circl.append(i)
    else:
        main_circl.append(to_operate1)


def c_str_join(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        if to_operate2.type == ExpressionType.CIRCL:
            new_elements = []
            for separator in to_operate2:
                if not isinstance(separator, str):
                    raise TypeError(f"Excpected string, got {type(separator)}")
                joined_str = separator.join(to_operate1)
                new_elements.append(joined_str)
            main_circl.append(Circl(new_elements))
        elif to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, str):
            main_circl.append(to_operate2.value.join(to_operate1.value))
        else:
            if to_operate2.type == ExpressionType.POINT:
                raise TypeError(f"Expected str, got {type(to_operate2.value)}")
            else:
                TypeError(f"Expected Point got {to_operate2.type}")
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1.value, str):
        if to_operate2.type == ExpressionType.CIRCL:
            main_circl.append(to_operate1.join(to_operate2))
        elif to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, str):    
            main_circl.append(to_operate2.join(list(to_operate1)))
        else: 
            if to_operate2.type == ExpressionType.POINT:
                raise TypeError(f"Expected str, got {type(to_operate2.value)}")
            else:
                TypeError(f"Expected Point got {to_operate2.type}")
    else:
        if to_operate1.type == ExpressionType.POINT:
            raise TypeError(f"Expected str, got {type(to_operate1.value)}")
        else:
            TypeError(f"Expected Point, got {to_operate1.type}")


def c_str_split(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if to_operate1.type == ExpressionType.CIRCL:
        to_operate2 = main_circl.pop()
        if to_operate2.type == ExpressionType.CIRCL:
            new = []
            for elem in to_operate2:
                if not isinstance(elem, str):
                    raise TypeError(f"Expected string, got {type(elem)}")
                new.append(i.split(elem) for i in to_operate1)
            main_circl.append(Circl(new))
        elif to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, str):
            main_circl.append(Circl(i.split(to_operate2) for i in to_operate1))
        else:
            if to_operate2.type == ExpressionType.POINT:
                raise TypeError(f"Expected str, got {type(to_operate2.value)}")
            else:
                TypeError(f"Expected Point got {to_operate2.type}")
    elif to_operate1.type == ExpressionType.POINT and isinstance(to_operate1.value, str):
        to_operate2 = main_circl.pop()
        if to_operate2.type == ExpressionType.CIRCL:
            main_circl.append(Circl(i.split(to_operate1) for i in to_operate2))
        elif to_operate2.type == ExpressionType.POINT and isinstance(to_operate2.value, str):
            main_circl.append(Circl(to_operate1.split(to_operate2)))
        else:
            if to_operate2.type == ExpressionType.POINT:
                raise TypeError(f"Expected str, got {type(to_operate2.value)}")
            else:
                TypeError(f"Expected Point got {to_operate2.type}")
    else:
        if to_operate1.type == ExpressionType.POINT:
            raise TypeError(f"Expected str, got {type(to_operate1.value)}")
        else:
            TypeError(f"Expected Point, got {to_operate1.type}")


def c_add_circl_elems(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([i + elem for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([to_operate2 + i for i in to_operate1]))
    else:
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([to_operate1 + i for i in to_operate2]))
        else:
            main_circl.append(to_operate1 + to_operate2)


def c_sub_circl_elems(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([i - elem for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([to_operate2 - i for i in to_operate1]))
    else:
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([to_operate1 - i for i in to_operate2]))
        else:
            main_circl.append(to_operate1 - to_operate2)


def c_mul_circl_elems(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([i * elem for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([to_operate2 * i for i in to_operate1]))
    else:
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([to_operate1 * i for i in to_operate2]))
        else:
            main_circl.append(to_operate1 * to_operate2)


def c_div_circl_elems(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([i / elem for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([to_operate2 / i for i in to_operate1]))
    else:
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([to_operate1 / i for i in to_operate2]))
        else:
            main_circl.append(to_operate1 / to_operate2)


def c_mod_circl_elems(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        to_operate2 = main_circl.pop()
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([i % elem for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([to_operate2 % i for i in to_operate1]))
    else:
        to_operate2 = main_circl.pop()
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([to_operate1 % i for i in to_operate2]))
        else:
            main_circl.append(to_operate1 % to_operate2)


def c_negate(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        main_circl.append(Circl([-i for i in to_operate1]))
    else:
        main_circl.append(-to_operate1)


def c_extend(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl) and isinstance(to_operate2, Circl):
        main_circl.append(Circl(to_operate2 + to_operate1))
    elif isinstance(to_operate1, Circl):
        main_circl.append(Circl([to_operate2] + to_operate1))
    elif isinstance(to_operate2, Circl):
        main_circl.append(Circl(to_operate2 + [to_operate1]))
    else:
        main_circl.append(to_operate2 + to_operate1)


def c_mul_circlify(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    main_circl.append(Circl([to_operate2] * to_operate1))


def c_typeof(main_circl: Circl):
    to_operate1 = main_circl.pop()
    main_circl.append(to_operate1)
    main_circl.append("circl" if isinstance(to_operate1, Circl) else "string")


def c_unique(main_circl: Circl):
    to_operate1 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        seen = []
        result = []
        for i in to_operate1:
            if i not in seen:
                seen.append(i)
                result.append(i)
        main_circl.append(Circl(result))
    else:
        seen = []
        result = []
        for i in to_operate1:
            if i not in seen:
                seen.append(i)
                result.append(i)
        main_circl.append("".join(result))


def c_circlify_multiple(main_circl: Circl):
    to_operate1 = main_circl.pop()
    items = []
    for i in range(to_operate1):
        items.append(main_circl.pop())
    main_circl.append(Circl(list(reversed(items))))


def c_append_program_counter(main_circl: Circl):
    main_circl.append(main_program.get_counter())


def c_count(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        main_circl.append(to_operate1.count(to_operate2))
    else:
        main_circl.append(to_operate1.count(to_operate2))


def c_var_push(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    id_ = hash(Identifier(to_operate1))
    for var in var_circl:
        if var[0] == id_:
            var[1] = to_operate2
            return
    var_circl.append(Circl([id_, to_operate2]))


def c_var_pull(main_circl: Circl):
    to_operate1 = main_circl.pop()
    looking = hash(Identifier(to_operate1))
    for var in var_circl:
        if var[0] == looking:
            main_circl.append(i[1])
            break

def c_var_del(main_circl: Circl):
    to_operate1 = main_circl.pop()
    id_ = hash(Identifier(to_operate1))
    for i, var in enumerate(var_circl):
        if var[0] == id_:
            var_circl.pop(i)
            return

def c_regex_match(main_circl: Circl):
    to_operate1 = main_circl.pop()
    to_operate2 = main_circl.pop()
    if isinstance(to_operate1, Circl):
        if isinstance(to_operate2, Circl):
            new = []
            for elem in to_operate1:
                new.append(Circl([re.findall(elem, i) for i in to_operate2]))
            main_circl.append(Circl(new))
        else:
            main_circl.append(Circl([re.findall(i, to_operate2) for i in to_operate1]))
    else:
        if isinstance(to_operate2, Circl):
            main_circl.append(Circl([re.findall(i, to_operate1) for i in to_operate2]))
        else:
            main_circl.append(Circl(re.findall(to_operate1, to_operate2)))

def c_noop(main_circl: Circl):
    pass

# MAIN INSTRUCTION SET
# Each declared function above should correspond to a character (i.e. command)
class Instruction:
    def __init__(self, operation: Callable, calls_subroutine: bool = False) -> None:
        self.operation = operation
        self.calls_subroutine = calls_subroutine


instruction_set: Dict[str, Instruction] = {
    ".": Instruction(c_halt),
    "˅": Instruction(c_read_input),
    "π": Instruction(c_pi),
    "ε": Instruction(c_e),
    "∞": Instruction(c_inf),
    "⧺": Instruction(c_duplicate),
    "↓": Instruction(c_pop),
    "↶": Instruction(c_cycle_back),
    "↷": Instruction(c_cycle_forward),
    "⇄": Instruction(c_swap_last),
    "@": Instruction(c_move_top),
    "^": Instruction(c_println),
    "§": Instruction(c_print),
    "←": Instruction(c_read_file),
    "→": Instruction(c_write_file),
    "⇀": Instruction(c_length),
    "⦰": Instruction(c_radius),
    "♯": Instruction(c_cast_float),
    "♭": Instruction(c_cast_int),
    "Φ": Instruction(c_to_precision),
    "Ψ": Instruction(c_ordinal),
    "Ω": Instruction(c_cast_char),
    "⚂": Instruction(c_rnd),
    "¬": Instruction(c_logical_not),
    "∧": Instruction(c_logical_and),
    "∨": Instruction(c_logical_or),
    "⊕": Instruction(c_logical_xor),
    "⋘": Instruction(c_left_shift),
    "⋙": Instruction(c_right_shift),
    "=": Instruction(c_equals),
    "≠": Instruction(c_not_equals),
    "<": Instruction(c_lower_than),
    ">": Instruction(c_greater_than),
    "≤": Instruction(c_lower_than_equal),
    "≥": Instruction(c_greater_than_equal),
    "⁇": Instruction(c_jump_if_true),
    "‽": Instruction(c_jump_if_false),
    "⇒": Instruction(c_increment_program_counter_by),
    "⇐": Instruction(c_decrement_program_counter_by),
    "↺": Instruction(c_execute_as_circl, calls_subroutine=True),
    "⊲": Instruction(c_remove_nth_element),
    "⊳": Instruction(c_remove_negative_nth_element),
    "⊙": Instruction(c_set_index_zero),
    "⡳": Instruction(c_append_range),
    "⇡": Instruction(c_append_range_circl),
    "²": Instruction(c_square),
    "√": Instruction(c_sqrt),
    "ⁿ": Instruction(c_pow),
    "⌊": Instruction(c_floor),
    "⌈": Instruction(c_ceil),
    "○": Instruction(c_round),
    "⌃": Instruction(c_max),
    "⌄": Instruction(c_min),
    "|": Instruction(c_abs),
    "ℓ": Instruction(c_logn),
    "ℒ": Instruction(c_log10),
    "∿": Instruction(c_sin),
    "⌒": Instruction(c_cos),
    "∡": Instruction(c_tan),
    "✄": Instruction(c_split),
    "⊂": Instruction(c_slice),
    "↔": Instruction(c_replace_string),
    "⬆": Instruction(c_uppercase),
    "⬇": Instruction(c_lowercase),
    "∑": Instruction(c_sum),
    "Π": Instruction(c_product),
    "∈": Instruction(c_contains),
    "∉": Instruction(c_not_contains),
    "⍳": Instruction(c_indexof),
    "∩": Instruction(c_intersection),
    "∪": Instruction(c_union),
    "⊖": Instruction(c_difference),
    "⊛": Instruction(c_zip),
    "⌀": Instruction(c_stack_size),
    "κ": Instruction(c_sort),
    "ρ": Instruction(c_reverse),
    "χ": Instruction(c_replace),
    "≡": Instruction(c_all_elements_equal),
    "‾": Instruction(c_circlify),
    "_": Instruction(c_uncirclify),
    "⋃": Instruction(c_str_join),
    "✂": Instruction(c_str_split),
    "+": Instruction(c_add_circl_elems),
    "-": Instruction(c_sub_circl_elems),
    "×": Instruction(c_mul_circl_elems),
    "÷": Instruction(c_div_circl_elems),
    "%": Instruction(c_mod_circl_elems),
    "⁻": Instruction(c_negate),
    "∥": Instruction(c_extend),
    "⊡": Instruction(c_mul_circlify),
    "τ": Instruction(c_typeof),
    "⌂": Instruction(c_unique),
    "⊤": Instruction(c_circlify_multiple),
    "⊞": Instruction(c_append_program_counter),
    "ν": Instruction(c_count),
    "↦": Instruction(c_var_push),
    "↤": Instruction(c_var_pull),
    "🜏": Instruction(c_var_del),
    "Я": Instruction(c_regex_match),
    "∅": Instruction(c_noop)
}
