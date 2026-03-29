# log4a copied from Reality (from https://github.com/tsing-xl/Reality). 
# Oringinal name: log4r

from colorama import init, Fore, Style
from os import name

# Init colorama.
init(
    # Reset the color style automatic.
    autoreset = True if name == 'nt' else False, 

    # If windows, colorama will use another color system.
    wrap = False if name == 'nt' else False, 
)

__lvl__: tuple = (
    Fore.LIGHTBLUE_EX + 'Infomation', 
    Fore.LIGHTBLACK_EX + 'Suggestion', 
    Fore.YELLOW + 'Warning', 
    Fore.LIGHTRED_EX + 'Error', 
    Fore.RED + 'Fatal', 
    Fore.MAGENTA + 'Debug', 
)

def logout(
        from_module: str = 'Anonymous', 
        record_level: int = 0, 
        recordings: str = '', 
    ) -> None: 

    print(
        f'{__lvl__[min(record_level, 5)]}: \
{Style.RESET_ALL}{recordings}\
{Fore.LIGHTBLACK_EX} (From {from_module})'
    )