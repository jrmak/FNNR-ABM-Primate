import numpy as np
import numpy.random
import matplotlib.pyplot as plt

# Create data
x = np.random.randn(4096)
y = np.random.randn(4096)

# Create heatmap
heatmap, xedges, yedges = np.histogram2d(x, y, bins=(640, 640))
extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

# Plot heatmap
plt.clf()
plt.title('Pythonspot.com heatmap example')
plt.ylabel('y')
plt.xlabel('x')
plt.imshow(heatmap, extent=extent)
plt.show()