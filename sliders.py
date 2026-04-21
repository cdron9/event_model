import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from model import AVG_SPEND_PP, FLOOR_SPEND_PP, TICKET_PRICE, SENSITIVITY

def create_sliders():
    ax_slider             = plt.axes([0.2, 0.25, 0.6, 0.03])
    ax_slider_min_spend   = plt.axes([0.2, 0.20, 0.6, 0.03])
    ax_slider_avg_spend   = plt.axes([0.2, 0.15, 0.6, 0.03])
    ax_slider_sensitivity = plt.axes([0.2, 0.10, 0.6, 0.03])

    slider             = Slider(ax_slider,             'Ticket Price (£)',             1,    30,  valinit=TICKET_PRICE)
    slider_min_spend   = Slider(ax_slider_min_spend,   'Floor Spend Per-Person (£)',   4.50, 10,  valinit=FLOOR_SPEND_PP)
    slider_avg_spend   = Slider(ax_slider_avg_spend,   'Average Spend Per-Person (£)', 10,   20,  valinit=AVG_SPEND_PP)
    slider_sensitivity = Slider(ax_slider_sensitivity, 'Sensitivity (PED)',            0.01, 0.1, valinit=SENSITIVITY)

    return slider, slider_min_spend, slider_avg_spend, slider_sensitivity