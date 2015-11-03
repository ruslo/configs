# Copyright (c) 2013, Ruslan Baratov
# All rights reserved.

# Bash colors
# https://wiki.archlinux.org/index.php/Color_Bash_Prompt#List_of_colors_for_prompt_and_Bash

# Reset
export COLOR_OFF=$(print -P '\e[0m')       # Text Reset

# Regular Colors
export COLOR_BLACK=$(print -P '\e[0;30m')        # Black
export COLOR_RED=$(print -P '\e[0;31m')          # Red
export COLOR_GREEN=$(print -P '\e[0;32m')        # Green
export COLOR_YELLOW=$(print -P '\e[0;33m')       # Yellow
export COLOR_BLUE=$(print -P '\e[0;34m')         # Blue
export COLOR_PURPLE=$(print -P '\e[0;35m')       # Purple
export COLOR_CYAN=$(print -P '\e[0;36m')         # Cyan
export COLOR_WHITE=$(print -P '\e[0;37m')        # White

# Bold (B)
export COLOR_B_BLACK=$(print -P '\e[1;30m')       # Black
export COLOR_B_RED=$(print -P '\e[1;31m')         # Red
export COLOR_B_GREEN=$(print -P '\e[1;32m')       # Green
export COLOR_B_YELLOW=$(print -P '\e[1;33m')      # Yellow
export COLOR_B_BLUE=$(print -P '\e[1;34m')        # Blue
export COLOR_B_PURPLE=$(print -P '\e[1;35m')      # Purple
export COLOR_B_CYAN=$(print -P '\e[1;36m')        # Cyan
export COLOR_B_WHITE=$(print -P '\e[1;37m')       # White

# Underline (U)
export COLOR_U_BLACK=$(print -P '\e[4;30m')       # Black
export COLOR_U_RED=$(print -P '\e[4;31m')         # Red
export COLOR_U_GREEN=$(print -P '\e[4;32m')       # Green
export COLOR_U_YELLOW=$(print -P '\e[4;33m')      # Yellow
export COLOR_U_BLUE=$(print -P '\e[4;34m')        # Blue
export COLOR_U_PURPLE=$(print -P '\e[4;35m')      # Purple
export COLOR_U_CYAN=$(print -P '\e[4;36m')        # Cyan
export COLOR_U_WHITE=$(print -P '\e[4;37m')       # White

# Background (ON)
export COLOR_ON_BLACK=$(print -P '\e[40m')       # Black
export COLOR_ON_RED=$(print -P '\e[41m')         # Red
export COLOR_ON_GREEN=$(print -P '\e[42m')       # Green
export COLOR_ON_YELLOW=$(print -P '\e[43m')      # Yellow
export COLOR_ON_BLUE=$(print -P '\e[44m')        # Blue
export COLOR_ON_PURPLE=$(print -P '\e[45m')      # Purple
export COLOR_ON_CYAN=$(print -P '\e[46m')        # Cyan
export COLOR_ON_WHITE=$(print -P '\e[47m')       # White

# High Intensity (HI)
export COLOR_HI_BLACK=$(print -P '\e[0;90m')       # Black
export COLOR_HI_RED=$(print -P '\e[0;91m')         # Red
export COLOR_HI_GREEN=$(print -P '\e[0;92m')       # Green
export COLOR_HI_YELLOW=$(print -P '\e[0;93m')      # Yellow
export COLOR_HI_BLUE=$(print -P '\e[0;94m')        # Blue
export COLOR_HI_PURPLE=$(print -P '\e[0;95m')      # Purple
export COLOR_HI_CYAN=$(print -P '\e[0;96m')        # Cyan
export COLOR_HI_WHITE=$(print -P '\e[0;97m')       # White

# Bold High Intensity (BHI)
export COLOR_BHI_BLACK=$(print -P '\e[1;90m')      # Black
export COLOR_BHI_RED=$(print -P '\e[1;91m')        # Red
export COLOR_BHI_GREEN=$(print -P '\e[1;92m')      # Green
export COLOR_BHI_YELLOW=$(print -P '\e[1;93m')     # Yellow
export COLOR_BHI_BLUE=$(print -P '\e[1;94m')       # Blue
export COLOR_BHI_PURPLE=$(print -P '\e[1;95m')     # Purple
export COLOR_BHI_CYAN=$(print -P '\e[1;96m')       # Cyan
export COLOR_BHI_WHITE=$(print -P '\e[1;97m')      # White

# High Intensity backgrounds (ON_BHI)
export COLOR_ON_BHI_IBLACK=$(print -P '\e[0;100m')   # Black
export COLOR_ON_BHI_IRED=$(print -P '\e[0;101m')     # Red
export COLOR_ON_BHI_IGREEN=$(print -P '\e[0;102m')   # Green
export COLOR_ON_BHI_IYELLOW=$(print -P '\e[0;103m')  # Yellow
export COLOR_ON_BHI_IBLUE=$(print -P '\e[0;104m')    # Blue
export COLOR_ON_BHI_IPURPLE=$(print -P '\e[10;95m')  # Purple
export COLOR_ON_BHI_ICYAN=$(print -P '\e[0;106m')    # Cyan
export COLOR_ON_BHI_IWHITE=$(print -P '\e[0;107m')   # White
