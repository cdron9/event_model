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
SENSITIVITY = 0.5

## we hit floor at above max attendance (VERY BAD)
## we hit avg around 450ish 

def exposure(min_bar_spend, avg_spend_pp, acc_guests):
    exposure = np.maximum(0, min_bar_spend - (avg_spend_pp * acc_guests))
    return exposure

tab_cost_avgnight = exposure(MIN_BAR_SPEND, AVG_SPEND_PP, acc_guests)
tab_cost_badnight = exposure(MIN_BAR_SPEND, FLOOR_SPEND_PP, acc_guests)

## net position = ticket revenue - venue cost - bar exposure
## target is net >= 0, no profit needed
TICKET_PRICE = 15

net_avgnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_avgnight
net_badnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_badnight

## plot
fig, ax = plt.subplots()

lines = [
    ax.plot(acc_guests, net_avgnight, label='Net position - avg night')[0],
    ax.plot(acc_guests, net_badnight, label='Net position - bad night')[0]
]

ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
ax.set_xlabel('Number of guests')
ax.set_ylabel('Net Position (£)')
ax.set_title('Net Position vs Attendance')
ax.legend()
ax.set_ylim(-8000, 8000)

## slider
plt.subplots_adjust(bottom=0.25)
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])
slider = Slider(ax_slider, 'Ticket Price (£)', 1, 30, valinit=TICKET_PRICE)

## slider for avg and floor spend 
## Floor spend 
plt.subplots_adjust(bottom=0.15)
ax_slider_min_spend = plt.axes([0.2, 0.2, 0.6, 0.03])
slider_min_spend = Slider(ax_slider_min_spend, 'Floor Spend Per-Person (£)', 4.50, 10, valinit=FLOOR_SPEND_PP)

## Avg spend
plt.subplots_adjust(bottom=0.05)
ax_slider_avg_spend = plt.axes([0.2, 0.3, 0.6, 0.03])
slider_avg_spend = Slider(ax_slider_avg_spend, 'Average Spend Per-Person (£)', 10, 20, valinit=AVG_SPEND_PP )

##slider for sensitivity
plt.subplots_adjust(bottom=0.00)
ax_slider_sensitivity = plt.axes([0.2, 0.4, 0.6, 0.03])
slider_sensitivity = Slider(ax_slider_sensitivity, 'Sensitivity', 0.2, 0.8, valinit=SENSITIVITY)


annot_avg = None
annot_bad = None

## implement linear decay to simulate basket theory 

## sensutivity for PED (will be a slider for live aadjustments)
##sensitivity = 1
##def basket_theory_decay():
    ## linear decay 
    ## y = C - mt 
    ## || avg_spend_pp = AVG_SPEND_PP - (sensitivity * ticket_price)
    ##avg_spend_pp = AVG_SPEND_PP - (sensitivity * ticket_price)

def update(val):
    global annot_avg, annot_bad
    ticket_price = slider.val
    min_spend = slider_min_spend.val
    avg_spend = slider_avg_spend.val 
    sensitivity = slider_sensitivity.val
    avg_spend_decayed = avg_spend - (sensitivity * ticket_price)
    min_spend_decayed = min_spend - (sensitivity * ticket_price)
    tab_cost_avgnight = exposure(MIN_BAR_SPEND, avg_spend_decayed, acc_guests)
    tab_cost_badnight = exposure(MIN_BAR_SPEND, min_spend_decayed, acc_guests)
    net_avgnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_avgnight
    net_badnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_badnight
    lines[0].set_ydata(net_avgnight)
    lines[1].set_ydata(net_badnight)

## use try and except to avoid breaking matplot - need to remember to set annot back to None to avoid crashing due to glbal

    if annot_avg is not None:
        try:
            annot_avg.remove()
        except ValueError:
            pass
        annot_avg = None

    if annot_bad is not None:
        try:
            annot_bad.remove()
        except ValueError:
            pass 
        annot_bad = None

    breakeven_avg_idx = np.where(np.diff(np.sign(net_avgnight)))[0]
    breakeven_bad_idx = np.where(np.diff(np.sign(net_badnight)))[0]

    if len(breakeven_avg_idx) > 0:
        x_avg = acc_guests[breakeven_avg_idx[0]]
        annot_avg = ax.annotate(f'Avg breakeven: {x_avg} guests', (x_avg, 0))
    if len(breakeven_bad_idx) > 0:
        x_bad = acc_guests[breakeven_bad_idx[0]]
        annot_bad = ax.annotate(f'Bad breakeven: {x_bad} guests', (x_bad, 0))

    fig.canvas.draw_idle()

    print(avg_spend_decayed)
    print(min_spend_decayed)

slider.on_changed(update)
slider_min_spend.on_changed(update)
slider_avg_spend.on_changed(update)
slider_sensitivity.on_changed(update)


plt.show()