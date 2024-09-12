import json
import random

def generate_arrays(arr_count):
    arrays = []
    for i in range(arr_count):
        capacity = float(random.randint(10, 100) * 100) * 1024 * 1024 * 1024 # TB to KB
        print("Added array", "a" + str(i))
        arrays.append({"id":"a" + str(i), "capacity": capacity, "used": 0.0, "free": capacity, "files":[]})
    return  arrays

def generate_pools(arrays):
    # Number of storage pools
    num_pools = min(len(arrays), random.randint(1, len(arrays)))

    # Distribute arrays to storage pools
    storage_pools = {f'sp{i}': [] for i in range(num_pools)}
    for i, array in enumerate(arrays):
        pool_id = f'sp{i % num_pools}'
        storage_pools[pool_id].append(array)

    pools = []
    # Print the distribution
    for pool_id, pool_arrays in storage_pools.items():
        pool_capacity = 0
        arrays = []
        for array in pool_arrays:
            pool_capacity += array['capacity']
            arrays.append(array['id'])
        print("Added pool", pool_id)
        pools.append({"id": pool_id, "capacity": pool_capacity, "array": arrays, "used": 0.0, "free": pool_capacity, "files": []})
    return pools

def generate_volumes(pools):   
    num_volumes = random.randint(1, len(pools)) * 2
    # Define the volumes
    volumes = [{"id": f"v{i+1}", "sp": [], "files": [], "capacity": 0.0, "used": 0.0, "free": 0.0} for i in range(num_volumes)]

    # Distribute the pools to volumes
    for pool in pools:
        while pool["free"] > 0:
            # Select a random volume
            volume = random.choice(volumes)
            
            # Determine the amount of capacity to allocate
            allocation = min(pool["free"], 2.0 * 1024 * 1024 * 1024)  # 2 TB, KB -> MB -> GB -> TB
            
            # Update the pool and volume
            pool["used"] += allocation
            pool["free"] -= allocation
            volume["capacity"] += allocation
            volume["free"] += allocation

            # Check if the pool is already in the volume
            existing_pool = next((p for p in volume["sp"] if p["id"] == pool["id"]), None)
            if existing_pool:
                # If the pool is already in the volume, update its capacity
                existing_pool["capacity"] += allocation
                existing_pool["free"] += allocation
            else:
                # If the pool is not in the volume, add it
                volume["sp"].append({"id": pool["id"], "capacity": allocation, "used": 0.0, "free": allocation})
            
            # Remove the volume from the list if it's full
            if volume["free"] == 0:
                volumes.remove(volume)
            print("Configured volume", volume['id'])
    return volumes

def generate_vms(volumes):
    # Create VMs
    num_vms = len(volumes) * 500
    vms = [{"id": f"vm{i}", "volumes": [], "files":[]} for i in range(1, num_vms + 1)]

    print("VMs generated, running volume distribution")

    # Distribute volumes to VMs
    for i, volume in enumerate(volumes):
        # Select a subset of VMs for this volume
        start_index = (num_vms // len(volumes)) * i
        end_index = start_index + (num_vms // len(volumes))
        selected_vms = vms[start_index:end_index]
        
        # Calculate the capacity to be allocated to each VM
        capacity_per_vm = volume["capacity"] / len(selected_vms)
        
        # Update the volume and VMs
        for vm in selected_vms:
            vm["volumes"].append({"id": volume["id"], "capacity": capacity_per_vm, "used": 0.0, "free": capacity_per_vm})
            volume["used"] += capacity_per_vm
            volume["free"] -= capacity_per_vm

    return vms

def find_storage_details(objs):
    objStorage = 0
    objFreeStorage = 0
    objUsedStorage = 0
    for obj in objs:
        objStorage += obj['capacity']
        objFreeStorage += obj['free']
        objUsedStorage += obj['used']
    return(objStorage, objFreeStorage, objUsedStorage)

def reset_obj(objs):
    for obj in objs:
        obj['used'] = 0.0
        obj['free'] = obj['capacity']

def generate_config(arr_count):
    arrays = generate_arrays(arr_count)
    storagePools = generate_pools(arrays)
    volumes = generate_volumes(storagePools)
    vms = generate_vms(volumes)

    print("Total arrays " + str(len(arrays)))
    storeDetails = find_storage_details(arrays)
    print("Total Storage from arrays", storeDetails[0], "Used Storage", storeDetails[2], "Free", storeDetails[1])
    reset_obj(arrays)
    print("Total pools " + str(len(storagePools)))
    storeDetails = find_storage_details(storagePools)
    print("Total Storage from arrays", storeDetails[0], "Used Storage", storeDetails[2], "Free", storeDetails[1])
    reset_obj(storagePools)
    print("Total volumes " + str(len(volumes)))
    storeDetails = find_storage_details(volumes)
    print("Total Storage from arrays", storeDetails[0], "Used Storage", storeDetails[2], "Free", storeDetails[1])
    reset_obj(volumes)
    print("Total vms " + str(len(vms)))

    

    config = {
        "vms": vms,
        "volumes": volumes,
        "storagePools": storagePools,
        "arrays": arrays,
        "files": []
    }

    return config

def write_config_to_file(config, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

config = generate_config(4)
write_config_to_file(config, 'config.json')
