import numpy as np

## ─── CONSTANTS ───────────────────────────────────────────────────────────────

MAX_GUESTS    = 500 
MIN_BAR_SPEND = 6000
VENUE_COST    = 1500

## ─── ASSUMPTIONS ─────────────────────────────────────────────────────────────

## Drinker distribution (bell curve approximation):
## 2 non-drinkers, 6 average drinkers, 2 heavy drinkers per 10 people
## £6 beer, £8 cocktail → avg drink £7
## Avg spend: (6×14 + 2×28) / 10 = £14 per person
## Bad case: 4 non-drinkers, 5 light, 1 heavy
## Bad case spend: (5×6 + 1×12) / 10 = £4.20

AVG_SPEND_PP   = 14
FLOOR_SPEND_PP = 4.20
TICKET_PRICE   = 15

## PED sensitivity: elasticity coefficient for exponential decay of bar spend vs ticket price
## hard to calibrate without data — treated as an adjustable assumption
SENSITIVITY    = 0.05

## ─── GUEST RANGE ─────────────────────────────────────────────────────────────

acc_guests   = np.arange(1, MAX_GUESTS + 1) 
min_spend_pp = (MIN_BAR_SPEND / acc_guests)

## ─── CORE FUNCTIONS ──────────────────────────────────────────────────────────

def exposure(min_bar_spend, avg_spend_pp, acc_guests):
    ## exposure = shortfall between min bar spend and actual bar revenue
    return np.maximum(0, min_bar_spend - (avg_spend_pp * acc_guests))

def calculate_net(ticket_price, avg_spend_pp, acc_guests):
    tab_cost = exposure(MIN_BAR_SPEND, avg_spend_pp, acc_guests)
    return (ticket_price * acc_guests) - VENUE_COST - tab_cost

def ped_decay(baseline_spend, sensitivity, ticket_price):
    ## PED exponential decay on spend per person
    ## decay = baseline * e^(-sensitivity * ticket_price)
    return baseline_spend * np.exp(-sensitivity * ticket_price)