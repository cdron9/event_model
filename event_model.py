import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider

MAX_GUESTS = 500 
MIN_BAR_SPEND = 6000

## guest variables
acc_guests = np.arange(1, 501) 
min_spend_pp = (MIN_BAR_SPEND / acc_guests)

print(min_spend_pp[49])
print(min_spend_pp[99])
print(min_spend_pp[149])
print(min_spend_pp[249])
print(min_spend_pp[399])
print(min_spend_pp[499])
