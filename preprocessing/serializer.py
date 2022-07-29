import struct

class Serializer:
    def __init__(self):
        self.format = 'ffH'

    def to_binary(self, x, y, gene_tid_pair):
        return struct.pack(self.format, x, y, gene_tid_pair)

    def from_binary(self, b):
        return struct.unpack(self.format, b)
