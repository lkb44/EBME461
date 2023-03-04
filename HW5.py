import numpy as np
import matplotlib.pyplot as plt

# Define the input image
img = np.array([[1, 3, 1, 5, 6],
                [2, 4, 2, 8, 7],
                [3, 1, 5, 4, 3],
                [8, 7, 8, 2, 5],
                [5, 3, 1, 7, 4]])

# Define the dimensions of the image
nrows, ncols = img.shape

# Define the cost matrix
cost = np.zeros((nrows, ncols))

# Define the previous matrix
prev = np.zeros((nrows, ncols), dtype=int)

# Compute the cumulative edge costs
for i in range(1, nrows):
    for j in range(ncols):
        if j == 0:
            candidates = [cost[i-1, j], cost[i-1, j+1]]
        elif j == ncols - 1:
            candidates = [cost[i-1, j-1], cost[i-1, j]]
        else:
            candidates = [cost[i-1, j-1], cost[i-1, j], cost[i-1, j+1]]
        min_cost = np.min(candidates)
        prev[i, j] = np.argmin(candidates) - 1
        cost[i, j] = min_cost + np.abs(img[i, j] - img[i-1, j+prev[i, j]])

# Backtrack to find the optimal path
path = [(nrows-1, np.argmin(cost[-1]))]
for i in range(nrows-2, -1, -1):
    j = path[-1][1] + prev[i+1, path[-1][1]]
    path.append((i, j))

# Plot the results
plt.imshow(img, cmap='gray')
for i in range(nrows):
    for j in range(ncols):
        if i < nrows-1:
            plt.plot([j, j-1, j+1], [i+1, i, i], 'b', alpha=0.1)
plt.plot([j for _, j in path], [i for i, _ in path], 'r')
plt.show()

