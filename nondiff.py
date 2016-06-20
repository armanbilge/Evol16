import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib2tikz import save as tikz_save

surface = np.ndfromtxt('surface.txt')[:100,:]
fig = plt.figure()

ax = fig.add_subplot(111, projection='3d')
ax.view_init(azim=30, elev=11)
ax.set_xticklabels([])
ax.set_yticklabels([])
for i, theta in enumerate((0, 2/3 * np.pi, 4/3 * np.pi), 1):
    ax.plot(surface[:,0] * np.cos(theta), surface[:,0] * np.sin(theta), surface[:,i], lw=2)
ax.set_aspect('equal', 'datalim')
fig.tight_layout(pad=0)
fig.savefig('nondiff.pdf')