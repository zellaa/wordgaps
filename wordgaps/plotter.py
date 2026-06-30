import string
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from wordgaps.utils import is_outbound, is_inbound, REPO_ROOT


def plot_word(word: str):
    """Plot the trajectory and envelope widths for a word."""
    word = word.upper()
    if not word.isalpha():
        raise ValueError("Word must only contain alphabetical characters.")

    x = list(range(len(word)))
    y = [string.ascii_uppercase.index(char) for char in word]

    out_widths = []
    curr_min = y[0]
    curr_max = y[0]
    out_widths.append(0)
    for i in range(1, len(word)):
        curr_min = min(curr_min, y[i])
        curr_max = max(curr_max, y[i])
        out_widths.append(curr_max - curr_min)

    in_widths = []
    for i in range(len(word)):
        suffix = y[i:]
        in_widths.append(max(suffix) - min(suffix))

    outbound = is_outbound(word)
    inbound = is_inbound(word)

    plot_outbound_width = True
    plot_inbound_width = True

    if outbound and not inbound:
        plot_inbound_width = False
    elif inbound and not outbound:
        plot_outbound_width = False

    plt.style.use("default")
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    })

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 9), sharex=True, dpi=300
    )

    fig.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#ffffff")
    ax2.set_facecolor("#ffffff")

    ax1.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)
    ax2.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)

    if len(word) >= 2:
        current_min = y[0]
        current_max = y[0]

        for i in range(len(word) - 1):
            y_a, y_b = y[i], y[i + 1]
            x_eval = np.linspace(i, i + 1, 100)
            y_traj = y_a + (y_b - y_a) * (x_eval - i)

            if y_b < current_min:
                top = np.minimum(y_traj, current_min)
                bottom = np.ones_like(x_eval) * current_max
                current_min = y_b
            elif y_b > current_max:
                top = np.ones_like(x_eval) * current_min
                bottom = np.maximum(y_traj, current_max)
                current_max = y_b
            else:
                top = np.ones_like(x_eval) * current_min
                bottom = np.ones_like(x_eval) * current_max

            ax1.fill_between(
                x_eval,
                top,
                bottom,
                color="#3b82f6",
                alpha=0.15,
                edgecolor="none",
            )

    (traj_line,) = ax1.plot(
        x,
        y,
        color="#1e3a8a",
        linewidth=2,
        marker="o",
        markersize=6,
        markerfacecolor="#ffffff",
        markeredgecolor="#1e3a8a",
        markeredgewidth=1.5,
    )

    ax1.set_yticks(list(range(26)))
    ax1.set_yticklabels(list(string.ascii_uppercase), fontsize=10, color="#0f172a")
    ax1.set_ylim(-0.5, 25.5)
    ax1.invert_yaxis()

    ax1.set_title(
        r"\textbf{Word Gap Trajectory: " + word + "}",
        fontsize=16,
        color="#0f172a",
        pad=15,
    )
    ax1.set_ylabel(
        r"\textbf{Alphabetical Position}", fontsize=12, color="#0f172a", labelpad=10
    )

    legend_handles2 = []
    legend_labels2 = []

    if plot_outbound_width:
        (out_width_line,) = ax2.plot(
            x,
            out_widths,
            color="#3b82f6",
            linewidth=2,
            marker="s",
            markersize=5,
            markerfacecolor="#ffffff",
            markeredgecolor="#3b82f6",
            markeredgewidth=1.5,
        )
        legend_handles2.append(out_width_line)
        legend_labels2.append(
            r"Outbound Envelope Width (Prefix Span)"
        )

    if plot_inbound_width:
        (in_width_line,) = ax2.plot(
            x,
            in_widths,
            color="#ef4444",
            linewidth=2,
            marker="^",
            markersize=5,
            markerfacecolor="#ffffff",
            markeredgecolor="#ef4444",
            markeredgewidth=1.5,
        )
        legend_handles2.append(in_width_line)
        legend_labels2.append(
            r"Inbound Envelope Width (Suffix Span)"
        )

    ax2.set_ylabel(
        r"\textbf{Envelope Width (Letters)}",
        fontsize=12,
        color="#0f172a",
        labelpad=10,
    )
    ax2.set_xlabel(
        r"\textbf{Word Letter Sequence}", fontsize=12, color="#0f172a", labelpad=10
    )

    ax2.set_ylim(-1, 26)

    ax2.set_xticks(x)
    ax2.set_xticklabels(list(word), fontsize=12, color="#0f172a")

    for ax_sp in (ax1, ax2):
        for spine in ax_sp.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1)

    envelope_patch = plt.Rectangle((0, 0), 1, 1, fc="#3b82f6", alpha=0.15)
    ax1.legend(
        [envelope_patch, traj_line],
        [r"Outbound Envelope", r"Word Trajectory"],
        loc="upper right",
        fontsize=9,
        framealpha=0.9,
        edgecolor="#cbd5e1",
    )

    if legend_handles2:
        ax2.legend(
            legend_handles2,
            legend_labels2,
            loc="upper right",
            fontsize=9,
            framealpha=0.9,
            edgecolor="#cbd5e1",
        )

    plt.tight_layout()

    output_dir = REPO_ROOT / "output-images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{word.lower()}.png"
    plt.savefig(
        output_path,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    print(f"Plot saved successfully to {output_path.resolve()}")
    try:
        subprocess.run(["open", str(output_path)], check=True)
    except Exception as e:
        print(f"Could not open plot file: {e}")


def plot_distribution(N: int, show_outbound: bool, show_inbound: bool, show_both: bool):
    """Plot envelope width distribution for all valid words of length N."""
    import json
    import string
    from wordgaps.utils import VALID_WORDS_JSON_PATH, REPO_ROOT

    with open(VALID_WORDS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    length_str = str(N)
    if length_str not in data:
        print(f"No valid words of length {N} found in {VALID_WORDS_JSON_PATH}.")
        return

    out_words = data[length_str].get("outbound_words", []) if (show_outbound or show_both) else []
    in_words = data[length_str].get("inbound_words", []) if (show_inbound or show_both) else []

    if show_both or (show_outbound and show_inbound):
        mode = "both"
    elif show_outbound:
        mode = "outbound"
    else:
        mode = "inbound"

    if mode == "outbound" and not out_words:
        print(f"No outbound words of length {N} found.")
        return
    if mode == "inbound" and not in_words:
        print(f"No inbound words of length {N} found.")
        return
    if mode == "both" and not out_words and not in_words:
        print(f"No outbound or inbound words of length {N} found.")
        return

    plt.style.use("default")
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    })

    output_dir = REPO_ROOT / "output-images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"dist_{N}_{mode}.png"

    def get_outbound_widths(w: str):
        vals = [string.ascii_uppercase.index(c) for c in w.upper()]
        w_out = [0]
        c_min = vals[0]
        c_max = vals[0]
        for val in vals[1:]:
            c_min = min(c_min, val)
            c_max = max(c_max, val)
            w_out.append(c_max - c_min)
        return w_out

    def get_inbound_widths(w: str):
        vals = [string.ascii_uppercase.index(c) for c in w.upper()]
        w_in = []
        for j in range(len(vals)):
            suffix = vals[j:]
            w_in.append(max(suffix) - min(suffix))
        return w_in

    x_vals = list(range(1, N + 1))

    if mode == "both":
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 9), sharex=True, dpi=300)
        fig.patch.set_facecolor("#ffffff")
        ax1.set_facecolor("#ffffff")
        ax2.set_facecolor("#ffffff")

        ax1.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)
        ax2.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)

        for w in out_words:
            ax1.plot(x_vals, get_outbound_widths(w), color="#3b82f6", alpha=0.3, linewidth=1.5)
        ax1.set_title(
            r"\textbf{Outbound Envelope Width Distribution (Length " + str(N) + ", " + str(len(out_words)) + " words)}",
            fontsize=14, color="#0f172a", pad=15
        )
        ax1.set_ylabel(r"\textbf{Prefix Width (Letters)}", fontsize=12, color="#0f172a")
        ax1.set_ylim(-1, 26)

        for w in in_words:
            ax2.plot(x_vals, get_inbound_widths(w), color="#ef4444", alpha=0.3, linewidth=1.5)
        ax2.set_title(
            r"\textbf{Inbound Envelope Width Distribution (Length " + str(N) + ", " + str(len(in_words)) + " words)}",
            fontsize=14, color="#0f172a", pad=15
        )
        ax2.set_ylabel(r"\textbf{Suffix Width (Letters)}", fontsize=12, color="#0f172a")
        ax2.set_xlabel(r"\textbf{Sequence Position}", fontsize=12, color="#0f172a")
        ax2.set_ylim(-1, 26)
        ax2.set_xticks(x_vals)

        for ax in (ax1, ax2):
            for spine in ax.spines.values():
                spine.set_color("#475569")
                spine.set_linewidth(1)
    else:
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        fig.patch.set_facecolor("#ffffff")
        ax.set_facecolor("#ffffff")
        ax.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)

        if mode == "outbound":
            for w in out_words:
                ax.plot(x_vals, get_outbound_widths(w), color="#3b82f6", alpha=0.3, linewidth=1.5)
            ax.set_title(
                r"\textbf{Outbound Envelope Width Distribution (Length " + str(N) + ", " + str(len(out_words)) + " words)}",
                fontsize=14, color="#0f172a", pad=15
            )
            ax.set_ylabel(r"\textbf{Prefix Width (Letters)}", fontsize=12, color="#0f172a")
        else:
            for w in in_words:
                ax.plot(x_vals, get_inbound_widths(w), color="#ef4444", alpha=0.3, linewidth=1.5)
            ax.set_title(
                r"\textbf{Inbound Envelope Width Distribution (Length " + str(N) + ", " + str(len(in_words)) + " words)}",
                fontsize=14, color="#0f172a", pad=15
            )
            ax.set_ylabel(r"\textbf{Suffix Width (Letters)}", fontsize=12, color="#0f172a")

        ax.set_xlabel(r"\textbf{Sequence Position}", fontsize=12, color="#0f172a")
        ax.set_ylim(-1, 26)
        ax.set_xticks(x_vals)
        for spine in ax.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1)

    plt.tight_layout()
    plt.savefig(
        output_path,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    print(f"Distribution plot saved successfully to {output_path.resolve()}")
    try:
        subprocess.run(["open", str(output_path)], check=True)
    except Exception as e:
        print(f"Could not open plot file: {e}")


def plot_counts_by_length():
    """Plot the number of inbound and outbound words per word length."""
    import json
    from wordgaps.utils import VALID_WORDS_JSON_PATH, REPO_ROOT

    with open(VALID_WORDS_JSON_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    lengths = sorted([int(k) for k in data.keys()])
    out_counts = [len(data[str(l)].get("outbound_words", [])) for l in lengths]
    in_counts = [len(data[str(l)].get("inbound_words", [])) for l in lengths]

    plt.style.use("default")
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    })

    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    fig.patch.set_facecolor("#ffffff")
    ax.set_facecolor("#ffffff")
    ax.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)

    x = np.arange(len(lengths))
    width = 0.35

    rects1 = ax.bar(x - width/2, out_counts, width, label='Outbound Words', color='#3b82f6', alpha=0.85)
    rects2 = ax.bar(x + width/2, in_counts, width, label='Inbound Words', color='#ef4444', alpha=0.85)

    ax.set_title(r"\textbf{Valid Word Counts by Length}", fontsize=16, color="#0f172a", pad=15)
    ax.set_xlabel(r"\textbf{Word Length (Letters)}", fontsize=12, color="#0f172a", labelpad=10)
    ax.set_ylabel(r"\textbf{Number of Words}", fontsize=12, color="#0f172a", labelpad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([str(l) for l in lengths], fontsize=10, color="#0f172a")

    ax.bar_label(rects1, padding=3, fontsize=8, color="#334155")
    ax.bar_label(rects2, padding=3, fontsize=8, color="#334155")

    max_val = max(max(out_counts), max(in_counts)) if out_counts or in_counts else 0
    ax.set_ylim(0, max_val * 1.15 if max_val > 0 else 10)

    ax.legend(loc="upper right", framealpha=0.9, edgecolor="#cbd5e1")

    for spine in ax.spines.values():
        spine.set_color("#475569")
        spine.set_linewidth(1)

    plt.tight_layout()

    output_dir = REPO_ROOT / "output-images"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "word_counts_by_length.png"
    plt.savefig(
        output_path,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    print(f"Counts plot saved successfully to {output_path.resolve()}")

    try:
        subprocess.run(["open", str(output_path)], check=True)
    except Exception as e:
        print(f"Could not open plot file: {e}")
