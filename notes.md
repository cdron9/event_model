# Event Pricing Model

## KEY INFO
- £1,500 venue cost
- Ticketed event
- Max occupancy: 500 persons
- Minimum spend at venue: £6,000
- Exposure to paying the remaining excess of the min spend must be MINIMAL

---

## CORE ISSUE
As attendance drops:
- Ticket revenue falls **linearly** (fewer people × same price)
- Required min spend per person rises **non-linearly** (£6,000 ÷ attendance gets steep fast at low numbers)

---

## OBSERVATIONS

Using common sense: when I go out, if I spend more on a ticket, I spend less on drinks.

Technically: there is a **negative correlation between ticket price and spend per person**.

This is complicated to model because it is not objectively guaranteed — just assumed but quite probable.

There is a compounding risk in this model that isn't immediately obvious:

- Higher ticket price → lower bar spend per person
- Lower bar spend → higher exposure to bar minimum shortfall
- Higher exposure → requires compounding ticket price increases to compensate

It's a nasty circle. Kind of like needing experience to get an entry level job.

### Budget Substitution
Spend per person can be modelled as a function of ticket price using **exponential decay** — this represents the economic concept of **budget substitution**: two goods competing for the same wallet.

At low ticket prices, bar spend is near baseline. As ticket price rises, bar spend decays exponentially. Sensitivity controls the steepness of this decay.

---

## MODEL APPROACH

### Monte Carlo Simulation
Rather than reading a single breakeven line, the model runs thousands of simulated nights by sampling from probability distributions for both attendance and spend per person. This gives a **probability of breaking even** at any given set of pricing assumptions.

#### Attendance Distribution
- Normal distribution
- Central estimate: ~300 guests (60% of max occupancy)
- Realistic range: 175–450 guests
- Standard deviation: ~65 guests

#### Spend Per Person Distribution
- Normal distribution centred on slider baseline values
- Separate distributions for average and floor spend scenarios
- Spread TBD — reflects natural variance in how much individuals drink on a given night

#### Sensitivity
- Controls the steepness of exponential decay in spend per person as ticket price rises
- Hard to calibrate without real data — accurate modelling would require significant historical data or ML
- Treated as an adjustable assumption rather than a fixed parameter

---

## LIMITATIONS
- Decay sensitivity is a best guess — real calibration requires event data
- Human decision making around spend is inherently unpredictable
- Model is a planning tool, not a guarantee