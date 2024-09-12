from ma import analyse_timeseries
import pandas as pd
import json

anomalous_data = False
fields = ['time', 'id', 'write', 'read']
df = pd.read_csv('storage_simulator/data/total_cust_iops.csv',
                parse_dates=['time'],
                skipinitialspace=True,
                usecols=fields, header=0, index_col=1)
if not df.empty:
    anomalous_data = analyse_timeseries(df, fields[3], 'Customer Level Write')

print("Customer data is anomalous", anomalous_data)

if anomalous_data:
    config = {}
    with open('storage_simulator/data/config.json', 'r') as f:
        config = json.load(f)

    arrays = config['arrays']
    anomaly_arrays = []

    for array in arrays:
        df = pd.read_csv('storage_simulator/data/total_array_iops.csv',
                    parse_dates=['time'],
                    skipinitialspace=True,
                    usecols=fields, header=0, index_col=1)
        adf = df.loc[df['id'] == array['id']]
        if not adf.empty:
            anomaly_detected = analyse_timeseries(adf, fields[3], 'Array Level Write on ' + array['id'])
            if  anomaly_detected:
                anomaly_arrays.append(array['id'])

    print("Customer arrays that are anomalous", anomaly_arrays)
    #input("Press any key for next step")

    pools = config['storagePools']
    anomaly_pools = []

    for pool in pools:
        for array in pool['array']:
            if array in anomaly_arrays:
                df = pd.read_csv('storage_simulator/data/total_pool_iops.csv',
                            parse_dates=['time'],
                            skipinitialspace=True,
                            usecols=fields, header=0, index_col=1)
                adf = df.loc[df['id'] == pool['id']]
                if not adf.empty:
                    anomaly_detected = analyse_timeseries(adf, fields[3], 'Pool Level Write on ' + pool['id'], showPlot=False)
                    if  anomaly_detected:
                        anomaly_pools.append(pool['id'])

    print("Customer storagePools that are anomalous", anomaly_pools)
    #input("Press any key for next step")

    volumes = config['volumes']
    anomaly_volumes = []

    for volume in volumes:
        for pool in volume['sp']:
            if pool['id'] in anomaly_pools:
                df = pd.read_csv('storage_simulator/data/total_volume_iops.csv',
                            parse_dates=['time'],
                            skipinitialspace=True,
                            usecols=fields, header=0, index_col=1)
                adf = df.loc[df['id'] == volume['id']]
                if not adf.empty:
                    anomaly_detected = analyse_timeseries(adf, fields[3], 'Volume Level Write on ' + volume['id'])
                    if  anomaly_detected:
                        anomaly_volumes.append(volume['id'])

    print("Customer volumes that are anomalous", anomaly_volumes)
    #input("Press any key for next step")

    vms = config['vms']
    anomaly_vms = []

    for vm in vms:
        for volume in vm['volumes']:
            if volume['id'] in anomaly_volumes:
                df = pd.read_csv('storage_simulator/data/total_vm_iops.csv',
                            parse_dates=['time'],
                            skipinitialspace=True,
                            usecols=fields, header=0, index_col=1)
                adf = df.loc[df['id'] == vm['id']]
                if not adf.empty:
                    anomaly_detected = analyse_timeseries(adf, fields[3], 'VM Level Write on ' + vm['id'], False)
                    if  anomaly_detected:
                        anomaly_vms.append(vm['id'])

    print("VMs with anomalies", anomaly_vms)

    with open('output.json', 'w') as f:
        json.dump(anomaly_vms, f, ensure_ascii=False, indent=4)

input("Press any key to exit")