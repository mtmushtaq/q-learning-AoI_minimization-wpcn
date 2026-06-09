# Distributed Q-Learning for Age of Information Optimization in Massive IoT

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-red)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-1.11%2B-orange)](https://scipy.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Paper](https://img.shields.io/badge/Paper-IEEE-blue)](https://arxiv.org/)

---

## Overview

This repository contains the full implementation of the framework presented in:

> **"Distributed Q-Learning for Age of Information Optimization:
> Energy-Aware, CSI-Aware IRSA with PD-NOMA and SIC Decoding"**
> Muhammad Tauseef Mushtaq
> Department of Electrical and Information Engineering,
> Politecnico di Bari, Bari, Italy

We propose a **model-free Q-learning framework** for distributed, energy-aware
random access in massive Machine-Type Communication (mMTC) networks.
The framework addresses the critical problem of maintaining **low Age of
Information (AoI)** under:

- **Non-linear energy harvesting** with finite battery capacity
- **Time-correlated Rician fading** with κ-factor awareness
- **CSI-aware power level selection** (PD-NOMA) with Successive Interference
  Cancellation (SIC)
- **Capture effect** enabling successful recovery from collisions
- **Decentralized decision-making** where each mMTC device adapts its
  transmission policy using only local state (battery, channel grade) and
  periodic broadcast feedback from the HAP

### Key Results

| Metric | Q-Learning (EEIL) | Greedy (Energy) | Random |
|--------|------------------|-----------------|--------|
| Avg AoI (M=10, N=5) | **~40 slots** | ~85 slots | ~120 slots |
| Avg AoI (M=15, N=5) | **~55 slots** | ~110 slots | ~150 slots |
| Avg Energy @ convergence (M=10) | **0.045 J** | 0.050 J | 0.065 J |
| Reward convergence | ✅ Stable after ~500 epochs | ❌ Suboptimal | ❌ No learning |

> **Key insight**: As power levels increase (k=2→5), Q-learning learns to
> use **fewer replicas** while maintaining lower AoI — demonstrating
> joint optimization of access diversity and energy efficiency.

---

## Key Features

- **Distributed Q-learning (EEIL)**: Each mMTC device independently learns
  an optimal policy mapping (battery, channel grade) → (num replicas, power level)
  without centralized coordination or model knowledge.

- **κ-factor-aware channel discretization**: Rician fading CDF is quantized
  into $V$ equally-probable bins, scaled by distance-dependent path loss —
  providing robust, CSI-efficient state representation.

- **Non-linear energy harvesting model**: Realistic WET conversion efficiency
  captured via nonlinear EH function with constants α₀=0.826, α₁=0.399.

- **Masked Q-learning with feasibility**: Only energy-feasible actions
  (replica count × power level) are considered in the Q-table update,
  eliminating infeasible state–action pairs.

- **REARLY-k slot-wise SIC decoding**: Greedy per-slot decoding (earliest
  first for low AoI) with immediate intra-slot and inter-slot interference
  Cancellation propagated in real-time.

- **Three-way AoI recovery**: Devices recover via (i) singleton slots,
  (ii) capture effect, or (iii) SIC after collisions — all modeled explicitly.

- **Composite reward balancing**: AoI minimization + energy efficiency
  via weighted reward $r = -w_a \cdot A_m(N) - w_E \cdot E_m$.

---

## 📂 Directory Structure

├── **Main Simulators/**  
│   Contains the core simulation code:  
│   • `pd_noma_q_learning.py` – your proposed PD-NOMA Q-learning algorithm  
│   • `greedy_baseline.py` – greedy access scheme for comparison  
│   • `random_baseline.py` – random access scheme for comparison  
│   • any other helper modules you call from these scripts  

├── **Results/**  
│   Stores all raw output from the simulators (e.g. `.csv`, `.mat`, `.json`)  
│   • per-run metrics, logs, traces, etc.  

├── **Comparison Plot Codes/**  
│   Contains scripts that read from `Results/` and generate the figures in the paper:  
│   • `plot_aoi_comparison.py`  
│   • `plot_energy_vs_age.py`  
│   • etc.  

├── **Extra PDF Plots/**  
│   High-resolution PDF versions of key plots for inclusion in slides/papers  

├── **Extra Data/**  
│   Any additional datasets or config files used by the simulators  


## Contact

**Muhammad Tauseef Mushtaq**
PhD, Department of Electrical and Information Engineering
Politecnico di Bari, Italy
📧 m.mushtaq@phd.poliba.it
🔗 https://www.linkedin.com/in/tauseef-mushtaq/
