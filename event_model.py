import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider

MAX_GUESTS = 500 
MIN_BAR_SPEND = 6000
VENUE_COST = 1500

## guest variables
acc_guests = np.arange(1, 501) 
min_spend_pp = (MIN_BAR_SPEND / acc_guests)

## drink variables 
## three groups: non drinkers, average drinkers, heavy drinkers 
## bell curve for distribution is most realistic. 
## 2 non drinkers, 6 average drinkers, 2 heavy drinkers. 
## £6 for beer, £8 for cocktail, avg drink = £7 
## realistic average spend = (6*14 + 2*28)/10 = £14 per person
## bad case: 4 non drinkers, 5 light drinkers, 1 heavy
## bad case average spend = (5*6 + 1*12)/10 = £4.20 floor
AVG_SPEND_PP = 14
FLOOR_SPEND_PP = 4.20

## we hit floor at above max attendance (VERY BAD)
## we hit avg around 450ish 

def exposure(min_bar_spend, avg_spend_pp, acc_guests):
    exposure = np.maximum(0, min_bar_spend - (avg_spend_pp * acc_guests))
    return exposure

tab_cost_avgnight = exposure(MIN_BAR_SPEND, AVG_SPEND_PP, acc_guests)
tab_cost_badnight = exposure(MIN_BAR_SPEND, FLOOR_SPEND_PP, acc_guests)

## net position = ticket revenue - venue cost - bar exposure
## target is net >= 0, no profit needed
TICKET_PRICE = 10

net_avgnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_avgnight
net_badnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_badnight

## plot
fig, ax = plt.subplots()

ax.plot(acc_guests, net_avgnight, label='Net position - avg night')
ax.plot(acc_guests, net_badnight, label='Net position - bad night')
ax.axhline(0, color='black', linewidth=0.8, linestyle='--')

ax.set_xlabel('Number of guests')
ax.set_ylabel('Net Position (£)')
ax.set_title('Net Position vs Attendance')
ax.legend()
ax.set_ylim(-8000, 8000)

plt.show()