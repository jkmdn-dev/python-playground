from __future__ import annotations  # noqa: D100

import random
import shutil
from typing import Any, Final, Generator, TypeVar, Iterable, Callable

T = TypeVar("T")

"""Print an arrow to stdout."""

SMALLEST_SIZE = 2


def create_arrow(size: int, symbol: str = "*", void_filler: str = " ") -> str:
    """Print arrow to stdout."""
    # rescale size
    size += 2

    # defining useful sizes
    middle_position: Final[int] = size + 1
    arrow_body_left_padding: Final[int] = size // 2 if size % 2 == 0 else size // 2 + 1
    arrow_body_length: Final[int] = size // 2 + 1

    # closure to append left side to output
    #   - will reverse the line and append
    output = ""

    def left_line_to_output(left_line: str, divider: str = void_filler) -> None:
        nonlocal output
        output += left_line + divider + left_line[::-1] + "\n"

    # arrow head
    arrow_head_left_padding = middle_position - 1
    arrow_head_right_padding = 0

    left_line_to_output(void_filler * arrow_head_left_padding, symbol)
    arrow_head_left_padding -= 1

    for _ in range(size - 1):
        left_line_to_output(
            void_filler * arrow_head_left_padding
            + symbol
            + void_filler * arrow_head_right_padding,
            void_filler,
        )

        arrow_head_left_padding -= 1
        arrow_head_right_padding += 1  # noqa: SIM113

    if size == SMALLEST_SIZE:
        # arrow head end-flats
        left_line_to_output(symbol * SMALLEST_SIZE, void_filler)

        # arrow body
        left_line_to_output(void_filler * (SMALLEST_SIZE - 1) + symbol, void_filler)
        left_line_to_output(void_filler * (SMALLEST_SIZE - 1) + symbol, symbol)

    else:
        # arrow head end-flats

        flats_length = arrow_body_left_padding + 1

        # minus one to account for the divider
        middle_half_length = middle_position - flats_length - 1

        left_line_to_output(
            symbol * flats_length + void_filler * middle_half_length,
        )

        # arrow body
        for _ in range(arrow_body_length):
            left_line_to_output(
                void_filler * arrow_body_left_padding
                + symbol
                + void_filler * middle_half_length,
            )

        # arrow body end
        middle_half_length += 1

        left_line_to_output(
            void_filler * arrow_body_left_padding + symbol * middle_half_length,
            symbol,
        )

    return output


def combine_lines(
    prompts: list[str],
    divider_symbol: str = " | ",
    max_width: int | None = None,
) -> str:
    """Will combine the lines of all `prompts` divided by `devider_symbol`."""
    assert len(prompts) != 0, "typechecking, hopefully, wont let this happen"

    max_line_length = max(max(len(line) for line in p.split("\n")) for p in prompts)

    ps = list(prompts)
    lines: list[str] = [
        (line + " " * (max(max_line_length, len(line)) - len(line)) + divider_symbol)
        for line in ps.pop(0).split("\n")
    ]

    def add_lines(lines_to_add: list[str]) -> None:
        nonlocal lines
        for index, line_to_add in enumerate(lines_to_add):
            line_len = len(line_to_add)
            lines[index] += (
                line_to_add
                + " " * (max(max_line_length, line_len) - line_len)
                + divider_symbol
            )

    while len(ps) != 0:
        current_prompt_lines = ps.pop(0).split("\n")
        add_lines(current_prompt_lines)

    if not max_width:
        return "\n".join(lines)

    assert max_line_length
    assert max_line_length > 0

    for index in range(len(lines)):
        lines[index] = lines[index][:max_width]

    return "\n".join(lines)


def random_product(
    *input_lists: list[T],
) -> Generator[list[T | None], T | None, T | None]:
    """Return a random product of the elements of `input_lists`."""
    longest_list = max(len(lst) for lst in input_lists)
    not_used_index_dict = {
        i: list(range(len(lst))) for i, lst in enumerate(input_lists)
    }

    for _ in range(longest_list):
        output_indexes: list[int | None] = []

        for i in range(len(input_lists)):
            if len(not_used_index_dict[i]) == 0:
                output_indexes.append(None)
                continue

            random_index = random.choice(not_used_index_dict[i])
            not_used_index_dict[i].remove(random_index)

            output_indexes.append(random_index)

        output: list[Any | None] = []
        for i, outp_i in enumerate(output_indexes):
            if outp_i is None:
                output.append(None)
                continue

            output.append(input_lists[i][outp_i])

        yield output


def find_first(predicate: Callable[[T], bool], iterable: Iterable[T]) -> int:
    """Find index of first element of `iterable` that satisfies `predicate`.
    Returns `len(iterable)` if no element satisfies `predicate`.
    """
    index = 0
    for index, element in enumerate(iterable):
        if predicate(element):
            return index

    return index + 1


def print_random_combinations_arrows_to_stdout(
    amount: int,
    fillers: list[str] = [" ", ".", "`", "_", "^", "~"],
    symbols: list[str] = ["*", "#", "$", "@", "&", "+"],
    allow_line_overflow: bool = False,
) -> None:
    """Prints random combinations of fillers and symbols to stdout.

    if `allow_line_overflow` is True, the line will overflow the terminal width. Otherwise, it will be truncated to the terminal width.

    Args:
        amount: amount of arrows of size ranging from 0 to `amount` to print

    Keyword arguments:
    fillers -- list of fillers to use (default: [" ", ".", "`", "_", "^", "~"])
    symbols -- list of symbols to use (default: ["*", "#", "$", "@", "&", "+"])
    allow_line_overflow -- whether to allow the line to overflow the terminal width (default: False)
    """
    term_x_size, _ = shutil.get_terminal_size()
    max_stdout_width = term_x_size if not allow_line_overflow else None

    for i in range(amount):
        prompts: list[str] = []
        for filler, symbol in random_product(fillers, symbols):
            header = f"symbol: '{symbol}', filler: '{filler}'\n"
            header_len = len(header)
            header += "-" * header_len + "\n"
            header += " " * header_len + "\n"
            arrow = create_arrow(
                i,
                symbol if symbol else "*",
                filler if filler else " ",
            )
            prompts.append(header + arrow)

        combined = combine_lines(prompts, max_width=max_stdout_width)

        # `-1` since `find_first` returns where '\n' is
        line_len = find_first(lambda x: x == "\n", combined) - 1
        combined += "\n" + "-" * line_len
        combined += "\n" + " " * line_len

        title_half_len = line_len // 2
        title_half_len -= 1 if line_len % 2 != 0 else 0

        print("#" * title_half_len, i, "#" * title_half_len)
        print(combined)


if __name__ == "__main__":
    print_random_combinations_arrows_to_stdout(10)
