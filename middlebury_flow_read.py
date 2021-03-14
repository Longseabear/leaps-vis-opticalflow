import numpy as np
import struct
import matplotlib.pyplot as plt
TAG_FLOAT = 202021.25

def read_flow(path, disp_max=10):
    with open(path, 'rb') as f:
        tag = struct.unpack('f', f.read(4))[0]
        if tag != TAG_FLOAT:
            raise Exception('tag miss match, you must to check your os binary read system')
        w,h = struct.unpack("<2I", f.read(8))
        flow = np.frombuffer(f.read(),dtype='<f4').reshape(h,w,2).copy()
    flow /= disp_max
    np.clip(flow, -1, 1)
    return flow

