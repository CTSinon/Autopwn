import re
import pwnlib
from pwn import *

# this module aims to add new methods to tube class.

def add_features(src):
    features = [extnum, l64, l32, sla, sa, lg, se, sl, ru, rl, verify_valid, polling]
    for feature in features:
        setattr(pwnlib.tubes.tube.tube, feature.__name__, feature)
    assert type(src) != int
    return src

def verify_valid(self, func, **kwargs):
    return func(self, kwargs)

def polling(self, templates=None, count=0):
    assert templates != None
    if count == 1:
        self.recvuntil(templates[0])
        self.sendline(templates[1])
        return
    for template in templates:
        self.recvuntil(template[0])
        self.sendline(template[1])


def l64(self):
    return self.verify_valid(lambda ex, args: u64(ex.recvuntil("\x7f")[-6:].ljust(8,"\x00")))

def l32(self):
    return self.verify_valid(lambda ex, args: u32(ex.recvuntil("\xf7")[-4:].ljust(4,"\x00")))

def rl(self):
    return self.verify_valid(lambda ex, args: ex.recvline())

def sla(self, after, send):
    return self.verify_valid(lambda ex, args: ex.sendlineafter(args['after'], args['send']),
                             after=after,
                             send=send)

def sa(self, after, send):
    return self.verify_valid(lambda ex, args: ex.sendafter(args['after'], args['send']),
                             after=after,
                             send=send)

def lg(self, message):
    return self.verify_valid(lambda ex, args: ex.success(args['message']),
                             message=message)

def se(self, payload):
    return self.verify_valid(lambda ex, args: ex.send(args['payload']), payload=payload)

def sl(self, payload):
    return self.verify_valid(lambda ex, args: ex.sendline(args['payload']), payload=payload)

def ru(self, until):
    return self.verify_valid(lambda ex, args: ex.recvuntil(str(args['until'])), until=until)
    
# extract numbers with a given base from an output line
def extnum(self, base = 10):  
    res = []
    if base == 10:
        pattern = re.compile(r'\d+')
    elif base == 16:
        pattern = re.compile(r"[0-9a-fA-F]{4,}")
    else:
        return None

    src = self.recvline()
    res = re.findall(pattern, src)
    for i in range(0, len(res)):
        res[i] = int(res[i], base=base)
    return res