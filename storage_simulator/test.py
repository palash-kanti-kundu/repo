from StorageSimulator import StorageSimulator
from deepdiff import DeepDiff
import json
from datetime import datetime, timedelta
import sqlite3
import os

def test():
    # Open Test Configurations and test files
    with open('test_data/dc_config.json', 'r') as f:
        config = json.load(f)
    
    with open('test_data/db_results.json', 'r') as f:
        expected_db = json.load(f)

    db_name = 'test_data/test_iops.db'
    if os.path.exists(db_name):
        os.remove(db_name)
        print("Successfully! The file has been removed")
    else:
        print("Cannot delete the file as it doesn't exist")
    
    sim = StorageSimulator(config, db_name)

    datetime_str = '01-01-21 00:00:00'
    datetime_object = datetime.strptime(datetime_str, '%m-%d-%y %H:%M:%S')

    # Write files to storage
    for i in range(8):
        if i < 5:
            print(sim.write_file("vm1", 100.0, "Hello " + str(i), "file"+str(i), datetime_object + timedelta(hours = i)))
        else:
            print(sim.write_file("vm2", 100.0, "Hello " + str(i), "file"+str(i), datetime_object + timedelta(hours = i)))
        print("Need to tally " + 'test_data/dc_config_add_'+ str(i) + '.json')
        try:
            with open('test_data/dc_config_add_'+ str(i) + '.json', 'r') as f:
                expected_config = json.load(f)
                if sim.get_changed_config() == expected_config:
                    print("Correct after writing " + str(i + 1) + " file")
                else:
                    print(DeepDiff(expected_config, sim.get_changed_config()))
                    print(json.dumps(config))
        except Exception as e:
            print('Iteration', i, 'does not have test', e )
        print('\n')
    
    # Check the read
    file = sim.read_file("vm1", "file_10", '01-01-21 23:00:00')
    print("file_10 read check", DeepDiff(file, {"status": "Error", "file_id": "file_10", "size": -1, "content": ""}))
    
    file = sim.read_file("vm1", "file0", '01-01-21 23:00:00')
    print(DeepDiff(file, {"status": "Success", "file_id": "file0", "size": 100.0, "content": "Hello 0"}))
    
    # Check DB Status
    conn = sqlite3.connect('test_data/test_iops.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * from array_iops')

    array_rows = []
    for row in sqlite3.connect(db_name).execute("SELECT * FROM array_iops").fetchall():
        array_rows.append({"id": row[0], "time": row[1], "read": float(row[2]), "write": float(row[3])})
    pool_rows = []
    for row in sqlite3.connect(db_name).execute("SELECT * FROM pool_iops").fetchall():
        pool_rows.append({"id": row[0], "time": row[1], "read": row[2], "write": row[3]})
    volume_rows = []
    for row in sqlite3.connect(db_name).execute("SELECT * FROM volume_iops").fetchall():
        volume_rows.append({"id": row[0], "time": row[1], "read": row[2], "write": row[3]})
    vm_rows = []
    for row in sqlite3.connect(db_name).execute("SELECT * FROM vm_iops").fetchall():
        vm_rows.append({"id": row[0], "time": row[1], "read": row[2], "write": row[3]})
    
    print("Array IOPS Check", DeepDiff(expected_db['array_iops'], array_rows))
    print("Pool IOPS Check", DeepDiff(expected_db['pool_iops'], pool_rows))
    print("Volume IOPS Check", DeepDiff(expected_db['volume_iops'], volume_rows))
    print("VM IOPS Check", DeepDiff(expected_db['vm_iops'], vm_rows))
    
test()