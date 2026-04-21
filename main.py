import matplotlib.pyplot as plt
import numpy as np
from model import (acc_guests, MIN_BAR_SPEND, VENUE_COST,
                   AVG_SPEND_PP, FLOOR_SPEND_PP, TICKET_PRICE,
                   exposure, ped_decay)
from sliders import create_sliders

## ─── PLOT SETUP ──────────────────────────────────────────────────────────────

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

tab_cost_avgnight = exposure(MIN_BAR_SPEND, AVG_SPEND_PP, acc_guests)
tab_cost_badnight = exposure(MIN_BAR_SPEND, FLOOR_SPEND_PP, acc_guests)

net_avgnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_avgnight
net_badnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_badnight

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

## live decayed spend display
decay_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top',
                     fontsize=9, color='dimgray',
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

## ─── SLIDERS ─────────────────────────────────────────────────────────────────

slider, slider_min_spend, slider_avg_spend, slider_sensitivity = create_sliders()

## ─── STATE ───────────────────────────────────────────────────────────────────

annot_avg = None
annot_bad = None

## ─── UPDATE FUNCTION ─────────────────────────────────────────────────────────

## cant use linear decay. if ticket price is low bar spend must assymetrically - to the decay - inflate due to basket theory. 
## avoiding modelling human decision making because how tf do i do that dynamically. 
## we need an exponential formula. 
## e^0 = 1, at £0 ticket price, then exponentially decay as exponent increases...
## PED: sensitivity is the elasticity coefficient. decay = baseline * e^(-sensitivity * ticket_price)

def update(val):
    global annot_avg, annot_bad

    ticket_price = slider.val
    min_spend    = slider_min_spend.val
    avg_spend    = slider_avg_spend.val 
    sensitivity  = slider_sensitivity.val

    avg_spend_decayed = ped_decay(avg_spend, sensitivity, ticket_price)
    min_spend_decayed = ped_decay(min_spend, sensitivity, ticket_price)

    tab_cost_avgnight = exposure(MIN_BAR_SPEND, avg_spend_decayed, acc_guests)
    tab_cost_badnight = exposure(MIN_BAR_SPEND, min_spend_decayed, acc_guests)
    net_avgnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_avgnight
    net_badnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_badnight

    lines[0].set_ydata(net_avgnight)
    lines[1].set_ydata(net_badnight)

    decay_text.set_text(
        f'Decayed avg spend/pp:   £{avg_spend_decayed:.2f}\n'
        f'Decayed floor spend/pp: £{min_spend_decayed:.2f}'
    )

    ## use try/except to avoid matplotlib crash on annotation removal
    ## must reset to None after remove to avoid stale reference on next call
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

## ─── CONNECT & RUN ───────────────────────────────────────────────────────────

slider.on_changed(update)
slider_min_spend.on_changed(update)
slider_avg_spend.on_changed(update)
slider_sensitivity.on_changed(update)

update(None)
plt.show()