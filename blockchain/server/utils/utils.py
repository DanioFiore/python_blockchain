import hashlib

# hash256 its 2 rounds of sha256. It will create the hash and the hash that hash to create a new hash
def hash256(string):
    return hashlib.sha256(hashlib.sha256(string).digest()).digest()

# to allow us to import this file as a package, we have to create in utils folder, a file called __init__.py