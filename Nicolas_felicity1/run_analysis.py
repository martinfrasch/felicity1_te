#!/usr/bin/env python3
"""
Main entry point for the maternal-fetal entropy analysis.

This script runs the complete analysis pipeline:
1. Load and merge data from entropy_rate.txt, SampEn.txt, and outcomes Excel file
2. Compute correlations between features and biomarkers
3. Generate visualizations

Usage:
    python run_analysis.py [--analysis-only] [--plots-only]

Options:
    --analysis-only    Run only statistical analysis
    --plots-only       Generate only plots (requires previous analysis run)
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


def main():
    parser = argparse.ArgumentParser(description='Run maternal-fetal entropy analysis')
    parser.add_argument('--analysis-only', action='store_true',
                        help='Run only statistical analysis')
    parser.add_argument('--plots-only', action='store_true',
                        help='Generate only plots')
    args = parser.parse_args()

    if args.plots_only:
        from visualization import main as vis_main
        vis_main()
    elif args.analysis_only:
        from analysis import main as analysis_main
        analysis_main()
    else:
        # Run both
        print("=" * 70)
        print("MATERNAL-FETAL ENTROPY ANALYSIS")
        print("Replicating Section 3.4: TE in relation to other biomarkers")
        print("=" * 70)

        print("\n\n" + "=" * 70)
        print("PART 1: STATISTICAL ANALYSIS")
        print("=" * 70 + "\n")

        from analysis import main as analysis_main
        analysis_main()

        print("\n\n" + "=" * 70)
        print("PART 2: VISUALIZATIONS")
        print("=" * 70 + "\n")

        from visualization import main as vis_main
        vis_main()

        print("\n\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)
        print("\nOutput files:")
        output_dir = Path(__file__).parent / 'output'
        for f in sorted(output_dir.iterdir()):
            print(f"  - {f.name}")


if __name__ == '__main__':
    main()
