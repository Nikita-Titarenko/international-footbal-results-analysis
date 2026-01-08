import os
import textwrap

import seaborn as sns
import matplotlib.pyplot as plt

plot_dir = 'plots'

def build_barplot(x, y, xlabel, ylabel, title):
    f = plt.figure(figsize=(12, 6))
    x_wrapped = [textwrap.fill(name, width=10) for name in x]
    axes = sns.barplot(x=x_wrapped, y=y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    for i, v in enumerate(y):
            axes.text(i, v + max(y)*0.01, f"{v:.1f}" if isinstance(v, float) else str(v), 
                    ha='center', va='bottom', fontweight='bold')
    save_figure(f, title)
    plt.close(f)
    

def build_plot(x, y, xlabel, ylabel, title):
    f, axes = plt.subplots()
    axes.set_xlabel(xlabel)
    axes.set_ylabel(ylabel)
    axes.set_title(title)
    axes.plot(x, y)
    save_figure(f, title)
    plt.close(f)

def save_figure(f, title):
    f.savefig(os.path.join(plot_dir, f'{title.lower().replace(' ', '_')}.png'))