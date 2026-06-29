import os
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
from config import CHARTS_FOLDER

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


def ensure_charts_dir():
    os.makedirs(CHARTS_FOLDER, exist_ok=True)


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
    ax.set_title('Job Role Prediction Probabilities', fontsize=18, fontweight='bold', pad=20)
    ax.set_xlim(0, max(probabilities) * 1.2)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    
    # Clean up spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', transparent=True)
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

    ax.set_title('Skill Distribution by Category', fontsize=18, fontweight='bold', pad=20)
    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)
    return filename


def plot_salary_estimation(min_sal, median_sal, max_sal, predicted_sal,
                           filename='salary_estimation.png'):
    """Salary range visualization."""
    ensure_charts_dir()
    fig, ax = plt.subplots(figsize=(9, 5))

    ax.barh(['Estimated Salary'], [max_sal - min_sal], left=[min_sal],
            color='#0d6efd', edgecolor='#0d6efd', linewidth=1, height=0.3, alpha=0.2, label='Market Range')
    
    ax.barh(['Estimated Salary'], [0.5], left=[predicted_sal - 0.25],
            color='#00e5ff', height=0.5, label=f'Your Estimate: {predicted_sal:.1f} LPA')
            
    ax.axvline(x=median_sal, color='#ffc107', linewidth=2, linestyle='--',
               label=f'Market Median: {median_sal:.1f} LPA')

    ax.set_xlabel('Salary (LPA)', fontsize=13)
    ax.set_title('Salary Estimation & Market Alignment', fontsize=18, fontweight='bold', pad=20)
    
    ax.legend(fontsize=11, loc='upper right', frameon=True, facecolor='#060b14', edgecolor='#333366', framealpha=0.8)
    
    ax.grid(axis='x', color='#333366', alpha=0.5, linestyle='--')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    plt.tight_layout()
    path = os.path.join(CHARTS_FOLDER, filename)
    fig.savefig(path, dpi=150, bbox_inches='tight', transparent=True)
    plt.close(fig)
    return filename
