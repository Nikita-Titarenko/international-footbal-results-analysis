import os
import textwrap

import seaborn as sns
import matplotlib.pyplot as plt

plot_dir = 'plots'

def add_titles(values, axes, orient='v'):
    offset = max(values) * 0.01
    
    for i, v in enumerate(values):
        display_text = f"{v:.1f}" if isinstance(v, float) else str(v)
        
        if orient == 'v':
            axes.text(i, v + offset, display_text, 
                      ha='center', va='bottom', fontweight='bold')
        else:
            axes.text(v + offset, i, display_text, 
                      ha='left', va='center', fontweight='bold')

def build_barplot(x, y, xlabel, ylabel, title, orient='v'):
    f = plt.figure(figsize=(12, 6))
    x_wrapped = x
    y_wrapped = y
    if orient == 'v':
         x_wrapped = [textwrap.fill(name, width=10) for name in x]
    if orient == 'h':
         y_wrapped = [textwrap.fill(name, width=10) for name in y]
    
    axes = sns.barplot(x=x_wrapped, y=y_wrapped, orient=orient)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    if orient == 'v':
             add_titles(y, axes, orient)
    if orient == 'h':
             add_titles(x, axes, orient)

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