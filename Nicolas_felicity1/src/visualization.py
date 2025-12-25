"""
Visualization module for entropy features analysis.

Creates plots similar to Section 3.4 of the manuscript:
- Correlation heatmaps
- Scatter plots with PSS/PDQ scores
- Feature distributions by group
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

from data_loader import merge_all_data, get_feature_names
from analysis import get_stress_group, ALL_OUTCOMES, compute_correlations


def setup_plotting():
    """Configure matplotlib for publication-quality figures."""
    plt.rcParams.update({
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 8,
        'ytick.labelsize': 8,
        'legend.fontsize': 8,
        'figure.figsize': (10, 8),
        'figure.dpi': 150,
    })


def create_correlation_heatmap(
    df: pd.DataFrame,
    feature_cols: list,
    outcome_cols: list,
    title: str,
    output_path: Path,
    method: str = 'auto'
):
    """
    Create a heatmap of correlations between features and outcomes.
    """
    corr_df = compute_correlations(df, feature_cols, outcome_cols, method)

    if corr_df.empty:
        print(f"No correlations to plot for {title}")
        return

    # Pivot for heatmap
    pivot = corr_df.pivot(index='feature', columns='outcome', values='r')
    p_pivot = corr_df.pivot(index='feature', columns='outcome', values='p_value')

    # Create heatmap
    fig, ax = plt.subplots(figsize=(12, 10))

    # Plot heatmap
    mask = np.isnan(pivot.values)
    sns.heatmap(
        pivot,
        annot=True,
        fmt='.2f',
        cmap='RdBu_r',
        center=0,
        vmin=-0.5,
        vmax=0.5,
        mask=mask,
        ax=ax,
        cbar_kws={'label': 'Spearman r'}
    )

    # Mark significant correlations
    for i in range(len(pivot)):
        for j in range(len(pivot.columns)):
            if not np.isnan(p_pivot.iloc[i, j]) and p_pivot.iloc[i, j] < 0.05:
                ax.text(
                    j + 0.5, i + 0.5, '*',
                    ha='center', va='center',
                    fontsize=14, color='black'
                )

    ax.set_title(f'{title}\n(* p < 0.05)')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def create_scatter_with_stress_scores(
    df: pd.DataFrame,
    feature_cols: list,
    output_dir: Path,
):
    """
    Create scatter plots of features vs PSS/PDQ scores.
    Similar to Figures 8 and 9 in the manuscript.
    """
    stress_cols = ['Mother Score_PSS', 'Mother Score PDQ']
    stress_cols = [c for c in stress_cols if c in df.columns]

    if not stress_cols:
        print("No stress score columns found")
        return

    # Select a subset of features for visualization
    feature_subset = [f for f in feature_cols if f in df.columns][:6]

    for stress_col in stress_cols:
        fig, axes = plt.subplots(2, 3, figsize=(14, 9))
        axes = axes.flatten()

        short_name = 'PSS' if 'PSS' in stress_col else 'PDQ'

        for idx, feature in enumerate(feature_subset):
            ax = axes[idx]

            x = pd.to_numeric(df[stress_col], errors='coerce')
            y = pd.to_numeric(df[feature], errors='coerce')

            mask = x.notna() & y.notna()
            x_valid = x[mask]
            y_valid = y[mask]

            if len(x_valid) < 5:
                ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center')
                continue

            # Get stress group for coloring
            stress_group = get_stress_group(df)
            colors = stress_group[mask].map({'stressed': 'red', 'control': 'blue'})

            ax.scatter(x_valid, y_valid, c=colors, alpha=0.6, s=30)

            # Add regression line
            r, p = stats.spearmanr(x_valid, y_valid)
            z = np.polyfit(x_valid, y_valid, 1)
            p_line = np.poly1d(z)
            x_line = np.linspace(x_valid.min(), x_valid.max(), 100)
            ax.plot(x_line, p_line(x_line), 'k--', alpha=0.5)

            # Simplify feature name for display
            feat_short = feature.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
            ax.set_xlabel(short_name)
            ax.set_ylabel(feat_short)
            ax.set_title(f'r={r:.2f}, p={p:.3f}')

        # Add legend
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Stressed'),
            Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Control'),
        ]
        fig.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(0.98, 0.98))

        fig.suptitle(f'Features vs {short_name} Score', fontsize=14)
        plt.tight_layout(rect=[0, 0, 1, 0.96])

        output_path = output_dir / f'scatter_{short_name.lower()}_scores.png'
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"Saved: {output_path}")


def create_boxplots_by_group(
    df: pd.DataFrame,
    feature_cols: list,
    group_col: str,
    output_path: Path,
):
    """
    Create boxplots of features by stress group.
    """
    feature_subset = [f for f in feature_cols if f in df.columns][:10]

    n_features = len(feature_subset)
    n_cols = 5
    n_rows = (n_features + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4 * n_rows))
    axes = axes.flatten()

    for idx, feature in enumerate(feature_subset):
        ax = axes[idx]

        data = df[[feature, group_col]].copy()
        data[feature] = pd.to_numeric(data[feature], errors='coerce')
        data = data.dropna()

        if len(data) < 5:
            ax.text(0.5, 0.5, 'Insufficient data', ha='center', va='center')
            continue

        sns.boxplot(data=data, x=group_col, y=feature, ax=ax, palette=['blue', 'red'])

        # Mann-Whitney test
        groups = data[group_col].unique()
        if len(groups) == 2:
            g1_data = data[data[group_col] == groups[0]][feature]
            g2_data = data[data[group_col] == groups[1]][feature]
            _, p = stats.mannwhitneyu(g1_data, g2_data, alternative='two-sided')
            ax.set_title(f'p={p:.3f}')

        # Simplify feature name
        feat_short = feature.replace('entropy_rate_', 'ER_').replace('sampen_', 'SE_')
        ax.set_ylabel(feat_short)
        ax.set_xlabel('')

    # Hide unused axes
    for idx in range(len(feature_subset), len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle(f'Feature Distributions by Stress Group', fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def create_outcome_correlation_summary(
    df: pd.DataFrame,
    feature_cols: list,
    output_path: Path,
):
    """
    Create summary plot of correlations with developmental outcomes.
    """
    outcome_cols = [
        'COG COMPOSITE SCORE',
        'LANG COMP SCORE',
        'MOTOR COMPOSITE SCORE',
    ]
    outcome_cols = [c for c in outcome_cols if c in df.columns]

    if not outcome_cols:
        print("No outcome columns found")
        return

    corr_df = compute_correlations(df, feature_cols, outcome_cols)

    if corr_df.empty:
        print("No correlations computed")
        return

    # Create bar plot of correlations
    fig, axes = plt.subplots(1, len(outcome_cols), figsize=(5 * len(outcome_cols), 8))
    if len(outcome_cols) == 1:
        axes = [axes]

    for ax, outcome in zip(axes, outcome_cols):
        subset = corr_df[corr_df['outcome'] == outcome].copy()
        subset = subset.sort_values('r')

        # Color by significance
        colors = ['red' if p < 0.05 else 'gray' for p in subset['p_value']]

        # Simplify feature names
        subset['feature_short'] = subset['feature'].str.replace(
            'entropy_rate_', 'ER_'
        ).str.replace('sampen_', 'SE_')

        ax.barh(subset['feature_short'], subset['r'], color=colors, alpha=0.7)
        ax.axvline(x=0, color='black', linewidth=0.5)
        ax.set_xlabel('Spearman r')
        ax.set_title(outcome.replace(' SCORE', ''))
        ax.set_xlim(-0.5, 0.5)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"Saved: {output_path}")


def main():
    """Generate all visualizations."""
    setup_plotting()

    data_dir = Path(__file__).parent.parent
    output_dir = data_dir / 'output'
    output_dir.mkdir(exist_ok=True)

    print("Loading data...")
    df = merge_all_data(data_dir)
    df['stress_group'] = get_stress_group(df)

    feature_cols = get_feature_names()
    available_features = [c for c in feature_cols if c in df.columns]

    print(f"\nGenerating visualizations...")

    # 1. Correlation heatmap - all subjects
    print("\n1. Correlation heatmap (all subjects)")
    outcome_cols = [c for c in ALL_OUTCOMES if c in df.columns]
    create_correlation_heatmap(
        df, available_features, outcome_cols,
        'Feature-Outcome Correlations (All Subjects)',
        output_dir / 'heatmap_correlations_all.png'
    )

    # 2. Correlation heatmap - by stress group
    print("\n2. Correlation heatmaps by stress group")
    for group in ['stressed', 'control']:
        group_df = df[df['stress_group'] == group]
        create_correlation_heatmap(
            group_df, available_features, outcome_cols,
            f'Feature-Outcome Correlations ({group.capitalize()})',
            output_dir / f'heatmap_correlations_{group}.png'
        )

    # 3. Scatter plots with stress scores
    print("\n3. Scatter plots with stress scores")
    create_scatter_with_stress_scores(df, available_features, output_dir)

    # 4. Boxplots by stress group
    print("\n4. Feature distributions by stress group")
    create_boxplots_by_group(
        df, available_features, 'stress_group',
        output_dir / 'boxplots_by_stress.png'
    )

    # 5. Outcome correlation summary
    print("\n5. Outcome correlation summary")
    create_outcome_correlation_summary(
        df, available_features,
        output_dir / 'outcome_correlations_summary.png'
    )

    print("\n" + "=" * 60)
    print("Visualizations complete. Files saved to output/")
    print("=" * 60)


if __name__ == '__main__':
    main()
