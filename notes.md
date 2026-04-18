*firstly.* 

## KEY INFO.
- £1500 venue cost
- ticketed event
- max occupancy: 500 persons 
- min spend at venue: £6,000
- exposure to paying the remaining excess of the min spend must be MINIMAL 


## AN ASIDE. 
Id be happy to build a shitty ticketing platform so you dont have to pay to have one hosted. woudl just be a database i can link to excel or something, stripe for payment and confrmation, and just like event info on the site too. can automate emails going out to attendees also if you want. its all possible, there may be cost in doing that. I dont want any money just in terms of using Stripes API, web hosting, and email domain also. wouldnt be expensive though i dont think. 

## CORE ISSUE.
As attendance drops:
Ticket revenue falls linearly (fewer people × same price)
Required min spend per person rises NOT linearly (6000 ÷ attendance = gets steep fast at low numbers)

## OBSERVATIONS.
basically using common sense: when i go out, if i spend more on a ticket, i spend less on drinks. 

this idea labelled technically: there is a negative correlation between ticket price and spend per person. 

now, this is complicated to model becasue it not objectively 'garaunteed' just assumed but quite probable. 
theres basically a compounding risk in this model that isnt currently captured. 
- higher ticket price -> lower bar spend per person
- lower bar spend -> higher exposure to bar minimum shortfall
- higher exposure -> requires compounding ticket price.
its a nasty circle. kidna like needing experience to get an entry level job. 

### actually having thought about this for 5 mins more. I can model spend per person as a function of ticket price. linear decay would work well just to simply represent this. 
this represents 'budget substitution' according to my best friend claude. it is the economic concept of two goods competing for the same wallet. cool. 



