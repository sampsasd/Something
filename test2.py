import matplotlib.pyplot as plt
import numpy as np
from time import sleep

thiccboi = [0, 5, 10, 40, 80]
fatboi = [1.062, 1.619, 2.138, 4.138, 4.375]

plt.plot(thiccboi, fatboi, c='mediumorchid')
plt.xlabel('Thicc / ug/cm2')
plt.ylabel("Conversion area / i don't fucking know")
plt.tight_layout()
plt.show()