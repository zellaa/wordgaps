import json
from collections import defaultdict
import typer
from wordgaps.utils import is_outbound, is_inbound, DICT_PATH, VALID_WORDS_JSON_PATH
from wordgaps.plotter import plot_word, plot_distribution

app = typer.Typer(help="Wordgaps CLI to analyze outbound and inbound words.")


def run_find_longest():
    if not DICT_PATH.exists():
        typer.echo(f"Error: Dictionary not found at {DICT_PATH}", err=True)
        raise typer.Exit(code=1)

    buckets = defaultdict(list)
    with open(DICT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            word = line.rstrip()
            if word:
                buckets[len(word)].append(word)

    outbound_words = []
    max_out_len = 0
    for wlen in sorted(buckets.keys(), reverse=True):
        for word in buckets[wlen]:
            if is_outbound(word):
                outbound_words.append(word)
        if outbound_words:
            max_out_len = wlen
            break

    inbound_words = []
    max_in_len = 0
    for wlen in sorted(buckets.keys(), reverse=True):
        for word in buckets[wlen]:
            if is_inbound(word):
                inbound_words.append(word)
        if inbound_words:
            max_in_len = wlen
            break

    typer.echo(f"Largest Outbound Words (Length {max_out_len}):")
    for word in outbound_words:
        typer.echo(f"  - {word}")

    typer.echo(f"\nLargest Inbound Words (Length {max_in_len}):")
    for word in inbound_words:
        typer.echo(f"  - {word}")


def run_generate_valid():
    if not DICT_PATH.exists():
        typer.echo(f"Error: Dictionary not found at {DICT_PATH}", err=True)
        raise typer.Exit(code=1)

    results = defaultdict(lambda: {"outbound_words": [], "inbound_words": []})

    with open(DICT_PATH, "r", encoding="utf-8") as f:
        for line in f:
            word = line.strip().lower()
            if not word or not word.isalpha():
                continue

            wlen = len(word)
            if is_outbound(word):
                results[wlen]["outbound_words"].append(word)
            if is_inbound(word):
                results[wlen]["inbound_words"].append(word)

    sorted_results = {}
    for wlen in sorted(results.keys()):
        if results[wlen]["outbound_words"] or results[wlen]["inbound_words"]:
            sorted_results[str(wlen)] = {
                "outbound_words": sorted(results[wlen]["outbound_words"]),
                "inbound_words": sorted(results[wlen]["inbound_words"])
            }

    with open(VALID_WORDS_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(sorted_results, f, indent=2)

    typer.echo(f"Successfully generated {VALID_WORDS_JSON_PATH}")


def run_plot(word: str):
    try:
        plot_word(word)
    except Exception as e:
        typer.echo(f"Error generating plot: {e}", err=True)
        raise typer.Exit(code=1)


@app.callback(invoke_without_command=True)
def main(
    find_longest: bool = typer.Option(
        False,
        "--find-longest",
        help="Find the longest outbound and inbound words in the dictionary",
    ),
    plot: str = typer.Option(
        None,
        "--plot",
        help="Generate trajectory plot for the specified word",
    ),
    generate_valid: bool = typer.Option(
        False,
        "--generate-valid",
        help="Generate the dict/valid_words.json file",
    ),
    plot_dist: int = typer.Option(
        None,
        "--plot-dist",
        help="Plot the envelope width distribution for all valid words of length N",
    ),
    outbound: bool = typer.Option(
        False,
        "--outbound",
        help="Plot outbound distribution (used with --plot-dist)",
    ),
    inbound: bool = typer.Option(
        False,
        "--inbound",
        help="Plot inbound distribution (used with --plot-dist)",
    ),
    both: bool = typer.Option(
        False,
        "--both",
        help="Plot both outbound and inbound distributions (used with --plot-dist)",
    ),
):
    if not (find_longest or plot or generate_valid or plot_dist is not None):
        raise typer.BadParameter(
            "Please specify at least one option: --find-longest, --plot, --generate-valid, or --plot-dist."
        )

    if plot_dist is not None and not (outbound or inbound or both):
        raise typer.BadParameter(
            "When using --plot-dist, you must specify --outbound, --inbound, or --both."
        )

    if find_longest:
        run_find_longest()

    if generate_valid:
        run_generate_valid()

    if plot:
        run_plot(plot)

    if plot_dist is not None:
        if not VALID_WORDS_JSON_PATH.exists():
            typer.echo(f"{VALID_WORDS_JSON_PATH} not found. Generating it first...", err=True)
            run_generate_valid()
        plot_distribution(plot_dist, outbound, inbound, both)


if __name__ == "__main__":
    app()
