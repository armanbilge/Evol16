import os
import numpy as np
from matplotlib import style
from matplotlib import pyplot as plt
from matplotlib2tikz import save as tikz_save

style.use('seaborn-poster')

data = np.ndfromtxt('acceptance.txt')
fig = plt.figure(facecolor='white')

L = len(data[:,0])
plt.plot(range(0, L), data[:,])
plt.xlabel('leap-prog step')
plt.ylabel('acceptance probability')

fig.tight_layout()
tikz_save('tmp', show_info=False)
with open('tmp') as f:
    i = 0
    for l in f:
        l = l.strip()
        if 'addplot' in l:
            i += 1
        if i == 2 and 'addplot' in l:
            print('\\only<2>{')
            j = l.find('[')
        if i == 2 and 'table' in l:
            l = 'table[row sep=crcr] {%'
        if i == 2 and all(x not in l for x in ('addplot', ';')):
            l += '\\\\'
        print(l)
        if i == 2 and ';' in l:
            print('}')
            i = 3
os.remove('tmp')