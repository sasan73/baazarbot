from typing import Generator


def batch(input: list, size: int) -> Generator[list, None, None]:
    yield from [input[i:i+size] for i in range(0, len(input), batch_size)]