from StorageSimulator import StorageSimulator
import json
from datetime import datetime, timedelta

with open('data1.json', 'r') as f:
    config = json.load(f)

sim = StorageSimulator(config, "backup_iops.db")

datetime_str = '18-01-21 23:59:59'
datetime_object = datetime.strptime(datetime_str, '%d-%m-%y %H:%M:%S')

all_vms = config['vms']

num_main_vms = int(len(all_vms) / 2)

main_vms = []
backup_vms = []

for i in range(num_main_vms):
    main_vms.append(all_vms[i])

for i in range(num_main_vms):
    backup_vms.append(all_vms[num_main_vms + i])

for main_vm in main_vms:
    print(main_vm['id'])
print("-----------")
for backup_vm in backup_vms:
    print(backup_vm['id'])
input()



for i in range(400):
    main_vm = main_vms[i]
    backup_vm = backup_vms[i]

    for file in main_vm['files']:
        file_read = sim.read_file(main_vm['id'], file, datetime_object)
        print(file_read)
        sim.write_file(backup_vm['id'], file_read['size'], file_read['content'], file_read['file_id'], datetime_object)
        
