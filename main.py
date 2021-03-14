import skimage.color as color
import numpy as np
import matplotlib.pyplot as plt
import argparse
import middlebury_flow_read
def vector_len(x, ax=2):
    return np.sqrt(np.sum(x ** 2, axis=ax, keepdims=True))

def norm(x, ax=2):
    return x/(vector_len(x,ax) + 0.000001)

def dot_product(x,y):
    return np.sum(x*y,axis=2)

def Rad2Deg(x):
    return x * 180.0 / np.pi

"""
flow: numpy[H W 2]
"""
def visualize_flow(flow):
    h,w, _ = flow.shape
    norm_flow = norm(flow)
    base = np.ones_like(norm_flow)
    base[:,:,1] *= 0
    theta = np.arccos(dot_product(norm_flow, base)) * 180.0 / np.pi
    z = np.cross(flow, base)
    theta = theta * (z>=0) + (360.0-theta) * (z<0)

    # normal
    hue = theta / 360.0
    saturation = vector_len(flow)
    saturation = saturation * (saturation<=1)

    vis_flow = color.hsv2rgb(np.stack([hue, saturation[:,:,0], np.ones_like(hue)], axis=2))
    plt.imshow(vis_flow)
    plt.colorbar()
    plt.show()

parser = argparse.ArgumentParser(description='loss surface project')
parser.add_argument('--flow_path', default='flow10.flo', help='flow_path')
parser.add_argument('--max_flow', default=5, help='flow_path')
args = parser.parse_args()

visualize_flow(middlebury_flow_read.read_flow(args.flow_path, args.max_flow))
