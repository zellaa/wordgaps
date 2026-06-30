import subprocess
from pathlib import Path


def get_repo_root() -> Path:
    try:
        res = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], stderr=subprocess.DEVNULL)
        return Path(res.decode("utf-8").strip())
    except Exception:
        return Path(__file__).resolve().parent.parent


REPO_ROOT = get_repo_root()
DICT_PATH = REPO_ROOT / "dict" / "words.txt"
VALID_WORDS_JSON_PATH = REPO_ROOT / "dict" / "valid_words.json"


def alphabet_values(word: str) -> list[int]:
    """Return zero-based A=0 through Z=25 values for a word."""
    return [ord(char.upper()) - ord("A") for char in word]


def prefix_widths(word: str) -> list[int]:
    """Return running prefix envelope widths in one forward pass."""
    values = alphabet_values(word)
    if not values:
        return []

    min_value = max_value = values[0]
    widths = [0]
    for value in values[1:]:
        if value < min_value:
            min_value = value
        elif value > max_value:
            max_value = value
        widths.append(max_value - min_value)
    return widths


def suffix_widths(word: str) -> list[int]:
    """Return running suffix envelope widths in one backward pass."""
    values = alphabet_values(word)
    if not values:
        return []

    widths = [0] * len(values)
    min_value = max_value = values[-1]
    for index in range(len(values) - 2, -1, -1):
        value = values[index]
        if value < min_value:
            min_value = value
        elif value > max_value:
            max_value = value
        widths[index] = max_value - min_value
    return widths


def is_outbound(word: str) -> bool:
    """
    Check if a word is outbound.
    A word is outbound if every character from the second onwards lies outside
    the range spanned by the preceding characters.
    """
    if not word:
        return False
    min_char = max_char = word[0]
    for char in word[1:]:
        if char < min_char:
            min_char = char
        elif char > max_char:
            max_char = char
        else:
            return False
    return True


def is_inbound(word: str) -> bool:
    """
    Check if a word is inbound.
    A word is inbound if its reversed sequence is outbound.
    """
    if not word:
        return False
    min_char = max_char = word[-1]
    for index in range(len(word) - 2, -1, -1):
        char = word[index]
        if char < min_char:
            min_char = char
        elif char > max_char:
            max_char = char
        else:
            return False
    return True


def classify_word(word: str) -> tuple[bool, bool]:
    """Return ``(is_outbound, is_inbound)`` using one pass from both ends."""
    word_len = len(word)
    if word_len == 0:
        return False, False

    outbound = True
    inbound = True
    out_min = out_max = word[0]
    in_min = in_max = word[-1]
    last_index = word_len - 1

    for offset in range(1, word_len):
        if outbound:
            out_char = word[offset]
            if out_char < out_min:
                out_min = out_char
            elif out_char > out_max:
                out_max = out_char
            else:
                outbound = False

        if inbound:
            in_char = word[last_index - offset]
            if in_char < in_min:
                in_min = in_char
            elif in_char > in_max:
                in_max = in_char
            else:
                inbound = False

        if not outbound and not inbound:
            break

    return outbound, inbound
