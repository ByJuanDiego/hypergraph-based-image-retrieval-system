from typing import List
import matplotlib.pyplot as plt


def show_distances(
        distances: List[float],
        num_bins: int = 100
) -> None:

    plt.hist(
        x=distances,
        bins=num_bins,
        color='blue',
        alpha=0.7,
        cumulative=1,
        density=True
    )

    plt.show()
