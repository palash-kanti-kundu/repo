import json
import sqlite3
from datetime import datetime, timedelta
import sqlite3
import random

class DatabaseManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        columns: a dict where key is column name and value is column type
        """
        columns_str = ', '.join([f'{name} {type}' for name, type in columns.items()])
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str});")

    def insert_data(self, table_name, data):
        """
        data: a dict where key is column name and value is data to insert
        """
        columns_str = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        self.cursor.execute(f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});", list(data.values()))
        self.conn.commit()

    def close(self):
        self.conn.close()

db = DatabaseManager("iops.db")
db.create_table('array_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
db.create_table('pool_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
db.create_table('volume_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
db.create_table('vm_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})

def log(table, id, size, time, type):
    try:
        if type == 'W':
            db.insert_data(table, {'id': id, 'time': time, 'read': 0, 'write': size})
        else:
            db.insert_data(table, {'id': id, 'time': time, 'read': size, 'write': 0})
    except Exception as e:
        pass #print(e)

class Array:
    def __init__(self, data):
        self.id = data['id']
        self.capacity = data['capacity']
        self.used = data['used']
        self.free = data['free']
        self.files = data['files']

    def read(self, file_id, time, files):
        if file_id in self.files:
            try:
                foundFile = {'size': -1, 'content': ""}
                for file in files:
                    if file['id'] == file_id:
                        foundFile = file
                log('array_iops', self.id, foundFile['size'], time, 'R')
                return foundFile
            except Exception as e:
                pass #print(e)
        else:
            raise Exception('\t\t\tFile ' + file_id + ' not found in Array ' + self.id)

    def write(self, file_id, size, time):
        if self.free >= size:
            self.used += size
            self.free -= size
            self.files.append(file_id)
            log('array_iops', self.id, size, time, 'W')
            pass #print("\t\t\tFile " + file_id + " Write success on Array", self.id)
        else:
            raise Exception('Not enough space in array')
    
    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "used": self.used,
            "free": self.free,
            "files": self.files
        }

class StoragePool:
    def __init__(self, data, arrays):
        self.id = data['id']
        self.capacity = data['capacity']
        self.used = data['used']
        self.free = data['free']
        self.files = data['files']
        self.arrays = [next(array for array in arrays if array.id == array_id) for array_id in data['array']]

    def read(self, file_id, time, files):
        for arr in self.arrays:
            try:
                file = arr.read(file_id, time, files)
                log('pool_iops', self.id, file['size'], time, 'R')
                return file
            except Exception as e:
                continue
        raise Exception('\t\tFile ' +  file_id + ' not found in Pool ' + self.id)

    def write(self, file_id, size, time):
        for array in self.arrays:
            try:
                array.write(file_id, size, time)
                self.used += size
                self.free -= size
                self.files.append(file_id)
                log('pool_iops', self.id, size, time, 'W')
                return
            except Exception as e:
                print(e)
                continue
        raise Exception('Not enough space in storage pool')

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "used": self.used,
            "free": self.free,
            "files": self.files,
            "array": [array.id for array in self.arrays]
        }

class Volume:
    def __init__(self, data, storagePools):
        self.id = data['id']
        self.capacity = data['capacity']
        self.used = data['used']
        self.free = data['free']
        self.files = data['files']
        self.storagePools = []
        for sp in data['sp']:
            for pool in storagePools:
                if sp['id'] == pool.id:
                    self.storagePools.append(pool)
    
    def read(self, file_id, time,  files):
        for sp in self.storagePools:
            try:
                file = sp.read(file_id, time, files)
                log('volume_iops', self.id, file['size'], time, 'R')
                return file
            except Exception as e:
                continue
        raise Exception('\tFile ' + file_id + ' not found in Volume ' + self.id)

    def write(self, file_id, size, time):
        for sp in self.storagePools:
            try:
                sp.write(file_id, size, time)
                self.used += size
                self.free -= size
                self.files.append(file_id)
                log('volume_iops', self.id, size, time, 'W')
                #print("\tWrite success on Volume", self.id)
                return
            except Exception as e:
                print(e)
                continue
        raise Exception('Not enough space in volume')

    def to_dict(self):
        return {
            "id": self.id,
            "capacity": self.capacity,
            "used": self.used,
            "free": self.free,
            "files": self.files,
            "sp": [sp.to_dict() for sp in self.storagePools]
        }

class VM:
    def __init__(self, data, volumes):
        self.id = data['id']
        self.volumes = []
        for volume in data['volumes']:
            for v in volumes:
                if volume['id'] == v.id:
                    self.volumes.append(v)
        self.files = data['files']

    def write(self, file_id, size, time):
        for volume in self.volumes:
            try:
                volume.write(file_id, size, time)
                self.files.append(file_id)
                log('vm_iops', self.id, size, time, 'W')
                #print("Write success on VM", self.id)
                return
            except Exception as e:
                #print(e)
                continue
        raise Exception('Not enough space in VM')
    
    def read(self, file_id, time, files):
        for volume in self.volumes:
            try:
                file = volume.read(file_id, time, files)
                log('vm_iops', self.id, file['size'], time, 'R')
                return file
            except Exception as e:
                continue
        raise Exception('File ' + file_id + ' not found in VM ' + self.id)
    
    def to_dict(self):
        return {
            "id": self.id,
            "volumes": [volume.to_dict() for volume in self.volumes],
            "files": self.files
        }

class DataCenter:
    def __init__(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        self.arrays = [Array(array_data) for array_data in data['arrays']]
        self.storagePools = [StoragePool(sp_data, self.arrays) for sp_data in data['storagePools']]
        self.volumes = [Volume(volume_data, self.storagePools) for volume_data in data['volumes']]
        self.vms = [VM(vm_data, self.volumes) for vm_data in data['vms']]
        self.files = data['files']
    
    def read(self, vm_id, file_id, time):
        vm = next((vm for vm in self.vms if vm.id == vm_id), None)
        if not vm:
            raise Exception(f'VM {vm_id} not found')
        try:
            file = vm.read(file_id, time, self.files)
            return file['content']
        except Exception as e:
            pass

    def write(self, vm_id, file_id, size, content, time):
        vm = next((vm for vm in self.vms if vm.id == vm_id), None)
        if not vm:
            raise Exception(f'VM {vm_id} not found')
        vm.write(file_id, size, time)
        self.files.append({
            "id": file_id,
            "size": size,
            "content": content
        })
    
    def to_dict(self):
        return {
            "vms": [vm.to_dict() for vm in self.vms],
            "volumes": [volume.to_dict() for volume in self.volumes],
            "storagePools": [sp.to_dict() for sp in self.storagePools],
            "arrays": [array.to_dict() for array in self.arrays],
            "files": self.files
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

# Usage
dc = DataCenter('config.json')
print("Data Center Created")

datetime_str = '01-01-21 00:00:00'
datetime_object = datetime.strptime(datetime_str, '%m-%d-%y %H:%M:%S')

for i in range(500):
    if i  > 399 and i <= 400:
        maxSize = 15
        minSize = 10
    else:
        maxSize = 5
        minSize = 1
        
    fileSize = random.randint(minSize, maxSize)
    print(i, minSize, maxSize, fileSize)

    try:
        dc.write("vm1", "f" + str(i), fileSize, "File " + str(i) + " Content", datetime_object + timedelta(hours = i))
    except:
        pass


with open("final_state.json", "w") as f:
    json.dump(dc.to_dict(), f)

