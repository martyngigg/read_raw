"""Read a RAW file"""
from __future__ import print_function

import binaryfile as bf
import inspect
import sys

SEEK_BEG = 0
SEEK_CUR = 1

IDET_POS = 768

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

def display(obj):
    print(obj)

def to_string(obj):
    attrs = dir(obj)
    s = []
    for att in attrs:
        if att.startswith("__"):
            continue
        value = getattr(obj, att)
        if not inspect.isfunction(value):
            s.append(key_value_to_string(att, value))
    return "\n".join(s)

def key_value_to_string(name, value):
    return "{} = {}".format(name, value)

def str_join(arr, start, end):
    return ''.join(arr[start:end])

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

class HDR_STRUCT(object):

    @staticmethod
    def from_file(fid):
        data = bf.read_data(fid, 'char', n=80)
        hdr = HDR_STRUCT()
        hdr.inst_abrv = str_join(data, 0, 3)
        hdr.hd_run = int(str_join(data, 3, 8))
        hdr.hd_user = str_join(data, 8, 28)
        hdr.hd_title = str_join(data, 28, 52)
        hdr.hd_date = str_join(data, 52, 64)
        hdr.hd_time = str_join(data, 64, 72)
        hdr.hd_dur = str_join(data, 72, 80)
        return hdr

    def __init__(self):

        self.inst_abrv = None
        self.hd_run = None
        self.hd_user = None
        self.hd_title = None
        self.hd_date = None
        self.hd_time = None
        self.hd_dur = None

    def __str__(self):
        return to_string(self)

# -------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if len(sys.argv) == 1:
    raise RuntimeError("Usage: {} path".format(sys.argv[0]))

filepath = sys.argv[1]
fid = open(filepath, 'rb')

fid.seek(32*4, SEEK_BEG)
val = bf.read_int32(fid)
display(key_value_to_string("val", val))

fid.seek((126 + 67)*4, SEEK_BEG)
val = bf.read_int32(fid)
display(key_value_to_string("val", val))

sys.exit(0)

# HDR struct - 80 bytes or character arrays
hdr = HDR_STRUCT.from_file(fid)
display("-- HDR --")
display(hdr)
display("")

# Format version
frmt_ver_no = bf.read_int32(fid)
display(key_value_to_string("frmt_ver_no", frmt_ver_no))

# Address fields
addresses = bf.read_int32(fid, n=9)
display(key_value_to_string("addresses", addresses))
data_format = bf.read_int32(fid)
display(key_value_to_string("data_format", data_format))

print("run section pos =",fid.tell())

# Jump to i_det to find number of detectors
# Number of detectors & monitors
fid.seek(IDET_POS, SEEK_BEG)
i_det = bf.read_int32(fid)
i_mon = bf.read_int32(fid)
i_use = bf.read_int32(fid)
display(key_value_to_string("i_det", i_det))
display(key_value_to_string("i_mon", i_mon))
display(key_value_to_string("i_use", i_use))

# Move past detector sections to start of section 4
#sizeof int
s_int = 4
# sizeof float
s_flt = 4
sec4_pos = 2*s_int*i_mon + s_int*i_det + 2*s_flt*i_det + s_int*i_det + s_flt*i_det + s_flt*i_det*i_use
fid.seek(sec4_pos, SEEK_CUR)
display("")

# section 4
ver4 = bf.read_int32(fid)
display(key_value_to_string("ver4", ver4))
# skip spb
fid.seek(64*4, SEEK_CUR)
e_nse = bf.read_int32(fid)
display(key_value_to_string("e_nse", e_nse))
# skip se_struct
fid.seek(e_nse*32*4, SEEK_CUR)
display("")

# section 5
ver5 = bf.read_int32(fid)
display(key_value_to_string("ver5", ver5))
fid.seek(64*s_int + 5*s_int*i_det, SEEK_CUR)
display("")

# section 6
ver6 = bf.read_int32(fid)
display(key_value_to_string("ver6", ver6))
fid.seek(2*s_int, SEEK_CUR)
t_nper = bf.read_int32(fid)
display(key_value_to_string("t_nper", t_nper))
t_pmap = bf.read_int32(fid, 256)
display(key_value_to_string("t_pmap", t_pmap))
t_nsp1 = bf.read_int32(fid)
display(key_value_to_string("t_nsp1", t_nsp1))
t_ntc1 = bf.read_int32(fid)
display(key_value_to_string("t_ntc1", t_ntc1))

