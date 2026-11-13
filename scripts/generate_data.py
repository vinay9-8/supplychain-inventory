from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.generators.data_generator import DataGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate synthetic supply-chain datasets.")
    parser.add_argument("--mode", choices=["sample", "full"], default="full")
    parser.add_argument("--seed", type=int, default=20261022)
    parser.add_argument("--output-dir", type=str, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    root_dir = Path(args.output_dir).resolve() if args.output_dir else Path(__file__).resolve().parents[1]
    generator = DataGenerator(seed=args.seed, root_dir=root_dir)
    summary = generator.generate_dataset(mode=args.mode)

    print(f"Generated dataset in mode={args.mode} with seed={args.seed}")
    print(summary["counts"])


if __name__ == "__main__":
    main()
