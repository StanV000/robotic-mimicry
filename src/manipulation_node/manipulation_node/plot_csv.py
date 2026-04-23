import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import csv
import numpy as np

files = [
    "horizontal_pose.csv",
    "upward_pose.csv",
    "45_degree_pose.csv"
]

labels = ["Horizontal Pose", "Upward Pose", "45° Pose"]

for file, label in zip(files, labels):
    t, cmd_sh, act_sh, cmd_el, act_el = [], [], [], [], []

    with open(file, 'r') as f:
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
    print(f"  {label}")
    print(f"{'='*50}")
    print(f"  Shoulder — MAE: {sh_mae:.3f}°  Max: {sh_max:.3f}°  Std: {sh_std:.3f}°")
    print(f"  Elbow    — MAE: {el_mae:.3f}°  Max: {el_max:.3f}°  Std: {el_std:.3f}°")

    fig = plt.figure(figsize=(14, 9))
    fig.suptitle(label, fontsize=14, fontweight='bold', y=0.98)

    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

    # ── Shoulder: command vs actual ──────────────────────────────────────────
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(cmd_sh, t, color='#378ADD', linewidth=2, linestyle='--', label='Commanded')
    ax1.plot(act_sh, t, color='#D85A30', linewidth=2, label='Actual')
    ax1.fill_betweenx(t, cmd_sh, act_sh, alpha=0.12, color='#D85A30')
    ax1.set_xlim(-np.pi/2, np.pi/2)
    ax1.set_title('Shoulder — command vs actual', fontsize=11)
    ax1.set_xlabel('Angle (rad)')
    ax1.set_ylabel('Time (s)')
    ax1.legend(fontsize=9)
    ax1.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

    # ── Elbow: command vs actual ─────────────────────────────────────────────
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(cmd_el, t, color='#378ADD', linewidth=2, linestyle='--', label='Commanded')
    ax2.plot(act_el, t, color='#1D9E75', linewidth=2, label='Actual')
    ax2.fill_betweenx(t, cmd_el, act_el, alpha=0.12, color='#1D9E75')
    ax2.set_xlim(-np.pi/2, np.pi/2)
    ax2.set_title('Elbow — command vs actual', fontsize=11)
    ax2.set_xlabel('Angle (rad)')
    ax2.set_ylabel('Time (s)')
    ax2.legend(fontsize=9)
    ax2.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

    # ── Shoulder error ───────────────────────────────────────────────────────
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(sh_err_deg, t, color='#D85A30', linewidth=1.5)
    ax3.fill_betweenx(t, sh_err_deg, alpha=0.15, color='#D85A30')
    ax3.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax3.axvline( sh_mae, color='#D85A30', linewidth=1, linestyle=':', label=f'MAE = {sh_mae:.3f}°')
    ax3.axvline(-sh_mae, color='#D85A30', linewidth=1, linestyle=':')
    ax3.set_xlim(-np.degrees(np.pi/2), np.degrees(np.pi/2))
    ax3.set_title('Shoulder tracking error', fontsize=11)
    ax3.set_xlabel('Error (deg)')
    ax3.set_ylabel('Time (s)')
    ax3.legend(fontsize=9)
    ax3.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

    # ── Elbow error ──────────────────────────────────────────────────────────
    ax4 = fig.add_subplot(gs[1, 1])
    ax4.plot(el_err_deg, t, color='#1D9E75', linewidth=1.5)
    ax4.fill_betweenx(t, el_err_deg, alpha=0.15, color='#1D9E75')
    ax4.axvline(0, color='black', linewidth=0.8, linestyle='-')
    ax4.axvline( el_mae, color='#1D9E75', linewidth=1, linestyle=':', label=f'MAE = {el_mae:.3f}°')
    ax4.axvline(-el_mae, color='#1D9E75', linewidth=1, linestyle=':')
    ax4.set_xlim(-np.degrees(np.pi/2), np.degrees(np.pi/2))
    ax4.set_title('Elbow tracking error', fontsize=11)
    ax4.set_xlabel('Error (deg)')
    ax4.set_ylabel('Time (s)')
    ax4.legend(fontsize=9)
    ax4.grid(True, linestyle='--', linewidth=0.4, alpha=0.6)

    plt.savefig(f"{file.replace('.csv', '')}_results.png", dpi=150, bbox_inches='tight')
    plt.show()