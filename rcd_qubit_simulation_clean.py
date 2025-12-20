# -*- coding: utf-8 -*-
"""
RCD Quantum Error Correction Simulation
========================================
Comparison: Standard qubit decoherence vs. Coherential geometry-protected qubit

This script demonstrates the core prediction of RCD applied to quantum computing:
Qubits coupled to coherential geometry exhibit slower decoherence than 
isolated qubits relying on brute redundancy.

Author: Arturo Cerezo Garcia
ORCID: 0009-0007-4739-4990
Framework: Radial Coherential Dynamics (RCD)
License: Apache 2.0
Repository: https://doi.org/10.5281/zenodo.XXXXXXX (update after upload)
"""

import numpy as np
import matplotlib.pyplot as plt
from qutip import *

# =============================================================================
# PHYSICAL PARAMETERS
# =============================================================================

# RCD universal parameter
alpha = 1.3e-4  # Coherential coupling constant

# Simulation parameters
T_max = 50.0      # Total simulation time (arbitrary units)
n_steps = 500     # Number of time steps
times = np.linspace(0, T_max, n_steps)

# Qubit parameters
omega = 1.0       # Qubit frequency

# Decoherence rates
gamma_standard = 0.1                    # Standard T2 decay rate
gamma_coherential = gamma_standard * np.sqrt(alpha)  # RCD-suppressed rate
# Note: sqrt(alpha) = 0.0114 -> ~98.9% reduction in decoherence rate

print("=" * 60)
print("RCD QUBIT DECOHERENCE SIMULATION")
print("=" * 60)
print(f"RCD parameter alpha = {alpha}")
print(f"Standard decoherence rate gamma_0 = {gamma_standard}")
print(f"Coherential decoherence rate gamma_RCD = gamma_0 * sqrt(alpha) = {gamma_coherential:.6f}")
print(f"Suppression factor: {gamma_standard/gamma_coherential:.1f}x")
print("=" * 60)

# =============================================================================
# QUANTUM SYSTEM SETUP
# =============================================================================

# Basis states
psi0 = (basis(2, 0) + basis(2, 1)).unit()  # Initial state: |+> = (|0> + |1>)/sqrt(2)

# Hamiltonian (free precession)
H = omega * sigmaz() / 2

# Collapse operators for dephasing (T2 process)
c_ops_standard = [np.sqrt(gamma_standard) * sigmaz()]
c_ops_coherential = [np.sqrt(gamma_coherential) * sigmaz()]

# Observable: off-diagonal coherence (|<0|rho|1>|)
# We'll track the expectation value of sigma_x which measures coherence
observable = sigmax()

# =============================================================================
# MASTER EQUATION SIMULATION
# =============================================================================

print("\nRunning simulations...")

# Standard qubit evolution
result_standard = mesolve(H, psi0, times, c_ops_standard, [observable])
coherence_standard = np.abs(result_standard.expect[0])

# Coherential (RCD) qubit evolution
result_coherential = mesolve(H, psi0, times, c_ops_coherential, [observable])
coherence_coherential = np.abs(result_coherential.expect[0])

print("Simulations complete!")

# =============================================================================
# THEORETICAL PREDICTIONS (for comparison)
# =============================================================================

# Analytical exponential decay envelope
coherence_theory_standard = np.exp(-gamma_standard * times)
coherence_theory_coherential = np.exp(-gamma_coherential * times)

# =============================================================================
# VISUALIZATION
# =============================================================================

# Create figure with professional styling
fig, ax = plt.subplots(figsize=(10, 7), dpi=150)

# Plot simulation results
ax.plot(times, coherence_standard, 'r-', linewidth=2.5, 
        label=f'Standard Qubit (gamma = {gamma_standard})', alpha=0.9)
ax.plot(times, coherence_coherential, 'b-', linewidth=2.5,
        label=f'RCD Coherential Qubit (gamma = gamma_0*sqrt(alpha) = {gamma_coherential:.4f})', alpha=0.9)

# Plot theoretical curves (dashed)
ax.plot(times, coherence_theory_standard, 'r--', linewidth=1.5, alpha=0.5,
        label='Theory: exp(-gamma_0*t)')
ax.plot(times, coherence_theory_coherential, 'b--', linewidth=1.5, alpha=0.5,
        label='Theory: exp(-gamma_0*sqrt(alpha)*t)')

