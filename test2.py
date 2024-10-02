import matplotlib.pyplot as plt
import numpy as np
from time import sleep

thiccboi = [0, 4.96, 10.035, 20.18, 29.74, 41.42, 88.06]
fatboi = [1.062, 1.619, 2.138, 2.685, 3.662, 4.138, 4.375]

plt.scatter(thiccboi, fatboi, c='deepskyblue')
plt.xlabel('Surface density / ug/cm$^{2}$')
plt.ylabel("Area of conversion dist")
plt.tight_layout()
plt.show()