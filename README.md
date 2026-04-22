# Event Pricing Model

## Overview

This project models the financial viability of hosting a ticketed event at a venue with a **minimum bar spend requirement**. The goal is to minimize the risk of financial loss by balancing ticket prices, attendance, and bar spend per person. The model uses **exponential decay** to simulate the relationship between ticket price and bar spend, and a **Monte Carlo simulation** to estimate the probability of breaking even under various scenarios.

For detailed notes and observations, refer to the notes.md file.

---

## Key Features

### 1. **Core Parameters**
The model is built around the following constants:

```python
MAX_GUESTS    = 500 
MIN_BAR_SPEND = 6000
VENUE_COST    = 1500
TICKET_PRICE  = 15
```

These parameters define the venue's constraints:
- **Max Guests**: 500 (venue capacity)
- **Minimum Bar Spend**: £6,000
- **Venue Cost**: £1,500
- **Ticket Price**: Adjustable via slider (default £15)

---

### 2. **Exponential Decay for Bar Spend**
The model assumes a **negative correlation between ticket price and bar spend per person**, implemented using an **exponential decay formula**:

```python
avg_spend_decayed = avg_spend * np.exp(-sensitivity * ticket_price)
min_spend_decayed = min_spend * np.exp(-sensitivity * ticket_price)
```

This formula reflects the economic concept of **budget substitution**, where higher ticket prices reduce bar spend. The **sensitivity slider** controls the steepness of this decay, representing the **price elasticity of demand (PED)**.

For more details on this concept, see the **Budget Substitution** section in notes.md.

---

### 3. **Monte Carlo Simulation**
The model uses a **Monte Carlo simulation** to estimate the **risk of financial loss**. This involves generating random samples for attendance and bar spend per person, based on normal distributions:

```python
sim_attendance = norm.rvs(loc=att_mean, scale=att_std, size=num_samples)
sim_spend      = norm.rvs(loc=spend_mean, scale=spend_std, size=num_samples)
sim_attendance = np.clip(sim_attendance, 0, 500)
```

The simulation calculates the **net position** for 10,000 simulated nights and determines the percentage of nights where the event incurs a loss:

```python
sim_exposure = np.maximum(0, MIN_BAR_SPEND - (decayed_sim_spend * sim_attendance))
sim_net_pos = (ticket_price * sim_attendance) - VENUE_COST - sim_exposure
risk_of_loss = np.sum(sim_net_pos < 0) / num_samples
```

---

### 4. **Dynamic Visualization**
The model provides a **real-time plot** of the net position for two scenarios:
- **Average Night**: Based on average spend per person.
- **Bad Night**: Based on floor spend per person.

The plot updates dynamically as sliders are adjusted:

```python
lines = [
    ax.plot(acc_guests, net_avgnight, label='Net position - avg night')[0],
    ax.plot(acc_guests, net_badnight, label='Net position - bad night')[0]
]
```

The breakeven points for both scenarios are annotated on the plot:

```python
breakeven_avg_idx = np.where(np.diff(np.sign(net_avgnight)))[0]
breakeven_bad_idx = np.where(np.diff(np.sign(net_badnight)))[0]
if len(breakeven_avg_idx) > 0:
    x_avg = acc_guests[breakeven_avg_idx[0]]
    annot_avg = ax.annotate(f'Avg breakeven: {x_avg} guests', (x_avg, 0))
```

---

### 5. **Risk of Loss Display**
The model displays the **risk of financial loss** and the decayed spend per person directly on the plot:

```python
decay_text.set_text(
    f'Decayed avg spend/pp:   £{avg_spend_decayed:.2f}\n'
    f'Decayed floor spend/pp: £{min_spend_decayed:.2f}\n'
    f'─────────────────────────\n'
    f'Risk of loss:           {risk:.1f}%'
)
```

---

## Probability Distributions

The model relies on **normal distributions** for both attendance and spend per person. For more information on probability distributions and their applications, refer to the prob_dist_notes.txt file.

---

## Limitations

As noted in notes.md, the model has several limitations:
- **Sensitivity** is an estimated parameter due to the lack of historical data.
- **Human decision-making** around spend is inherently unpredictable.
- The model is a **planning tool**, not a guarantee of financial outcomes.

---

## How to Use

1. **Run the Script**: Execute the Python script to launch the interactive plot.
2. **Adjust Sliders**: Use the sliders to modify ticket price, spend assumptions, and sensitivity.
3. **Analyze Results**: Observe the breakeven points, net positions, and risk of loss.

---

## Future Improvements

Potential enhancements include:
- Adding sliders for attendance mean and standard deviation.
- Modelling the impact of ticket price on attendance.
- Incorporating additional probability distributions (e.g., binomial or Poisson).

For more ideas, see the **Other Questions** section in notes.md.