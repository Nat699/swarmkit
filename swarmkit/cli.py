"""
Command-line interface for swarmkit.
"""
import argparse
import sys
from pathlib import Path


def cmd_build(args):
    """Build a corpus of windows from OMNI DST data."""
    from .fetch import load_omni_multi
    from .detect import detect_windows

    print(f"Downloading OMNI {args.years}...")
    anos = [int(y) for y in args.years.split("-")]
    omni = load_omni_multi(anos[0], anos[1])

    print(f"Detecting {args.state} windows...")
    windows = detect_windows(omni["dst"], args.state, min_dur_h=args.min_dur)
    print(f"  {len(windows)} windows detected")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    windows.to_csv(out, index=False)
    print(f"Saved to {out}")


def cmd_predict(args):
    """Classify a single .npz pass."""
    from .model import SamaClassifier
    import numpy as np

    clf = SamaClassifier.load(args.model)
    z = np.load(args.npz)
    if "F" not in z:
        print(f"Error: {args.npz} has no 'F' key", file=sys.stderr)
        sys.exit(1)
    p = clf.predict_proba(z["F"])
    print(f"p_sama = {p:.4f}")


def cmd_info(args):
    """Show version and available functions."""
    from . import __version__
    print(f"swarmkit {__version__}")
    print("Available functions: fetch_swarm_window, download_omni,")
    print("  detect_onsets, detect_windows, classify_period,")
    print("  extract_features, SamaClassifier")


def main():
    ap = argparse.ArgumentParser(
        prog="swarmkit",
        description="SAMA signature detection from Swarm magnetic field data",
    )
    sub = ap.add_subparsers(dest="cmd")

    p_build = sub.add_parser("build", help="build a corpus of windows")
    p_build.add_argument("--years", default="2015-2024",
                         help="year range, e.g. 2015-2024")
    p_build.add_argument("--state", default="storm",
                         choices=["calm", "moderate", "storm"])
    p_build.add_argument("--min-dur", type=int, default=24,
                         help="minimum window duration (hours)")
    p_build.add_argument("--out", default="corpus.csv")
    p_build.set_defaults(func=cmd_build)

    p_pred = sub.add_parser("predict", help="classify a pass")
    p_pred.add_argument("--npz", required=True)
    p_pred.add_argument("--model", required=True)
    p_pred.set_defaults(func=cmd_predict)

    p_info = sub.add_parser("info", help="show version and API")
    p_info.set_defaults(func=cmd_info)

    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == "__main__":
    main()
