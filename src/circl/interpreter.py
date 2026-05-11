from copy import copy
import time
import traceback
from typing import cast
from typing import NamedTuple

from .circl import Circl
from .instruction_set import instruction_set, Instruction
from .program import main_program
from .source_info import SourcecodeInfo

class Program(NamedTuple):
    full_source: str
    offset: int

# TODO: Move open_quotes into Program?
def circl_gen(program: Program, open_quotes="", source_info: SourcecodeInfo = None) -> tuple[Circl, int]:
    if source_info == None:
        source_info = SourcecodeInfo(from_position=program.offset, to_position=program.offset)
    to_circl: list[Circl, int, str] = []

    i: int = program.offset
    char: str
    while True: # while in current circl
        if i >= len(program.full_source):
            break
        char = program.full_source[i]
        if char in ("\t", " "):
            i += 1
            source_info.to_position = i
            continue
        if char == "\n":
            i += 1
            source_info.to_position = 0
            source_info.to_line += 1
            continue
        # TODO: add {} and () and [] for subcircles
        # TODO: make the quotes " ' ` put in a single string instead of a subcircle
        # TODO: add \ for escaping characters
        #
        if char in ('"', "'", "`"):
            if open_quotes and open_quotes[-1] is char:
                break
            else:
                # Get new sub_circl and letters to be skipped
                sub_circl, skip_to = circl_gen(
                    Program(full_source=program.full_source, offset=i+1),
                    open_quotes + char,
                    source_info = copy(source_info)
                )
                # typing shenanigans
                sub_circl.source_info = cast(SourcecodeInfo, sub_circl.source_info)

                # Inform current circl of where we are now
                source_info.from_line = sub_circl.source_info.to_line
                source_info.from_position = sub_circl.source_info.to_position + 1

                # Cleanup
                to_circl.append(sub_circl)
                i = skip_to
        else:
            to_add: int | str = char
            if char.isnumeric():
                to_add = int(to_add)

            to_circl.append(to_add)  # append to current circl

        # Prepare for next iteration
        i += 1
        source_info.to_position = i

    return (
        Circl(
            to_circl,
            source_info=source_info
        ),
        i
    )   # push current circl


def decode(program: str = ".", file: str = "<stdin>") -> Circl:
    main_circl, _ = circl_gen(Program(full_source=program, offset=0), "", SourcecodeInfo(file=file))
    print("Compiled a circl with radius ", main_circl.radius())
    return main_circl


def execute(executing_circl) -> str:
    main_program.add_counter()
    while True:
        # print("-" * 2 * (main_program.number_of_counters()-1), executing_circl, f"counter is at {main_program.get_counter()}")
        if len(executing_circl) == 0:
            main_program.remove_counter()
            if main_program.number_of_counters() == 0:
                return executing_circl.stdout_copy
            break # Change this later to return the return-value instead
        current_step = main_program.get_counter()
        command = executing_circl[current_step]
        try:
            if isinstance(command, Circl) or command not in instruction_set.keys():
                executing_circl.append(command)
            else:
                instruction: Instruction = instruction_set[command]

                # instruction exists for command -> execute it
                if instruction.calls_subroutine:
                    instruction.operation(executing_circl, execute)
                else:
                    instruction.operation(executing_circl)
        
        except Exception as e:
            if isinstance(command, Circl) and command.source_info is not None:
                line_info: str
                if command.source_info.from_line == command.source_info.to_line:
                    line_info = f"line {command.source_info.from_line}"
                else:
                    line_info = f"lines {command.source_info.from_line} to {command.source_info.to_line}"

                position_info: str
                if command.source_info.from_position == command.source_info.to_position:
                    position_info = f"at position {command.source_info.from_position}"
                else:
                    position_info = f"from {command.source_info.from_position} to {command.source_info.to_position}"

                print(f"Exception in {command.source_info.file} on {line_info} {position_info}: {e}")
            else:
                print(f"Exception: {e}")
            if main_program.verbose_exceptions:
                traceback.print_stack()
            print("Appending current exception to current circl")
            executing_circl.append(str(e))

        main_program.increment_counter()
        time.sleep(0.01)
