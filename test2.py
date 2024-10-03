import matplotlib.pyplot as plt
import numpy as np
from time import sleep

thiccboi = [0, 4.96, 10.035, 20.18, 29.74, 41.42, 88.06, 155.8]
fatboi = [1.062e-8, 1.619e-8, 2.138e-8, 2.685e-8, 3.662e-8, 4.138e-8, 4.375e-8, 5.672e-8]

plt.scatter(thiccboi, fatboi, c='deepskyblue')
plt.xlabel('Surface density / $\mathrm{\mu}$g/cm$^{2}$')
plt.ylabel("Sum of angle dist / W")
plt.tight_layout()
plt.show()