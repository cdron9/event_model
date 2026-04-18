import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider

MAX_GUESTS = 500 
MIN_BAR_SPEND = 6000

## guest variables
acc_guests = np.arange(1, 501) 
min_spend_pp = (MIN_BAR_SPEND / acc_guests)

## drink variables 
## three groups
## non drinkers, averae drinkers, heavy drinkers 
## bell curve for distribution is most realistic. 
## 2 non drinkers, 6 average drinkers, 2 heavy drinkers. 
## £6 for beer, £8 for cocktail avg drink = £7 
## realistic average spend = (6*14 + 2*28)/10 = £14 per person
## now assuming 4 non drinkers, 2 light drinking, 1 average / heavy for the night
## bad case average spend = (5*6 + 1*12)/10 = £4.2 floor

## drink variables 
AVG_SPEND_PP = 14
FLOOR_SPEND_PP = 4.20

## we hit floor at above max attendance (VERY BAD)
## we hit avg around 450ish 

print(min_spend_pp[49])
print(min_spend_pp[99])
print(min_spend_pp[149])
print(min_spend_pp[249])
print(min_spend_pp[399])
print(min_spend_pp[499])