# Mark characteristic times
T2_standard = 1/gamma_standard
T2_coherential = 1/gamma_coherential

ax.axvline(x=T2_standard, color='red', linestyle=':', alpha=0.7)
ax.axvline(x=T2_coherential, color='blue', linestyle=':', alpha=0.7)

ax.annotate(f'T2 = {T2_standard:.1f}', xy=(T2_standard, 0.37), 
            xytext=(T2_standard + 2, 0.45), fontsize=10, color='red',
            arrowprops=dict(arrowstyle='->', color='red', alpha=0.7))

ax.annotate(f'T2(RCD) = {T2_coherential:.1f}', xy=(T2_coherential, 0.37),
            xytext=(T2_coherential - 25, 0.5), fontsize=10, color='blue',
            arrowprops=dict(arrowstyle='->', color='blue', alpha=0.7))

# Styling
ax.set_xlabel('Time (arbitrary units)', fontsize=12)
ax.set_ylabel('Coherence |<sigma_x>|', fontsize=12)
ax.set_title('Decoherence Suppression via Coherential Geometry\n' + 
             f'RCD Parameter alpha = {alpha}, Suppression Factor = {gamma_standard/gamma_coherential:.1f}x',
             fontsize=14, fontweight='bold')

ax.legend(loc='upper right', fontsize=10, framealpha=0.95)
ax.set_xlim(0, T_max)
ax.set_ylim(0, 1.05)
ax.grid(True, alpha=0.3)

# Add RCD attribution
ax.text(0.02, 0.02, 'Radial Coherential Dynamics (RCD)\nCerezo Garcia, A. (2025)',
        transform=ax.transAxes, fontsize=9, verticalalignment='bottom',
        style='italic', alpha=0.7)

plt.tight_layout()

# Save figure
output_path = 'rcd_decoherence_comparison.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\nFigure saved to: {output_path}")

# Also save high-res version for paper
output_path_hires = 'rcd_decoherence_comparison_hires.png'
plt.savefig(output_path_hires, dpi=600, bbox_inches='tight', facecolor='white')
print(f"High-res version saved to: {output_path_hires}")

plt.show()

# =============================================================================
# QUANTITATIVE RESULTS
# =============================================================================

print("\n" + "=" * 60)
print("QUANTITATIVE RESULTS")
print("=" * 60)

# Calculate time to reach 50% coherence (T2*)
idx_50_std = np.argmin(np.abs(coherence_standard - 0.5))
idx_50_rcd = np.argmin(np.abs(coherence_coherential - 0.5))

print(f"\nTime to 50% coherence:")
print(f"  Standard qubit:    T2* = {times[idx_50_std]:.2f}")
print(f"  RCD qubit:         T2* = {times[idx_50_rcd]:.2f}")
print(f"  Improvement:       {times[idx_50_rcd]/times[idx_50_std]:.1f}x longer coherence time")

# Calculate time to reach 1/e coherence
idx_e_std = np.argmin(np.abs(coherence_standard - 1/np.e))
idx_e_rcd = np.argmin(np.abs(coherence_coherential - 1/np.e))

print(f"\nTime to 1/e coherence (characteristic T2):")
print(f"  Standard qubit:    T2 = {times[idx_e_std]:.2f}")
print(f"  RCD qubit:         T2 = {times[idx_e_rcd]:.2f}")
print(f"  Improvement:       {times[idx_e_rcd]/times[idx_e_std]:.1f}x longer coherence time")

# Coherence remaining at fixed time
t_check = 20.0
idx_check = np.argmin(np.abs(times - t_check))

print(f"\nCoherence remaining at t = {t_check}:")
print(f"  Standard qubit:    {coherence_standard[idx_check]*100:.1f}%")
print(f"  RCD qubit:         {coherence_coherential[idx_check]*100:.1f}%")

print("\n" + "=" * 60)
print("KEY PREDICTION FOR PAPER")
print("=" * 60)
print(f"""
RCD predicts that qubits coupled to coherential geometry
exhibit decoherence rates suppressed by factor sqrt(alpha) = 1.14%.

For a standard qubit with T2 = 10 us:
  -> RCD-protected qubit: T2(RCD) = {10/np.sqrt(alpha):.0f} us

This is a FALSIFIABLE PREDICTION testable with current
trapped-ion or superconducting qubit hardware.
""")
print("=" * 60)
