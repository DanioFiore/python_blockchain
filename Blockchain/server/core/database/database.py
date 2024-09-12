import os
import json

# this base class is used to read and update data on our "DB" simulated with a file
class BaseDB:
    def __init__(self):
        self.base_path = 'data'
        self.file_path = '/'.join((self.base_path, self.file_name))
    
    # read the data from the file
    def read(self):
        if not os.path.exists(self.file_path):
            print(f"File {self.file_path} not available")
            return False
        
        with open(self.file_path, "r") as file:
            raw = file.readline()
        
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            # if we trying to create genesis block, return empty
            data =  []
        
        return data

    # append data to the file
    def write(self, item):
        data = self.read()

        if data:
            # add the new block to the existing data
            data = data + item
        else:
            # if data is empty, that means it's a genesis block
            data = item

        with open(self.file_path, "w+") as file:
            file.write(json.dumps(data))


class BlockchainDB(BaseDB):
    def __init__(self):
        # set our "DB" file name
        self.file_name = 'blockchain'
        super().__init__()

    # catch the last block
    def lastBlock(self):
        # read from our "DB"
        data = self.read()
        print(data)
        if data:
            return data[-1]