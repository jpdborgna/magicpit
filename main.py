#!python

import tarfile
from cStringIO import StringIO
import sys
import random
import struct

def random_bytes(amount):
    return bytearray(random.getrandbits(8) for i in range(amount))

class Magic:

    class Field:
        """Class for containing a line of magic configuration/conditions"""
        def __init__(self, configline):
            cols = [x.strip() for x in configline.split()]
            self.offset = cols[0]
            self.ftype = cols[1]
            self.condition = cols[2]
            self.value = self.create_value()

        def create_value(self):
            """Creates a new (random?) valid value according to conditios and types"""
            notrandomvalue = 7 #this *should* be a radom value that satisfies the fcondition
            if self.ftype == 'leshort':
                return struct.pack('<h', notrandomvalue)
            elif self.ftype == '':
                return

            #not matched? not implemented? return some BS
            return 'someBS'

    def __init__(self):
        self.fields = []
        self.magic = 'MZ'

    def __init__(self, configstring):
        self.load(configstring)

    def load(self, configstring):
        """Sets the magic paramteres from a configuration chunk string"""
        #load all the fields from confstrings
        for line in configstring:
            self.fields.append(Magic.Field(line))
        return

    def create_sample(self, size=100, data=None):
        """Creates a file with the magic needed, filled with size amount of random
            bytes or data repeated/truncated"""
        data = random_bytes(size)
        if self.offset:
            fill = ''
        #should I use bytes not strings
        sample = self.magic
        cursor = len(sample)

        for field in self.fields:
            if field.offset > cursor: #skip until next data place
                sample = sample + 'X' * (field.offset - cursor)
                cursor = field.offset
            sample = sample + field.value

        return sample


def load_all_the_magic(filename):
    all_the_magic = []

    with open(filename) as magicfile:
        configstring = ''
        for line in magicfile:
            line = line.strip()
            #filter empty lines and comments
            if line and not line.beginswith('#'):
                #new magic?
                if line.beginswith('0 '):#new config block (assuming too much?)
                    if configstring:
                        all_the_magic.append(Magic(configstring))
                    configstring = line
                    continue
                configstring = configstring + line

    return all_the_magic

def main():

    #load a magicfile
    all_the_magic = load_all_the_magic('magic.txt')


    #set the output to stdout but with a name, p
    out = tarfile.open('fullbackup_secure_this_file.tar', fileobj=sys.stdout, mode='w')


    ##infinite loop
    ##while True:
    for saraza in range(5):
        magic = random.choice(all_the_magic)

        data = magic.create_sample()

        try:
            info = tarfile.TarInfo('made_up_file.txt')
            info.size = len(data)
            out.addfile(info, StringIO(data))
        except Exception:
            pass

    #out.close() #better not close stdout


if __name__ == '__main__':
        main()
