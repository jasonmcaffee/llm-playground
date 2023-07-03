from typing import Tuple
import tiktoken


def calculate_number_of_tokens_for_gpt3point5(prompt: str) -> Tuple[int, int]:
    max_tokens = 4096
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    number_of_tokens = len(encoding.encode(prompt))
    remaining_tokens = max_tokens - number_of_tokens
    return number_of_tokens, remaining_tokens
