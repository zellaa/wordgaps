import sys
from pathlib import Path
import string
import numpy as np
import matplotlib.pyplot as plt


def is_outbound(word: str) -> bool:
    """Check if a word is outbound."""
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
    """Check if a word is inbound."""
    return is_outbound(word[::-1])


def main():
    if len(sys.argv) < 2:
        print("Usage: uv run plotter.py <word>")
        sys.exit(1)

    word = sys.argv[1].upper()
    if not word.isalpha():
        print("Error: Word must only contain alphabetical characters.")
        sys.exit(1)

    # Set up coordinates
    x = list(range(len(word)))
    # Alphabet position: A -> 0, B -> 1, ..., Z -> 25
    y = [string.ascii_uppercase.index(char) for char in word]

    # Calculate Outbound (Prefix) envelope widths
    out_widths = []
    curr_min = y[0]
    curr_max = y[0]
    out_widths.append(0)
    for i in range(1, len(word)):
        curr_min = min(curr_min, y[i])
        curr_max = max(curr_max, y[i])
        out_widths.append(curr_max - curr_min)

    # Calculate Inbound (Suffix) envelope widths
    in_widths = []
    for i in range(len(word)):
        suffix = y[i:]
        in_widths.append(max(suffix) - min(suffix))

    # Determine which width curves to plot
    outbound = is_outbound(word)
    inbound = is_inbound(word)

    plot_outbound_width = True
    plot_inbound_width = True

    if outbound and not inbound:
        plot_inbound_width = False
    elif inbound and not outbound:
        plot_outbound_width = False

    # LaTeX styling configuration
    plt.style.use("default")
    plt.rcParams.update({
        "text.usetex": True,
        "font.family": "serif",
        "font.serif": ["Computer Modern Roman", "Times New Roman", "DejaVu Serif"],
    })

    # Create 2 subplots sharing the x-axis
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(10, 9), sharex=True, dpi=300
    )

    # White background for both plots
    fig.patch.set_facecolor("#ffffff")
    ax1.set_facecolor("#ffffff")
    ax2.set_facecolor("#ffffff")

    # Grid lines - subtle light gray dashed lines
    ax1.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)
    ax2.grid(True, which="both", color="#e2e8f0", linestyle="--", linewidth=0.7)

    # ------------------ SUBPLOT 1: Trajectory & Envelope Shading ------------------
    if len(word) >= 2:
        current_min = y[0]
        current_max = y[0]

        for i in range(len(word) - 1):
            y_a, y_b = y[i], y[i + 1]
            x_eval = np.linspace(i, i + 1, 100)
            y_traj = y_a + (y_b - y_a) * (x_eval - i)

            if y_b < current_min:  # New minimum
                top = np.minimum(y_traj, current_min)
                bottom = np.ones_like(x_eval) * current_max
                current_min = y_b
            elif y_b > current_max:  # New maximum
                top = np.ones_like(x_eval) * current_min
                bottom = np.maximum(y_traj, current_max)
                current_max = y_b
            else:  # Not outbound
                top = np.ones_like(x_eval) * current_min
                bottom = np.ones_like(x_eval) * current_max

            ax1.fill_between(
                x_eval,
                top,
                bottom,
                color="#3b82f6",  # Light blue
                alpha=0.15,
                edgecolor="none",
            )

    # Plot trajectory
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

    # ------------------ SUBPLOT 2: Shaded Area Widths ------------------
    legend_handles2 = []
    legend_labels2 = []

    out_status = "Yes" if outbound else "No"
    in_status = "Yes" if inbound else "No"

    if plot_outbound_width:
        (out_width_line,) = ax2.plot(
            x,
            out_widths,
            color="#3b82f6",  # Blue
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
            color="#ef4444",  # Red
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

    # Ensure y-axis on width plot goes from 0 to 25
    ax2.set_ylim(-1, 26)

    # Configure shared x-axis labels on the bottom plot
    ax2.set_xticks(x)
    ax2.set_xticklabels(list(word), fontsize=12, color="#0f172a")

    # Style spines for both subplots
    for ax_sp in (ax1, ax2):
        for spine in ax_sp.spines.values():
            spine.set_color("#475569")
            spine.set_linewidth(1)

    # Legend for Subplot 1
    envelope_patch = plt.Rectangle((0, 0), 1, 1, fc="#3b82f6", alpha=0.15)
    ax1.legend(
        [envelope_patch, traj_line],
        [r"Outbound Envelope", r"Word Trajectory"],
        loc="upper right",
        fontsize=9,
        framealpha=0.9,
        edgecolor="#cbd5e1",
    )

    # Legend for Subplot 2
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

    # Save the output image
    output_path = Path("wordgap.png")
    plt.savefig(
        output_path,
        facecolor=fig.get_facecolor(),
        edgecolor="none",
        bbox_inches="tight",
    )
    print(f"Plot saved successfully to {output_path.resolve()}")


if __name__ == "__main__":
    main()
