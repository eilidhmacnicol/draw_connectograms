"""Command Line Interface."""
from pathlib import Path

def get_parser():
    """Build parser object."""
    from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

    parser = ArgumentParser(
        description="""\
draw_connectograms -- a command line tool to draw connectogram \
visualisations of symmetric adjacency matrices.\
""",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "input",
        action="store",
        type=Path,
        help="Path to the matrix CSV file",
    )
    parser.add_argument(
        "--node-labels",
        action="store",
        type=Path,
        default=None,
        help="Path to alternative node labels",
    )
    threshold = parser.add_mutually_exclusive_group()
    threshold.add_argument(
        "--prop-threshold",
        action="store",
        type=int,
        default=None,
        help="Proportional threshold to apply for top n percent of connections",
    )
    threshold.add_argument(
        "--abs-threshold",
        action="store",
        type=float,
        default=None,
        help="Absolute threshold to apply for absolute connection strength",
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        type=Path,
        default=Path("results").absolute(),
        help="Path where results should be stored",
    )
    return parser


def main():
    """Entry point."""
    from .viz import draw_connectogram

    opts = get_parser().parse_args()

    if not opts.node_labels:
        package_directory = Path(__file__).parent.absolute()
        node_labels = Path(
            package_directory, "data", "atlas-VHandWHS_desc-DC2_labels.csv"
        )
    else:
        node_labels = Path(opts.node_labels).absolute().resolve()

    if opts.prop_threshold:
        if 1 <= opts.prop_threshold < 100:
            threshold = ('proportional', opts.prop_threshold)
        else:
            raise ValueError("Proportional value must be an integer between 1 and 99")
    elif opts.abs_threshold:
        threshold = ('absolute', opts.abs_threshold)
    else:
        threshold = None

    connectogram = draw_connectogram(
        mat_file = opts.input,
        node_labels = node_labels,
        threshold = threshold
    )

    out_dir = Path.cwd() if not opts.output else opts.output
    connectogram.savefig(Path(out_dir,'connectogram.svg'),  format='svg')

if __name__ == "__main__":
    raise RuntimeError(
        """\
draw_connectograms/cli.py should not be run directly;
Please `pip install` draw_connectograms and use the `draw_connectogram` command."""
    )