import matplotlib.pyplot as plt
import csv
import numpy as np

files = [
    "horizontal_pose.csv",
    "upward_pose.csv",
    "45_degree_pose.csv"
]

for file in files:

    print("\n" + "="*50)
    print(f"RESULTS FOR: {file}")
    print("="*50)

    t = []
    cmd_sh = []
    act_sh = []
    cmd_el = []
    act_el = []

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)

        for row in reader:
            t.append(float(row[0]))
            cmd_sh.append(float(row[1]))
            act_sh.append(float(row[2]))
            cmd_el.append(float(row[5]))
            act_el.append(float(row[6]))

    t = np.array(t)
    cmd_sh = np.array(cmd_sh)
    act_sh = np.array(act_sh)
    cmd_el = np.array(cmd_el)
    act_el = np.array(act_el)


    mask = t <= 10

    cmd_sh = cmd_sh[mask]
    act_sh = act_sh[mask]
    cmd_el = cmd_el[mask]
    act_el = act_el[mask]

    
    cmd_sh_deg = np.degrees(cmd_sh)
    act_sh_deg = np.degrees(act_sh)

    cmd_el_deg = np.degrees(cmd_el)
    act_el_deg = np.degrees(act_el)

    
    sh_error = act_sh_deg - cmd_sh_deg
    el_error = act_el_deg - cmd_el_deg

    
    shoulder_mae = np.mean(np.abs(sh_error))
    elbow_mae = np.mean(np.abs(el_error))

    print("SHOULDER:")
    print(f"  Average error: {shoulder_mae:.4f}°")
   

    print("ELBOW:")
    print(f"  Average error: {elbow_mae:.4f}°")
   
    # Plot
    plt.figure()

    plt.plot(cmd_sh, t, label="Shoulder Command")
    plt.plot(act_sh, t, label="Shoulder Actual")

    plt.plot(cmd_el, t, label="Elbow Command")
    plt.plot(act_el, t, label="Elbow Actual")

    plt.xlabel("Joint Position (rad)")
    plt.ylabel("Time (s)")
    plt.title(f"Command vs Actual - {file}")
    plt.legend()
    plt.grid()

    plt.show()