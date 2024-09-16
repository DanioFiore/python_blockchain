class Script:
    def __init__(self, cmds = None):
        self.cmds = ([] if cmds is None else cmds)

# a class method is a method that belongs to the class itself, not to an instance of the class.
# cls is the class itself, and self refers to the instance of the class.
# p2pkh = Pay to Public Key Hash
@classmethod
def p2pkh_script(cls, hash160):
    """Takes a hash160 and returns a P2PKH ScriptPubKey."""
    return Script([0x76, 0xa9, hash160, 0x88, 0xac])