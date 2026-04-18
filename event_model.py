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

def exposure(min_bar_spend, avg_spend_pp, acc_guests):
    exposure = np.maximum(0, min_bar_spend - (avg_spend_pp * acc_guests))
    return exposure

tab_cost_avgnight = exposure(MIN_BAR_SPEND, AVG_SPEND_PP, acc_guests)
tab_cost_badnight = exposure(MIN_BAR_SPEND, FLOOR_SPEND_PP, acc_guests)

## min ticket price is set to make exposure == 0, we could adjust so there is some exposure just set to a controllable amount. 
min_ticket_price_avgnight = (tab_cost_avgnight * VENUE_COST) / acc_guests
min_ticket_price_badnight = (tab_cost_badnight * VENUE_COST) / acc_guests

## plot via matplotlib. 
fig, ax = plt.subplots()

ax.plot(acc_guests, min_ticket_price_avgnight, label='Min ticket price - avg night')
ax.plot(acc_guests, min_ticket_price_badnight, label='Min ticket price - bad night')

ax.set_xlabel('Number of guests')
ax.set_ylabel('Ticket Price (£)')
ax.set_title('Minimum Ticket Price vs Attendance')
ax.legend()

ax.set_ylim(0,30)

plt.show()