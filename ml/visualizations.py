"""
Visualization Module
Demonstrates: Matplotlib and Seaborn visualizations.
Generates charts as image files for the web dashboard.
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from config import CHARTS_FOLDER

# ── Global style ──
plt.rcParams.update({
    'figure.facecolor': '#0f0f23',
    'axes.facecolor': '#1a1a3e',
    'axes.edgecolor': '#333366',
    'axes.labelcolor': '#e0e0ff',
    'text.color': '#e0e0ff',
    'xtick.color': '#b0b0d0',
    'ytick.color': '#b0b0d0',
    'grid.color': '#252555',
    'grid.alpha': 0.5,
    'font.size': 11,
    'font.family': 'sans-serif',
})

COLORS = ['#6C63FF', '#00D4FF', '#FF6B9D', '#FFD93D', '#6BCB77',
          '#4D96FF', '#FF6B6B', '#C084FC', '#34D399', '#FB923C']
GRADIENT = ['#6C63FF', '#7C73FF', '#8C83FF', '#9C93FF', '#ACA3FF']


def ensure_charts_dir():
    os.makedirs(CHARTS_FOLDER, exist_ok=True)


# ════════════════════════════════════════════
#  MATPLOTLIB CHARTS
# ════════════════════════════════════════════

def plot_role_probabilities(roles, probabilities, filename='role_probabilities.png'):
    """Bar Chart: Job role prediction probabilities."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 6))

    bars = ax.barh(roles, probabilities, color=COLORS[:len(roles)],
                   edgecolor='white', linewidth=0.5, height=0.6)

    for bar, prob in zip(bars, probabilities):
        ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'{prob:.1f}%', va='center', fontsize=11, fontweight='bold', color='#e0e0ff')

    ax.set_xlabel('Probability (%)', fontsize=13)
    ax.set_title('Job Role Prediction Probabilities', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlim(0, max(probabilities) * 1.2)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_skill_distribution(skills_dict, filename='skill_distribution.png'):
    """Pie Chart: Distribution of skills by category."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(9, 9))

    categories = list(skills_dict.keys())
    counts = [len(v) for v in skills_dict.values()]

    wedges, texts, autotexts = ax.pie(
        counts, labels=categories, colors=COLORS[:len(categories)],
        autopct='%1.1f%%', startangle=140, pctdistance=0.8,
        wedgeprops=dict(width=0.5, edgecolor='#0f0f23', linewidth=2)
    )
    for text in texts + autotexts:
        text.set_fontsize(10)
        text.set_color('#e0e0ff')

    ax.set_title('Skill Distribution by Category', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_experience_vs_score(experience, scores, filename='exp_vs_score.png'):
    """Line Graph: Experience vs matching score."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 6))

    sorted_pairs = sorted(zip(experience, scores))
    exp_sorted = [p[0] for p in sorted_pairs]
    score_sorted = [p[1] for p in sorted_pairs]

    ax.plot(exp_sorted, score_sorted, color='#6C63FF', linewidth=2.5,
            marker='o', markersize=8, markerfacecolor='#00D4FF',
            markeredgecolor='white', markeredgewidth=1.5)
    ax.fill_between(exp_sorted, score_sorted, alpha=0.15, color='#6C63FF')

    ax.set_xlabel('Years of Experience', fontsize=13)
    ax.set_ylabel('Matching Score (%)', fontsize=13)
    ax.set_title('Experience vs Matching Score', fontsize=16, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_skill_vs_role_scatter(skill_counts, role_scores, categories,
                               filename='skill_vs_role.png'):
    """Scatter Plot: Skill count vs role score colored by category."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 7))

    unique_cats = list(set(categories))
    color_map = {cat: COLORS[i % len(COLORS)] for i, cat in enumerate(unique_cats)}

    for cat in unique_cats:
        mask = [c == cat for c in categories]
        sc = [s for s, m in zip(skill_counts, mask) if m]
        rs = [r for r, m in zip(role_scores, mask) if m]
        ax.scatter(sc, rs, c=color_map[cat], label=cat, s=60, alpha=0.7, edgecolors='white')

    ax.set_xlabel('Skill Count', fontsize=13)
    ax.set_ylabel('Role Score (%)', fontsize=13)
    ax.set_title('Skill Count vs Role Score', fontsize=16, fontweight='bold', pad=15)
    ax.legend(fontsize=8, loc='lower right', framealpha=0.5)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_category_distribution(df, filename='category_distribution.png'):
    """Bar chart showing resume count per job category."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(12, 6))

    counts = df['job_category'].value_counts()
    bars = ax.bar(range(len(counts)), counts.values, color=COLORS[:len(counts)],
                  edgecolor='white', linewidth=0.5)

    ax.set_xticks(range(len(counts)))
    ax.set_xticklabels(counts.index, rotation=45, ha='right', fontsize=9)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title('Resume Distribution by Job Category', fontsize=16, fontweight='bold', pad=15)

    for bar, val in zip(bars, counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                str(val), ha='center', fontsize=10, fontweight='bold', color='#e0e0ff')

    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


# ════════════════════════════════════════════
#  SEABORN CHARTS
# ════════════════════════════════════════════

def plot_correlation_heatmap(df, filename='correlation_heatmap.png'):
    """Seaborn Heatmap: Feature correlations."""
    ensure_charts_dir()
    numeric_cols = ['years_of_experience', 'gpa', 'skill_count', 'projects_count',
                    'cert_count', 'education_encoded', 'salary_lpa', 'lang_count']
    cols_present = [c for c in numeric_cols if c in df.columns]
    corr = df[cols_present].corr()

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, linewidths=0.5,
                fmt='.2f', ax=ax, square=True,
                annot_kws={'size': 10, 'color': '#e0e0ff'},
                cbar_kws={'label': 'Correlation'})
    ax.set_title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', pad=15)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_pairplot(df, filename='pairplot.png'):
    """Seaborn Pairplot: Encoded feature relationships."""
    ensure_charts_dir()
    cols = ['years_of_experience', 'skill_count', 'gpa', 'projects_count']
    cols_present = [c for c in cols if c in df.columns]

    sample = df[cols_present + ['job_category']].sample(n=min(200, len(df)), random_state=42)
    top_cats = sample['job_category'].value_counts().head(4).index.tolist()
    sample = sample[sample['job_category'].isin(top_cats)]

    with plt.rc_context({'figure.facecolor': '#0f0f23', 'axes.facecolor': '#1a1a3e'}):
        g = sns.pairplot(sample, hue='job_category', palette=COLORS[:len(top_cats)],
                         diag_kind='kde', height=2.5, plot_kws={'alpha': 0.6, 's': 30})
        g.figure.suptitle('Feature Pairplot', fontsize=16, fontweight='bold', y=1.02)

    path = os.path.join(CHARTS_FOLDER, filename)
    g.savefig(path, dpi=120, bbox_inches='tight')
    plt.close('all')
    return filename


def plot_violin(df, filename='violin_plot.png'):
    """Seaborn Violin Plot: Experience distribution by role."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(14, 7))

    top_cats = df['job_category'].value_counts().head(6).index.tolist()
    subset = df[df['job_category'].isin(top_cats)]

    sns.violinplot(data=subset, x='job_category', y='years_of_experience',
                   palette=COLORS[:len(top_cats)], ax=ax, inner='box', linewidth=1)

    ax.set_xlabel('Job Category', fontsize=13)
    ax.set_ylabel('Years of Experience', fontsize=13)
    ax.set_title('Experience Distribution by Role', fontsize=16, fontweight='bold', pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha='right', fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_experience_histogram(df, filename='experience_histogram.png'):
    """Seaborn Histogram: Experience level distribution."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.histplot(data=df, x='years_of_experience', hue='education_level',
                 multiple='stack', palette=COLORS[:4], ax=ax,
                 bins=15, edgecolor='white', linewidth=0.5)

    ax.set_xlabel('Years of Experience', fontsize=13)
    ax.set_ylabel('Count', fontsize=13)
    ax.set_title('Experience Level Distribution', fontsize=16, fontweight='bold', pad=15)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_clusters(df, filename='cluster_visualization.png'):
    """Scatter plot of K-Means clusters (PCA-reduced)."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 8))

    cluster_colors = {'Beginner': '#FF6B6B', 'Intermediate': '#FFD93D', 'Advanced': '#6BCB77'}

    for label, color in cluster_colors.items():
        mask = df['cluster_label'] == label
        ax.scatter(df.loc[mask, 'pca_x'], df.loc[mask, 'pca_y'],
                   c=color, label=label, s=50, alpha=0.7, edgecolors='white', linewidth=0.5)

    ax.set_xlabel('PCA Component 1', fontsize=13)
    ax.set_ylabel('PCA Component 2', fontsize=13)
    ax.set_title('Resume Clusters (K-Means)', fontsize=16, fontweight='bold', pad=15)
    ax.legend(fontsize=12, framealpha=0.5)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_model_comparison(metrics, filename='model_comparison.png'):
    """Bar chart comparing model metrics."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(12, 6))

    models = list(metrics.keys())
    metric_names = ['accuracy', 'precision', 'recall', 'f1_score']
    x = np.arange(len(models))
    width = 0.18

    for i, metric in enumerate(metric_names):
        values = [metrics[m][metric] for m in models]
        bars = ax.bar(x + i * width, values, width, label=metric.replace('_', ' ').title(),
                      color=COLORS[i], edgecolor='white', linewidth=0.5)

    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(models, fontsize=11)
    ax.set_ylabel('Score (%)', fontsize=13)
    ax.set_title('Model Performance Comparison', fontsize=16, fontweight='bold', pad=15)
    ax.legend(fontsize=10, framealpha=0.5)
    ax.set_ylim(0, 110)
    ax.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_confusion_matrix(cm, labels, filename='confusion_matrix.png'):
    """Seaborn heatmap of confusion matrix."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(12, 10))

    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels,
                yticklabels=labels, ax=ax, linewidths=0.5,
                annot_kws={'size': 9})

    ax.set_xlabel('Predicted', fontsize=13)
    ax.set_ylabel('Actual', fontsize=13)
    ax.set_title('Confusion Matrix (Best Model)', fontsize=16, fontweight='bold', pad=15)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right', fontsize=8)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=8)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_feature_importance(importance_dict, filename='feature_importance.png'):
    """Horizontal bar chart of feature importances."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 6))

    features = list(importance_dict.keys())[:15]
    values = [importance_dict[f] for f in features]

    bars = ax.barh(features, values, color=COLORS[:len(features)],
                   edgecolor='white', linewidth=0.5, height=0.6)
    ax.set_xlabel('Importance', fontsize=13)
    ax.set_title('Feature Importance', fontsize=16, fontweight='bold', pad=15)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_elbow(k_range, inertias, silhouettes, filename='elbow_plot.png'):
    """Elbow method + Silhouette score plot."""
    ensure_charts_dir()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.plot(k_range, inertias, 'o-', color='#6C63FF', linewidth=2.5, markersize=8)
    ax1.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax1.set_ylabel('Inertia', fontsize=12)
    ax1.set_title('Elbow Method', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    ax2.plot(k_range, silhouettes, 'o-', color='#00D4FF', linewidth=2.5, markersize=8)
    ax2.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax2.set_ylabel('Silhouette Score', fontsize=12)
    ax2.set_title('Silhouette Analysis', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    fig.suptitle('Optimal Cluster Selection', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def plot_salary_estimation(min_sal, median_sal, max_sal, predicted_sal,
                           filename='salary_estimation.png'):
    """Salary range visualization."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(10, 3))

    ax.barh(['Salary Range'], [max_sal - min_sal], left=[min_sal],
            color='#1a1a3e', edgecolor='#6C63FF', linewidth=2, height=0.4)
    ax.barh(['Salary Range'], [0.5], left=[predicted_sal - 0.25],
            color='#FF6B9D', height=0.5, label=f'Your Estimate: {predicted_sal:.1f} LPA')
    ax.axvline(x=median_sal, color='#00D4FF', linewidth=2, linestyle='--',
               label=f'Market Median: {median_sal:.1f} LPA')

    ax.set_xlabel('Salary (LPA)', fontsize=13)
    ax.set_title('Salary Estimation', fontsize=16, fontweight='bold', pad=15)
    ax.legend(fontsize=10, loc='upper right')
    ax.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    return filename


def generate_all_dataset_charts(df):
    """Generate all dataset-level charts. Returns list of filenames."""
    charts = []
    charts.append(plot_category_distribution(df))
    charts.append(plot_correlation_heatmap(df))
    charts.append(plot_violin(df))
    charts.append(plot_experience_histogram(df))
    try:
        charts.append(plot_pairplot(df))
    except Exception:
        pass
    return charts
