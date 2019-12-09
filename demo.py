import numpy as np
import matplotlib.pyplot as plt
from baseline_corrector import baseline_removal

# draws a spikey curve
x = np.linspace(0,10,200)
y = 5*np.sin(x)*np.cos(x**(1.5)) + x
y = np.abs(y)

y_nobase = baseline_removal(y)

plt.plot(x,y,'r',label='y')
plt.plot(x,y_nobase,'b',label='y sans baseline')
plt.legend()
plt.show()

