import numpy as np
import matplotlib.pyplot as plt
# generate a 30-by-50 array of random numbers
x = np.random.rand(30, 50)
# the following code that will plot the numbers as colors would normally
# be hidden from you, so again, you won't have to worry about it.
# try clicking the 'Plot' button to see the outcome.
plt.figure(figsize=(3,5))
plt.axis('off')
plt.imshow(x, cmap='Set3')