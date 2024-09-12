from DatabaseManager import DatabaseManager

class StorageSimulator:
    def  __init__(self, config, db_path):
        self.config = config
        self.db = DatabaseManager(db_path)
        self.db.create_table('array_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
        self.db.create_table('pool_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
        self.db.create_table('volume_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})
        self.db.create_table('vm_iops', {'id': 'text', 'time': 'TIMESTAMP', 'read':'REAL', 'write':'REAL'})

    def log(self, table, id, size, time, type):
        try:
            if type == 'W':
                self.db.insert_data(table, {'id': id, 'time': time, 'read': 0, 'write': size})
            else:
                self.db.insert_data(table, {'id': id, 'time': time, 'read': size, 'write': 0})
        except Exception as e:
            print(e)
    
    def get_changed_config(self):
        return self.config

    def get_object_by_key(self, key, objKey):
        for obj in self.config[objKey]:
            if obj['id'] == key:
                return obj
        return None

    def get_vm_by_id(self, vm_id):
        return self.get_object_by_key(vm_id, 'vms')

    def get_volume_by_id(self, vol_id):
        return self.get_object_by_key(vol_id, 'volumes')
        
    def get_sp_by_id(self, sp_id):
        return self.get_object_by_key(sp_id, 'storagePools')

    def get_array_by_id(self, array_id):
        return self.get_object_by_key(array_id, 'arrays')
    
    def get_file_by_id(self, file_id):
        for x in self.config['files']:
            if x['id'] == file_id:
                return x
    
    def log_object_iops(self, obj, size, time, type, table):
        self.log(table, obj['id'], size, time, type)

    def manage_space_in_objects(self, obj, file_size):
        obj['used'] += file_size
        obj['free'] -= file_size

    def add_file_to_object(self, obj, file_id, size, time, table):
        self.log_object_iops(obj, size, time, 'W', table)
        obj['files'].append(file_id)

    def manage_files_in_object(self, obj, file_size, file_id, time, table):
        self.manage_space_in_objects(obj, file_size)
        self.add_file_to_object(obj, file_id, file_size, time, table)

    def write_file(self, vm_id, file_size, file_content, file_id, time):
        vm =  self.get_vm_by_id(vm_id)
        if vm == None:
            return "Could not find VM"
        written = False
        for volume in vm['volumes']:
            if volume['free'] >= file_size:
                vol = self.get_volume_by_id(volume['id'])
                self.manage_space_in_objects(volume, file_size)
                self.manage_files_in_object(vol, file_size, file_id, time, 'volume_iops')

                for sp in vol['sp']:
                    if sp['free'] >= file_size:
                        pool = self.get_sp_by_id(sp['id'])
                        self.manage_space_in_objects(sp, file_size)
                        self.manage_files_in_object(pool, file_size, file_id, time, 'pool_iops')
                            
                        for array_id in pool['array']:
                            array = self.get_array_by_id(array_id)
                            if array['free'] >= file_size and not written:
                                self.manage_files_in_object(array, file_size, file_id, time, 'array_iops')
                                self.add_file_to_object(vm, file_id, file_size, time, 'vm_iops')
                                self.config['files'].append({'id': file_id, 'size': file_size, 'content': file_content})
                                #print("Files ", vm['files'])
                                written = True
                        return "File written successfully"
                return "Not enough space in storage pools"
        return "Not enough space in volumes"

    def file_exists_in_object(self, obj, file_id):
        return file_id in obj['files']

    def read_file(self, vm_id, file_id, time):
        vm =  self.get_vm_by_id(vm_id)
        if vm == None:
            return "Vm " + vm_id + " does not exist"
        
        if self.file_exists_in_object(vm, file_id):
            file_size = -1
            
            for volume in vm['volumes']:
                vol = self.get_volume_by_id(volume['id'])
                if self.file_exists_in_object(vol, file_id):
                    for pool in vol['sp']:
                        sp = self.get_sp_by_id(pool['id'])
                        if self.file_exists_in_object(sp, file_id):
                            for array in sp['array']:
                                arr = self.get_array_by_id(array)
                                if self.file_exists_in_object(arr, file_id):
                                    file = self.get_file_by_id(file_id)
                                    file_size = file['size']
                                    self.log_object_iops(arr, file_size, time, 'R', 'array_iops')
                                    self.log_object_iops(sp, file_size, time, 'R', 'pool_iops')
                                    self.log_object_iops(vol, file_size, time, 'R', 'volume_iops')
                                    self.log_object_iops(vm, file_size, time, 'R', 'vm_iops')
                                    return {"status": "Success", "file_id": file_id, "size": file['size'], "content": file["content"]}
        else:
            return {"status": "Error", "file_id": file_id, "size": -1, "content": ""}