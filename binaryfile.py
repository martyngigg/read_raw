"""Utility functions for reading binary data. The type mappings are for C
"""
import numpy as _np
import struct as _struct

# Sizes of different types in bytes
DATA_SIZES = {
    'char': 1,
    'float32': 4,
    'float64': 8,
    'int32': 4,
    'int64': 8
}

# Format character required for struct module
FORMAT_CHAR = {
    'char': 'c',
    'float32': 'f',
    'float64': 'd',
    'int32': 'i',
    'int64': 'q'
}

def read_string(fid, length=None):
    """Read a string. If length is None then assume that the file current points at an
    int32 that indicates the size of the string"""
    if length is None:
        length = read_int32(fid)
    return ''.join(read_data(fid, 'char', n=length))

def read_2d_string_array_matlab(fid, shape):
    """Read a 2D chracter array of the given shape. The shape is interpreted
    as (ncols, nrows) and the strings are joined down the columns and
    converted into a flat array of strings
    """
    ncols, nrows = shape[0], shape[1]
    bytes = read_data(fid, 'char', n=ncols*nrows)
    flattened = []
    for i in range(ncols):
        col_str = []
        for j in range(nrows):
            col_str.append(bytes[j*ncols + i])
        flattened.append(''.join(col_str))
    return flattened

def read_int32(fid, n=1):
    """Read an int32 from the file"""
    return read_data(fid, 'int32', n=n)

def read_int64(fid, n=1):
    """Read an int64 from the file"""
    return read_data(fid, 'int64', n=n)

def read_float32(fid, n=1):
    """Read an float32 from the file"""
    return read_data(fid, 'float32', n=n)

def read_2d_float32_array_matlab(fid, shape):
    ncols, nrows = shape[0], shape[1]
    matrix = _np.array(read_float32(fid, n=ncols*nrows))
    # Treat as Fortran ordered
    return matrix.reshape(shape, order='F')

def read_float64(fid, n=1):
    """Read an float64 from the file"""
    return read_data(fid, 'float64', n=1)

def read_data(fid, typename, n=1):
    """Main workhorse to read bytes from a file
    and unpack them as a tuple in the format defined by the struct module
    """
    if type(n) is not int:
        raise ValueError("Expected number of bytes as an int, found '{}'".format(type(n)))
    try:
        bytes =  _struct.unpack(n*FORMAT_CHAR[typename], fid.read(n*DATA_SIZES[typename]))
        if n == 1:
            bytes = bytes[0]
        return bytes

    except KeyError, ex:
        raise RuntimeError("Unknown data type: '{}'".format(typename))
