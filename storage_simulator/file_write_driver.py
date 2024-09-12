from StorageSimulator import StorageSimulator
import json
from datetime import datetime, timedelta
import random

with open('config.json', 'r') as f:
    config = json.load(f)

sim = StorageSimulator(config, "iops.db")

datetime_str = '19-01-21 00:00:00'
datetime_object = datetime.strptime(datetime_str, '%d-%m-%y %H:%M:%S')

all_vms = config['vms']

num_active_vms = int(len(all_vms) / 2)

active_vms = []
backup_vms = []

print("Active VMs")
for i in range(num_active_vms):
    active_vm = all_vms[i]
    #print(active_vm['id'])
    active_vms.append(active_vm)


file_index = 0
for i in range(6):
    print(datetime.now(), "Writing files for hour", i)
    for active_vm in active_vms:
        file_content = "Hello " + str(file_index)
        file_size = random.randint(1, 5)
        file_id = "file"+str(file_index)
        #print("Writing file to", active_vm['id'], file_id, file_size, file_content)
        sim.write_file(active_vm['id'], file_size, file_content, file_id, datetime_object + timedelta(hours = i))
        file_index += 1
    print("\n")

# Open the file in write mode ('w')
with open("data1.json", "w") as f:
    json.dump(config, f)


