from neopixel import *

# Define colors which are available for the wcd. Currenly: Alphabetic order
BLACK = Color(  0,  0,  0)
BLUE  = Color(  0,  0,255)
GREEN = Color(  0,255,  0)
PINK  = Color(255,  0,170)
RED   = Color(255,  0,  0)
WHITE = Color(255,255,255)
WWHITE= Color(255,255, 50) # Warm white
YELLOW= Color(255,255,  0)
ORANGE= Color(212,165,  25)

# Summarize colors: [BLACK->WHITE, RED->BLUE (rainbow)]
colors= [BLACK, WHITE, WWHITE, RED, YELLOW, GREEN, BLUE]
num_of_colors = len(colors)
