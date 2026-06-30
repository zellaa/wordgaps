from collections import defaultdict
from pathlib import Path


def is_outbound(word: str) -> bool:
    """
    For any word to be outbound:
    1. Start with the first character, this is the minimum and maximum value.
    2. Check if the next character is either below the minimum, or above the maximum.
    3. If so, update the new min/max
    4. If not, exit
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
    Inbound-ness is the same as outbound-ness on the reverse of a given word.
    """
    return is_outbound(word[::-1])


def find_largest_words():
    # find words
    dict_path = Path(__file__).resolve().parent / "dict" / "words.txt"

    # group by length
    buckets = defaultdict(list)
    with open(dict_path, "r", encoding="utf-8") as f:
        for line in f:
            word = line.rstrip()
            if word:
                buckets[len(word)].append(word)

    # find the largest outbound by searching by word length in decreasing order
    outbound_words = []
    max_out_len = 0
    for wlen in sorted(buckets.keys(), reverse=True):
        for word in buckets[wlen]:
            if is_outbound(word):
                outbound_words.append(word)
        if outbound_words:
            max_out_len = wlen
            break

    # find the largest inbound by searching by word length in decreasing order
    inbound_words = []
    max_in_len = 0
    for wlen in sorted(buckets.keys(), reverse=True):
        for word in buckets[wlen]:
            if is_inbound(word):
                inbound_words.append(word)
        if inbound_words:
            max_in_len = wlen
            break

    return max_out_len, outbound_words, max_in_len, inbound_words


def main():
    max_out_len, outbound_words, max_in_len, inbound_words = find_largest_words()

    print(f"Largest Outbound Words (Length {max_out_len}):")
    for word in outbound_words:
        print(f"  - {word}")

    print(f"\nLargest Inbound Words (Length {max_in_len}):")
    for word in inbound_words:
        print(f"  - {word}")


if __name__ == "__main__":
    main()
