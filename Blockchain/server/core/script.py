from Blockchain.server.tools.tools import intToLittleEndian, encodeVarInt

class Script:
    def __init__(self, cmds = None):
        self.cmds = ([] if cmds is None else cmds)

    # a class method is a method that belongs to the class itself, not to an instance of the class.
    # cls is the class itself, and self refers to the instance of the class.
    # p2pkh = Pay to Public Key Hash
    @classmethod
    def p2pkh_script(cls, hash160):
        """Takes a hash160 and returns a P2PKH ScriptPubKey."""
        return Script([0x76, 0xA9, hash160, 0x88, 0xAC])
    
    def serialize(self):
        # initialize what we'll send back
        result = b""
        # go through each cmd
        for cmd in self.cmds:
            # if the cmd is an integer, it's an opcode
            if type(cmd) == int:
                # turn the cmd into a single byte integer using intToLittleEndian
                # result += intToLittleEndian(cmd, 1)
                result += intToLittleEndian(cmd, 1)
            else:
                # otherwise, this is an element
                # get the length in bytes
                length = len(cmd)
                # for large lengths, we have to use a pushdata opcode
                if length < 75:
                    # turn the length into a single byte integer
                    result += intToLittleEndian(length, 1)
                elif length > 75 and length < 0x100:
                    # 76 is pushdata1
                    result += intToLittleEndian(76, 1)
                    result += intToLittleEndian(length, 1)
                elif length >= 0x100 and length <= 520:
                    # 77 is pushdata2
                    result += intToLittleEndian(77, 1)
                    result += intToLittleEndian(length, 2)
                else:
                    raise ValueError("too long an cmd")

                result += cmd
        # get the length of the whole thing
        total = len(result)
        # encode_varint the total length of the result and prepend
        return encodeVarInt(total) + result