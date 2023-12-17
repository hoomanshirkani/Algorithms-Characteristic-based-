import pandas as pd
import time
import random

# Define the slices
services = ["Autonomous Vehicles", "Remote Surgery", "Industrial Automation", "Drone Control", "Smart Grid", "Smart Metering"]

# Define the tiers
tiers = ["edge", "regional", "core"]

# Define number of each type of clouds
num_clouds = {"edge": 50, "regional": 20, "core": 1}

# Create a dictionary to track the number of slices placed per service
num_slices_placed = {service: 0 for service in services}

# Create a dictionary to track the acceptance ratio per service
acceptance_ratio_per_service = {service: 0 for service in services}

# Initialize number of slices for each service
num_slices = {"Autonomous Vehicles": 10000, "Remote Surgery": 10000, "Industrial Automation": 10000, "Drone Control": 10000, "Smart Grid": 10000, "Smart Metering": 10000}

# Define total cloud resources
clouds_cpu_res = {"edge": [50 for _ in range(num_clouds["edge"])], "regional": [150 for _ in range(num_clouds["regional"])], "core": [1500 for _ in range(num_clouds["core"])]}
clouds_bw_res = {"edge": [150 for _ in range(num_clouds["edge"])], "regional": [1500 for _ in range(num_clouds["regional"])], "core": [15000 for _ in range(num_clouds["core"])]}
clouds_power_res = {"edge": [100 for _ in range(num_clouds["edge"])], "regional": [100 for _ in range(num_clouds["regional"])], "core": [100 for _ in range(num_clouds["core"])]}
clouds_latency = {"edge": [1 for _ in range(num_clouds["edge"])], "regional": [5 for _ in range(num_clouds["regional"])], "core": [10 for _ in range(num_clouds["core"])]}
clouds_energy_consumption = {"edge": [5 for _ in range(num_clouds["edge"])], "regional": [10 for _ in range(num_clouds["regional"])], "core": [15 for _ in range(num_clouds["core"])]}

# Create a dictionary to indicate which clouds are in disaster areas
# We will randomly select 40% of the clouds on each tier
disaster_clouds = {tier: random.sample(range(num), round(num * 0.0)) for tier, num in num_clouds.items()}

start = time.time()

# Define maximum energy allowed per service
max_energy_per_service = {"Autonomous Vehicles": 5, "Remote Surgery": 5, "Industrial Automation": 5, "Drone Control": 3, "Smart Grid": 5, "Smart Metering": 2}

# Define slice requirements
for service in services:
    slices_cpu_req = [16 if service == "Autonomous Vehicles" else 32 if service == "Remote Surgery" else 16 if service == "Industrial Automation" else 8 if service in ["Drone Control", "Smart Grid"] else 4 for _ in range(num_slices[service])]
    slices_bw_req = [10 if service in ["Autonomous Vehicles", "Remote Surgery", "Industrial Automation", "Drone Control"] else 0.1 if service == "Smart Grid" else 0.05 for _ in range(num_slices[service])]
    slices_latency_req = [1 if service in ["Autonomous Vehicles", "Remote Surgery", "Industrial Automation"] else 5 if service == "Drone Control" else 15 if service == "Smart Grid" else 100 for _ in range(num_slices[service])]
    slices_energy_req = [1 if service in ["Autonomous Vehicles", "Remote Surgery", "Industrial Automation", "Drone Control"] else 0.5 if service == "Smart Grid" else 0.05 for _ in range(num_slices[service])]

    total_slices = num_slices[service]

    for i in range(total_slices):
        cpu_req = slices_cpu_req[i]
        bw_req = slices_bw_req[i]
        latency_req = slices_latency_req[i]
        energy_req = slices_energy_req[i]
        slice_placed = False

        for t in tiers:
            # Sort the clouds (descending)
            clouds_sorted = sorted(range(num_clouds[t]), key=lambda j: (clouds_cpu_res[t][j], clouds_bw_res[t][j], -clouds_energy_consumption[t][j]), reverse=False)
            print(clouds_sorted)
            for j in clouds_sorted:
                # If the cloud can accommodate the slice and satisfy its latency requirement
                # And if the cloud is not in the disaster area
                # And if energy consumption does not exceed the maximum allowed energy for the service
                if cpu_req <= clouds_cpu_res[t][j] and bw_req <= clouds_bw_res[t][j] and latency_req >= clouds_latency[t][j] and energy_req <= max_energy_per_service[service] and j not in disaster_clouds[t]:
                    # Place the slice on the cloud
                    clouds_cpu_res[t][j] -= cpu_req
                    clouds_bw_res[t][j] -= bw_req
                    clouds_energy_consumption[t][j] -= energy_req
                    num_slices_placed[service] += 1
                    slice_placed = True
                    break

            if slice_placed:
                break

# Calculate acceptance ratio for each service
for service in services:
    acceptance_ratio_per_service[service] = (num_slices_placed[service] / num_slices[service]) * 100 if num_slices[service] != 0 else 0

# Calculate overall acceptance ratio
total_slices_all_services = sum(num_slices.values())
total_slices_placed_all_services = sum(num_slices_placed.values())
overall_acceptance_ratio = (total_slices_placed_all_services / total_slices_all_services) * 100 if total_slices_all_services != 0 else 0

end = time.time()
exec_time = end - start

print("Execution Time: ", exec_time)
print("Acceptance Ratios: ", acceptance_ratio_per_service)
print("Overall Acceptance Ratio: ", overall_acceptance_ratio)
