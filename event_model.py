import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider
from scipy.stats import norm

## -------- CONSTANTS ---------

MAX_GUESTS    = 500 
MIN_BAR_SPEND = 6000
VENUE_COST    = 1500

## guest variables
acc_guests   = np.arange(1, 501) 
min_spend_pp = (MIN_BAR_SPEND / acc_guests)

## drink variables 
## three groups: non drinkers, average drinkers, heavy drinkers 
## bell curve for distribution is most realistic. 
## 2 non drinkers, 6 average drinkers, 2 heavy drinkers. 
## £6 for beer, £8 for cocktail, avg drink = £7 
## realistic average spend = (6*14 + 2*28)/10 = £14 per person
## bad case: 4 non drinkers, 5 light drinkers, 1 heavy
## bad case average spend = (5*6 + 1*12)/10 = £4.20 floor
AVG_SPEND_PP   = 14
FLOOR_SPEND_PP = 4.20
SENSITIVITY    = 0.05

## -------- CORE FUNCTIONS ---------

def exposure(min_bar_spend, avg_spend_pp, acc_guests):
    exposure = np.maximum(0, min_bar_spend - (avg_spend_pp * acc_guests))
    return exposure

## -------- INITIAL CALCULATIONS ---------

tab_cost_avgnight = exposure(MIN_BAR_SPEND, AVG_SPEND_PP, acc_guests)
tab_cost_badnight = exposure(MIN_BAR_SPEND, FLOOR_SPEND_PP, acc_guests)

## net position = ticket revenue - venue cost - bar exposure
## target is net >= 0, no profit needed
TICKET_PRICE = 15

net_avgnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_avgnight
net_badnight = (TICKET_PRICE * acc_guests) - VENUE_COST - tab_cost_badnight

## -------- PLOT SETUP ---------

fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)

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

## decayed spend display text
decay_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, verticalalignment='top',
                     fontsize=9, color='dimgray',
                     bbox=dict(boxstyle='round', facecolor='white', alpha=0.7))

## -------- SLIDERS ---------
## sliders — stacked at bottom with consistent spacing

ax_slider             = plt.axes([0.2, 0.25, 0.6, 0.03])
ax_slider_min_spend   = plt.axes([0.2, 0.20, 0.6, 0.03])
ax_slider_avg_spend   = plt.axes([0.2, 0.15, 0.6, 0.03])
ax_slider_sensitivity = plt.axes([0.2, 0.10, 0.6, 0.03])

slider             = Slider(ax_slider,             'Ticket Price (£)',             1,    30,  valinit=TICKET_PRICE)
slider_min_spend   = Slider(ax_slider_min_spend,   'Floor Spend Per-Person (£)',   4.50, 10,  valinit=FLOOR_SPEND_PP)
slider_avg_spend   = Slider(ax_slider_avg_spend,   'Average Spend Per-Person (£)', 10,   20,  valinit=AVG_SPEND_PP)
slider_sensitivity = Slider(ax_slider_sensitivity, 'Sensitivity (PED)',            0.01, 0.1, valinit=SENSITIVITY)

annot_avg = None
annot_bad = None

## -------- DECAY ---------
## cant use linear decay. if ticket price is low bar spend must assymetrically - to the decay - inflate due to basket theory. 
## avoiding modelling human decision making because how tf do i do that dynamically. 
## we need an exponential formula. 
## e^0 = 1, at £0 ticket price, then exponetnailly decay as exponent increases to 15... 
## PED: sensitivity is the elasticity coefficient. decay = baseline * e^(-sensitivity * ticket_price)

## -------- RISK CALCULATION ---------
## define shape of uncertainty for both attendance and spend
## attendance: normal distribution, mean ~300 (60% of 500), std ~65, range 175-450
## spend: normal distribution centred on slider baseline

def calculate_risk(ticket_price, sensitivity, att_mean, att_std, spend_mean, spend_std):
    ## 10,000 nights
    num_samples = 10000

    ## generate random nights and clip attendance to min and max
    sim_attendance = norm.rvs(loc=att_mean, scale=att_std, size=num_samples)
    sim_spend      = norm.rvs(loc=spend_mean, scale=spend_std, size=num_samples)
    sim_attendance = np.clip(sim_attendance, 0, 500)

    ## apply PED decay to sim spend
    decayed_sim_spend = sim_spend * np.exp(-sensitivity * ticket_price)

    ## get simulated exposure (same logic as exposure function)
    sim_exposure = np.maximum(0, MIN_BAR_SPEND - (decayed_sim_spend * sim_attendance))

    ## get simulated net position
    sim_net_pos = (ticket_price * sim_attendance) - VENUE_COST - sim_exposure

    risk_of_loss = np.sum(sim_net_pos < 0) / num_samples
    return risk_of_loss * 100 ## return as percentage

## -------- UPDATE ---------

def update(val):
    global annot_avg, annot_bad
    ticket_price = slider.val
    min_spend    = slider_min_spend.val
    avg_spend    = slider_avg_spend.val 
    sensitivity  = slider_sensitivity.val

    avg_spend_decayed = avg_spend * np.exp(-sensitivity * ticket_price)
    min_spend_decayed = min_spend * np.exp(-sensitivity * ticket_price)

    tab_cost_avgnight = exposure(MIN_BAR_SPEND, avg_spend_decayed, acc_guests)
    tab_cost_badnight = exposure(MIN_BAR_SPEND, min_spend_decayed, acc_guests)

    net_avgnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_avgnight
    net_badnight = (ticket_price * acc_guests) - VENUE_COST - tab_cost_badnight
    lines[0].set_ydata(net_avgnight)
    lines[1].set_ydata(net_badnight)

    ## run risk simulation with current slider values
    ## avg_spend used as spend mean so it responds to slider
    ## att_mean and att_std fixed — can be made into sliders later
    risk = calculate_risk(ticket_price, sensitivity,
                          att_mean=300, att_std=65,
                          spend_mean=14, spend_std=6)

    ## update decayed spend display
    decay_text.set_text(
        f'Decayed avg spend/pp:   £{avg_spend_decayed:.2f}\n'
        f'Decayed floor spend/pp: £{min_spend_decayed:.2f}\n'
        f'─────────────────────────\n'
        f'Risk of loss:           {risk:.1f}%'
    )

    ## use try and except to avoid breaking matplot - need to remember to set annot back to None to avoid crashing due to global
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

## -------- CONNECT & RUN ---------

slider.on_changed(update)
slider_min_spend.on_changed(update)
slider_avg_spend.on_changed(update)
slider_sensitivity.on_changed(update)

update(None)
plt.show()