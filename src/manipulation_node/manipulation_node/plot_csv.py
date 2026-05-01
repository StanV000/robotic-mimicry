import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import numpy as np
import psutil

# ── Load pose data ────────────────────────────────────────────────────────────
t, cmd_sh, act_sh, cmd_el, act_el = [], [], [], [], []

with open("45_to_45.csv", 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        t.append(float(row[0]))
        cmd_sh.append(float(row[1]))
        act_sh.append(float(row[2]))
        cmd_el.append(float(row[5]))
        act_el.append(float(row[6]))

t      = np.array(t)
cmd_sh = np.array(cmd_sh)
act_sh = np.array(act_sh)
cmd_el = np.array(cmd_el)
act_el = np.array(act_el)

mask   = t <= 10
t      = t[mask]
cmd_sh = cmd_sh[mask]
act_sh = act_sh[mask]
cmd_el = cmd_el[mask]
act_el = act_el[mask]

sh_err_deg = np.degrees(act_sh - cmd_sh)
el_err_deg = np.degrees(act_el - cmd_el)

sh_mae = np.mean(np.abs(sh_err_deg))
el_mae = np.mean(np.abs(el_err_deg))
sh_max = np.max(np.abs(sh_err_deg))
el_max = np.max(np.abs(el_err_deg))
sh_std = np.std(sh_err_deg)
el_std = np.std(el_err_deg)

print(f"\n{'='*50}")
print(f"  45° Pose")
print(f"{'='*50}")
print(f"  Shoulder — MAE: {sh_mae:.3f}°  Max: {sh_max:.3f}°  Std: {sh_std:.3f}°")
print(f"  Elbow    — MAE: {el_mae:.3f}°  Max: {el_max:.3f}°  Std: {el_std:.3f}°")

# ── Load CPU data ─────────────────────────────────────────────────────────────
cpu_t, cpu_vals = [], []

with open("45_to_45_cpu.csv", 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cpu_t.append(float(row[0]))
        cpu_vals.append(float(row[1]))

cpu_t    = np.array(cpu_t)
cpu_vals = np.array(cpu_vals) / psutil.cpu_count()  # Normalise to 0–100%

cpu_mean = np.mean(cpu_vals)
cpu_peak = np.max(cpu_vals)

print(f"  CPU     — Mean: {cpu_mean:.1f}%  Peak: {cpu_peak:.1f}%")

# ════════════════════════════════════════════════════════════════════════════
# Figure 1 — Joint tracking
# ════════════════════════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(14, 9))
fig1.suptitle("45° Pose — Joint Tracking", fontsize=14, fontweight='bold', y=0.98)
gs1 = gridspec.GridSpec(2, 2, figure=fig1, hspace=0.45, wspace=0.35)

# ── Shoulder: command vs actual ───────────────────────────────────────────────
ax1 = fig1.add_subplot(gs1[0, 0])
ax1.plot(t, cmd_sh, color='#378ADD', linewidth=2, linestyle='--', label='Commanded')
ax1.plot(t, act_sh, color='#D85A30', linewidth=2, label='Actual')
ax1.fill_between(t, cmd_sh, act_sh, alpha=0.12, color='#D85A30')
ax1.set_ylim(-np.pi/2, np.pi/2)
ax1.set_title('Shoulder — command vs actual', fontsize=11)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Angle (rad)')
ax1.legend(fontsize=9)
ax1.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

# ── Elbow: command vs actual ──────────────────────────────────────────────────
ax2 = fig1.add_subplot(gs1[0, 1])
ax2.plot(t, cmd_el, color='#378ADD', linewidth=2, linestyle='--', label='Commanded')
ax2.plot(t, act_el, color='#1D9E75', linewidth=2, label='Actual')
ax2.fill_between(t, cmd_el, act_el, alpha=0.12, color='#1D9E75')
ax2.set_ylim(-np.pi/2, np.pi/2)
ax2.set_title('Elbow — command vs actual', fontsize=11)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Angle (rad)')
ax2.legend(fontsize=9)
ax2.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

# ── Shoulder error ────────────────────────────────────────────────────────────
ax3 = fig1.add_subplot(gs1[1, 0])
ax3.plot(t, sh_err_deg, color='#D85A30', linewidth=1.5)
ax3.fill_between(t, sh_err_deg, alpha=0.15, color='#D85A30')
ax3.axhline(0, color='black', linewidth=0.8, linestyle='-')
ax3.axhline( sh_mae, color='#D85A30', linewidth=1, linestyle=':', label=f'MAE = {sh_mae:.3f}°')
ax3.axhline(-sh_mae, color='#D85A30', linewidth=1, linestyle=':')
ax3.set_title('Shoulder tracking error', fontsize=11)
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Error (deg)')
ax3.legend(fontsize=9)
ax3.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

# ── Elbow error ───────────────────────────────────────────────────────────────
ax4 = fig1.add_subplot(gs1[1, 1])
ax4.plot(t, el_err_deg, color='#1D9E75', linewidth=1.5)
ax4.fill_between(t, el_err_deg, alpha=0.15, color='#1D9E75')
ax4.axhline(0, color='black', linewidth=0.8, linestyle='-')
ax4.axhline( el_mae, color='#1D9E75', linewidth=1, linestyle=':', label=f'MAE = {el_mae:.3f}°')
ax4.axhline(-el_mae, color='#1D9E75', linewidth=1, linestyle=':')
ax4.set_title('Elbow tracking error', fontsize=11)
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Error (deg)')
ax4.legend(fontsize=9)
ax4.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

fig1.savefig("45_to_45_joints.png", dpi=150, bbox_inches='tight')

# ════════════════════════════════════════════════════════════════════════════
# Figure 2 — CPU usage
# ════════════════════════════════════════════════════════════════════════════
fig2, ax5 = plt.subplots(figsize=(12, 4))
fig2.suptitle("45° Pose — Node CPU Usage", fontsize=14, fontweight='bold')

ax5.plot(cpu_t, cpu_vals, color='#7B2D8B', linewidth=2)
ax5.fill_between(cpu_t, cpu_vals, alpha=0.2, color='#7B2D8B')
ax5.axhline(cpu_mean, color='#7B2D8B', linewidth=1, linestyle=':', label=f'Mean = {cpu_mean:.1f}%')
ax5.set_xlabel('Time (s)')
ax5.set_ylabel('CPU (%)')
ax5.set_xlim(cpu_t[0], cpu_t[-1])
ax5.set_ylim(0, 100)
ax5.legend(fontsize=9)
ax5.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

fig2.tight_layout()
fig2.savefig("45_to_45_cpu.png", dpi=150, bbox_inches='tight')

plt.show()