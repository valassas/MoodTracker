#Three lines to make our compiler able to draw:
import sys
import matplotlib.pyplot as plt
import numpy as np

#plot 1:

plt.subplot(1, 2, 1)
plt.grid( axis='y',color = 'green', linestyle = '--', linewidth = 0.5)
plt.title("Sports Watch Data")
plt.xlabel("Days")
plt.ylabel("Hours slept")

#plot 2:

plt.subplot(1, 2, 2)
plt.plot(marker='o')
plt.grid( axis='y',color = 'green', linestyle = '--', linewidth = 0.5)
plt.title("Sports Watch Data")
plt.xlabel("Days")
plt.ylabel("steps walked")

 

 

plt.suptitle("GRAPHS")
plt.show()

#Two lines to make our compiler able to draw:
plt.savefig(sys.stdout.buffer)
sys.stdout.flush()