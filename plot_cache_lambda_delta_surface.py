from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
import numpy as np


Z = np.genfromtxt("AIC_cache_delta_lambda.csv", delimiter=",")[1:, 1:]
x = np.arange(0.0, 1.01, 0.01)
y = np.arange(0.01, 1.01, 0.01)

fig = plt.figure()
ax = fig.gca(projection='3d')
X, Y = np.meshgrid(x, y)
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

fig.colorbar(surf, shrink=0.5, aspect=5)

ax.set_xlabel("$\delta$")
ax.set_ylabel("$\lambda$")

plt.show()
