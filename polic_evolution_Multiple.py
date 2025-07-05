import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from data_npy_io import load_test_matrix_npy

# Configuration
users = 100
tests_to_plot = 100  # first 100 tests
slots = [250, 225, 200, 160, 75, 62, 56, 50]
gains = [round(users/s,3) for s in slots]

# Methods: distinguish by linestyle/marker
methods = {
    'IL':  {'base_dir': Path(r"E:/IL_U100"),  'linestyle':'--', 'marker':'s'},
    'JAL': {'base_dir': Path(r"C:\Users\Tauseef\OneDrive - Politecnico di Bari\AOI Q learning Paper\Data July\JAL_U100"), 'linestyle':'-',  'marker':'o'}
}

# Precompute distinct bright colors for each action
cmap = plt.get_cmap('tab10')

# Helper to compute action probabilities
def compute_action_probs(AC, actions):
    num_tests = AC.shape[0]
    probs = np.zeros((num_tests, len(actions)))
    for t in range(num_tests):
        flat = AC[t].flatten()
        for i,a in enumerate(actions):
            probs[t,i] = np.mean(flat==a)
    return probs

# Main plotting function
def plot_policy_evolution(save_dir, filename):
    os.makedirs(save_dir, exist_ok=True)
    fig, axes = plt.subplots(2,4,figsize=(16,8),dpi=600,sharey=True)

    # Determine full action set
    seen = []
    for name,cfg in methods.items():
        for s in slots:
            folder = cfg['base_dir']/f"{name}_S_{s}_U_{users}_c"
            AC = load_test_matrix_npy("AC_user_tests", str(folder))[:tests_to_plot,:,:]
            seen.append(np.unique(AC))
    all_actions = np.sort(np.unique(np.concatenate(seen)))
    all_actions = all_actions[all_actions>=0].astype(int)
    num_actions = len(all_actions)
    action_colors = cmap(np.linspace(0,1,num_actions))

    for idx,(g,s) in enumerate(zip(gains,slots)):
        ax = axes.flat[idx]
        for name,cfg in methods.items():
            folder = cfg['base_dir']/f"{name}_S_{s}_U_{users}_c"
            AC = load_test_matrix_npy("AC_user_tests", str(folder))[:tests_to_plot,:,:]
            probs = compute_action_probs(AC, all_actions)
            x = np.arange(tests_to_plot)
            for i,a in enumerate(all_actions):
                ax.plot(x, probs[:,i],
                        linestyle=cfg['linestyle'],
                        marker=cfg['marker'], markevery=10,
                        color=action_colors[i],
                        label=f"Action {a}" if name=='IL' else None,
                        alpha=0.8)
        # subplot annotations
        ax.set_title(f"G={g}",fontsize=12,fontweight='bold')
        if idx%4==0:
            ax.set_ylabel('P(action)',fontsize=12,fontweight='bold')
        if idx//4==1:
            ax.set_xlabel('Test Index',fontsize=12,fontweight='bold')
        ax.grid(True,linestyle='--',alpha=0.4)
        # legend: show actions and method shapes
        handles,labels = ax.get_legend_handles_labels()
        # add method handles
        for name,cfg in methods.items():
            h, = ax.plot([],[],
                         linestyle=cfg['linestyle'],marker=cfg['marker'],
                         color='k',label=name)
            handles.append(h); labels.append(name)
        ax.legend(handles,labels,fontsize=8,loc='upper right',ncol=2,frameon=False)
        # ticks bold
        ax.tick_params(axis='both',labelsize=11,width=1.5,length=6)
        for lbl in ax.get_xticklabels()+ax.get_yticklabels(): lbl.set_fontweight('bold')

    fig.suptitle('Policy Evolution: Action Probabilities for IL & JAL',fontsize=14,fontweight='bold')
    plt.tight_layout(rect=(0,0.03,1,0.95))
    out = Path(save_dir)/filename
    fig.savefig(out,format='pdf')
    plt.show()
    print(f"Saved to {out}")

if __name__=='__main__':
    plot_policy_evolution('PolicyPlots_U100', 'policy_evolution_IL_JAL_U100.pdf')
