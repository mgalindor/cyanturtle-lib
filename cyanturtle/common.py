import binascii
import os
import random
import string
import struct
import threading
import time


def random_code(length=6):
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(length))
    return x


def remove_none_in_dict(data):
    new_dict = {}
    for k, v in data.items():
        if type(v) == dict:
            new_dict[k] = remove_none_in_dict(v)
        elif v:
            new_dict[k] = v
    return new_dict


class ObjectId:
    """ An MongoDB ObjectId is a 12-byte unique identifier consisting of:
         - a 4-byte value representing the seconds since the Unix epoch,
         - a 3-byte random bytes,
         - a 2-byte process id, and
         - a 3-byte counter, starting with a random value.
    """
    _inc = random.randint(0, 0xFFFFFF)
    _inc_lock = threading.Lock()

    def __init__(self):
        self.__id = self.__generate()

    def __generate(self):
        # 4 bytes current time
        oid = struct.pack(">I", int(time.time()))

        # 3 random bytes
        oid += os.urandom(3)

        # 2 bytes pid
        oid += struct.pack(">H", os.getpid() % 0xFFFF)

        # 3 bytes inc
        with ObjectId._inc_lock:
            oid += struct.pack(">I", ObjectId._inc)[1:4]
            ObjectId._inc = (ObjectId._inc + 1) % (0xFFFFFF + 1)

        return oid

    @property
    def binary(self):
        """12-byte binary representation of this ObjectId.
        """
        return self.__id

    def __str__(self):
        return binascii.hexlify(self.__id).decode()
