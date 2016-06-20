import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

surface = np.ndfromtxt('surface.txt')
motion = np.ndfromtxt('motion.txt')

fig = plt.figure(figsize=(16, 6.6))

ax = fig.add_subplot(122, projection='3d')
ax.view_init(azim=180, elev=15)
ax.set_axis_off()
ax.zaxis.set_visible(False)
internal = ax.plot([0, 0], [0, 0])
vchimp = 0.149 * np.array([0, 0, 1])
vhuman = 0.108 * np.array([0, 2/3 * np.sqrt(2), -1/3])
vgorilla = 0.123 * np.array([np.sqrt(6) / 3, - 2 / (3 * np.sqrt(2)), -1/3])
vorang = 0.251 * np.array([- np.sqrt(6) / 3, - 2 / (3 * np.sqrt(2)), -1/3])
vzero = np.array([0, 0, 0])
vchimphuman = (vchimp + vhuman) / np.sqrt(2)
vchimporang = (vchimp + vorang) / np.sqrt(2)
vchimpgorilla = (vchimp + vgorilla) / np.sqrt(2)
chimp, = ax.plot(*zip(vzero, vchimp), 'k', lw=2)
human, = ax.plot(*zip(vzero, vhuman), 'k', lw=2)
gorilla, = ax.plot(*zip(vzero, vgorilla), 'k', lw=2)
orang, = ax.plot(*zip(vzero, vorang), 'k', lw=2)
inter, = ax.plot(*zip(vzero, vzero), 'k', lw=2)
labchimp = ax.text(*(vchimp * 1.1), 'C', size=24)
labhuman = ax.text(*(vhuman * 1.5), 'H', size=24)
labgorilla = ax.text(*(vgorilla * 1.5), 'G', size=24)
laborang = ax.text(*(vorang * 1.1), 'O', size=24)
ax.set_aspect('equal', 'datalim')
# ax.plot(*zip(vzero, vchimphuman), 'g')
# ax.plot(*zip(vzero, vchimporang), 'r')
# ax.plot(*zip(vzero, vchimpgorilla), 'b')
ax = fig.add_subplot(121, projection='3d')
ax.view_init(azim=30, elev=11)
ax.set_xticklabels([])
ax.set_yticklabels([])
for i, theta in enumerate((0, 2/3 * np.pi, 4/3 * np.pi), 1):
    ax.plot(surface[:,0] * np.cos(theta), surface[:,0] * np.sin(theta), surface[:,i], lw=2)
x, y, z = map(lambda x: [x], motion[0, :3])
sc = ax.scatter(x, y, z, 'k', c='k', s=64)
def frame(data):
    # global labchimp
    # global labhuman
    # global labgorilla
    # global laborang
    t = data[3]
    x = data[4]
    if t == 0:
        dv = x * vchimphuman / 2
        vc = vchimp + dv
        vh = vhuman + dv
        vg = vgorilla - dv
        vo = vorang - dv
        vch = dv
        vgo = -dv
        update = ((vc, vch, chimp), (vh, vch, human), (vg, vgo, gorilla), (vo, vgo, orang), (vch, vgo, inter))
    elif t == 1:
        dv = x * vchimporang / 2
        vc = vchimp + dv
        vh = vhuman - dv
        vg = vgorilla - dv
        vo = vorang + dv
        vco = dv
        vgh = -dv
        update = ((vc, vco, chimp), (vo, vco, orang), (vg, vgh, gorilla), (vh, vgh, human), (vco, vgh, inter))
    elif t == 2:
        dv = x * vchimpgorilla / 2
        vc = vchimp + dv
        vh = vhuman - dv
        vg = vgorilla + dv
        vo = vorang - dv
        vcg = dv
        vho = -dv
        update = ((vc, vcg, chimp), (vg, vcg, gorilla), (vh, vho, human), (vo, vho, orang), (vcg, vho, inter))
    for u, v, l in update:
        d = list(zip(u, v))
        l.set_data(d[:2])
        l.set_3d_properties(d[2])
    # labchimp.remove()
    # labhuman.remove()
    # labgorilla.remove()
    # laborang.remove()
    # labchimp = ax.text(*(vc * 1.1), 'C')
    # labhuman = ax.text(*(vh * 1.1), 'H')
    # labgorilla = ax.text(*(vg * 1.1), 'G')
    # laborang = ax.text(*(vo * 1.1), 'O')
    sc.set_offsets(data[:2])
    sc.set_3d_properties(data[2:3], 'z')
    return sc, chimp, human, gorilla, orang, inter, labchimp, labhuman, labgorilla, laborang
ax.set_aspect('equal', 'datalim')
fig.tight_layout(pad=0)
# frame(motion[0])
# plt.show()
ani = animation.FuncAnimation(fig, frame, motion, interval=50, blit=True)
ani.save('animation.mp4', bitrate=1000)
