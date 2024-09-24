import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log
from Blockchain.server.core.EllepticCurve.EllepticCurve import BASE58_ALPHABET

# hash256 its 2 rounds of sha256. It will create the hash and the hash that hash to create a new hash
def hash256(string):
    return hashlib.sha256(hashlib.sha256(string).digest()).digest()

def hash160(string):
    return RIPEMD160.new(sha256(string).digest()).digest()
# to allow us to import this file as a package, we have to create in utils folder, a file called __init__.py

def bytesNeeded(n):
    """
    Calculate the number of bytes required to represent an integer in little-endian format.

    This function takes an integer `n` and returns the minimum number of bytes needed to represent
    `n` in little-endian format. If `n` is zero, it returns 1 byte.

    Parameters:
    n (int): The integer to calculate the byte requirement for.

    Returns:
    int: The number of bytes required to represent `n` in little-endian format.
    """
    if n == 0:
        return 1
    # every number lower than 256 can be represented in 1 byte, so if n = 10, return 1 byte, also if n = 257, return 2 bytes, if n = 65536, return 3 bytes
    return int(log(n, 256)) + 1

def intToLittleEndian(n, length):
    """
    Convert an integer to little-endian byte representation.

    This function takes an integer `n` and a desired byte length `length`,
    and returns the little-endian byte representation of `n` with the specified length.

    Parameters:
    n (int): The integer to convert.
    length (int): The desired byte length of the resulting byte representation.

    Returns:
    bytes: The little-endian byte representation of `n` with the specified length.
    """
    return n.to_bytes(length, "little")

def littleEndianToInt(bts):
    """
    Convert a little-endian byte representation to an integer.

    This function takes a byte array `bytes` representing a little-endian integer,
    and returns the corresponding integer.

    Parameters:
    bytes (bytes): The little-endian byte representation of the integer.

    Returns:
    int: The integer represented by the little-endian byte representation.
    """
    return int.from_bytes(bts, "little")

def decodeBase58(address):
    num = 0

    for character in address:
        num *= 58
        num += BASE58_ALPHABET.index(character)

    # it will be a total of 25 bytes and turn into a big endian
    combined = num.to_bytes(25, byteorder='big')
    # the last 4 characters are the checksum
    checksum = combined[-4:]

    if hash256(combined[:-4])[:4] != checksum:
        raise ValueError(f'Bad address {checksum} {hash256(combined[:-4])[:4]}')
    return combined[1:-4]

def encodeVarInt(i):
    """
    Encode an integer as a varint.

    This function encodes an integer into a variable-length format, which is used in the Bitcoin protocol
    to represent integers that can take on a wide range of values. The encoding uses a single byte for
    values less than 0xfd, two bytes for values between 0xfd and 10000, four bytes for values between
    10000 and 100000000, and eight bytes for values between 100000000 and 10000000000000000.

    Parameters:
    i (int): The integer to be encoded. It must be a non-negative integer.

    Returns:
    bytes: The encoded varint.

    Raises:
    ValueError: If the input integer is too large (greater than or equal to 10000000000000000).
    """
    if i < 0xfd:
        return bytes([i])
    elif i < 10000:
        return b"\xfd" + intToLittleEndian(i, 2)
    elif i < 100000000:
        return b"\xfe" + intToLittleEndian(i, 4)
    elif i < 10000000000000000:
        return b"\xff" + intToLittleEndian(i, 8)
    else:
        raise ValueError("Integer too large: {}".format(i))