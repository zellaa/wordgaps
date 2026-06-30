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
    return is_outbound(word[::-1])
