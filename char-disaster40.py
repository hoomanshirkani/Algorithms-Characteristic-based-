import pandas as pd
import time
import random
import math

# Define the tiers
tiers = ["edge", "regional", "core"]

# Define the slices
services = ["Autonomous Vehicles", "Remote Surgery", "Industrial Automation", "Drone Control", "Smart Grid", "Smart Metering"]

# Define requirements for each service
service_reqs = {
    "Autonomous Vehicles": {"cpu": 16, "bw": 10, "latency": 1, "power": 10},
    "Remote Surgery": {"cpu": 32, "bw": 10, "latency": 1, "power": 15},
    "Industrial Automation": {"cpu": 16, "bw": 10, "latency": 1, "power": 10},
    "Drone Control": {"cpu": 8, "bw": 10, "latency": 5, "power": 8},
    "Smart Grid": {"cpu": 8, "bw": 0.1, "latency": 15, "power": 5},
    "Smart Metering": {"cpu": 4, "bw": 0.05, "latency": 100, "power": 3}
}

# Define number of each type of clouds
num_clouds = {"edge": 50, "regional": 20, "core": 1}  # Make sure to use at least 5 clouds in each tier for this 40% disaster scenario to work

# Define total cloud resources
clouds_cpu_res = {"edge": [50 for _ in range(num_clouds["edge"])], 
                  "regional": [150 for _ in range(num_clouds["regional"])], 
                  "core": [1500 for _ in range(num_clouds["core"])]}
clouds_bw_res = {"edge": [150 for _ in range(num_clouds["edge"])], 
                 "regional": [1500 for _ in range(num_clouds["regional"])], 
                 "core": [15000 for _ in range(num_clouds["core"])]}
clouds_power_res = {"edge": [100 for _ in range(num_clouds["edge"])], 
                    "regional": [100 for _ in range(num_clouds["regional"])], 
                    "core": [100 for _ in range(num_clouds["core"])]}
clouds_latency = {"edge": [1 for _ in range(num_clouds["edge"])], 
                  "regional": [5 for _ in range(num_clouds["regional"])], 
                  "core": [10 for _ in range(num_clouds["core"])]}

# Define the disaster states for the clouds (40% of the clouds in each tier are in a disaster state)
clouds_disaster_state = {"edge": [False for _ in range(num_clouds["edge"])], 
                         "regional": [False for _ in range(num_clouds["regional"])], 
                         "core": [False for _ in range(num_clouds["core"])]}

for tier in tiers:
    num_clouds_in_tier = num_clouds[tier]
    num_disaster_clouds = math.floor(num_clouds_in_tier * 0.4)
    disaster_cloud_indices = random.sample(range(num_clouds_in_tier), num_disaster_clouds)
    for i in disaster_cloud_indices:
        clouds_disaster_state[tier][i] = True

# Define used cloud resources (initialized to zero)
clouds_cpu_used = {"edge": [0 for _ in range(num_clouds["edge"])], 
                   "regional": [0 for _ in range(num_clouds["regional"])], 
                   "core": [0 for _ in range(num_clouds["core"])]}
clouds_bw_used = {"edge": [0 for _ in range(num_clouds["edge"])], 
                  "regional": [0 for _ in range(num_clouds["regional"])], 
                  "core": [0 for _ in range(num_clouds["core"])]}
clouds_power_used = {"edge": [0 for _ in range(num_clouds["edge"])], 
                     "regional": [0 for _ in range(num_clouds["regional"])], 
                     "core": [0 for _ in range(num_clouds["core"])]}

# Initialize number of slices for each service
num_slices = {"Autonomous Vehicles": 1, "Remote Surgery": 1, "Industrial Automation": 1, "Drone Control": 1, "Smart Grid": 1000000, "Smart Metering": 1}

# Initialize counters for number of placed slices
num_slices_placed = {service: 0 for service in services}

# Acceptance ratio variables
service_acceptance_ratios = {service: 0 for service in services}
overall_acceptance_ratio = 0

start = time.time()

# Main loop for placing slices
for service, reqs in service_reqs.items():
    for _ in range(num_slices[service]):
        cpu_req = reqs["cpu"]
        bw_req = reqs["bw"]
        latency_req = reqs["latency"]
        power_req = reqs["power"]

        max_weight = float('-inf')
        max_weight_cloud = None
        max_weight_tier = None

        for t in tiers:
            for j in range(num_clouds[t]):
                # If the cloud is not in a disaster state and can accommodate the slice
                if not clouds_disaster_state[t][j] and cpu_req <= (clouds_cpu_res[t][j] - clouds_cpu_used[t][j]) and bw_req <= (clouds_bw_res[t][j] - clouds_bw_used[t][j]) and latency_req >= clouds_latency[t][j] and power_req <= (clouds_power_res[t][j] - clouds_power_used[t][j]):
                    cpu_avg = clouds_cpu_used[t][j] / clouds_cpu_res[t][j] if clouds_cpu_res[t][j] != 0 else 0
                    bw_avg = clouds_bw_used[t][j] / clouds_bw_res[t][j] if clouds_bw_res[t][j] != 0 else 0
                    bat_avg = clouds_power_used[t][j] / clouds_power_res[t][j] if clouds_power_res[t][j] != 0 else 0

                    # Calculate the weight of the cloud
                    w_r = clouds_power_res[t][j]  # Use the battery power as W_R
                    weight = w_r + 1/(cpu_avg + bw_avg + bat_avg+ 0.00001)  # We no longer subtract latency from the weight

                    # If this weight is higher than the current maximum, update the maximum and remember this cloud
                    if weight > max_weight:
                        max_weight = weight
                        max_weight_cloud = j
                        max_weight_tier = t

        # If a cloud was found to place the slice
        if max_weight_cloud is not None:
            clouds_cpu_used[max_weight_tier][max_weight_cloud] += cpu_req
            clouds_bw_used[max_weight_tier][max_weight_cloud] += bw_req
            clouds_power_used[max_weight_tier][max_weight_cloud] += power_req

            num_slices_placed[service] += 1

    # Calculate the acceptance ratio for the service
    service_acceptance_ratios[service] = num_slices_placed[service] / num_slices[service]

# Calculate the overall acceptance ratio
overall_slices_req = sum(num_slices.values())
overall_slices_placed = sum(num_slices_placed.values())
overall_acceptance_ratio = overall_slices_placed / overall_slices_req if overall_slices_req != 0 else 0

# Print the final result
print("Placement took", time.time() - start, "seconds")
print("Service acceptance ratios:", service_acceptance_ratios)
print("Overall acceptance ratio:", overall_acceptance_ratio)
