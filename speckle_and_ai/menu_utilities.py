from rich.console import Console
from rich.panel import Panel


def display_main_menu():
    """Display the main menu options using rich."""
    console = Console()
    menu_items = [
        "[1] Commit Info",
        "[2] View Previous Results",
        "[3] Project Info",
        "[4] Check Potential Matches of Room Names",
        "[5] Check Last Commit Section Names",
        "[6] Check area discrepancy",
        "[7] Inspection of residential premises",
        "Type 'exit' to exit the program",
    ]

    # Создаем панель с заголовком и меню
    menu_panel = Panel("\n".join(menu_items),
                       title="Speckle and AI Application",
                       subtitle="Main Menu",
                       expand=False)

    console.print(menu_panel)


def get_user_choice():
    console = Console()
    return console.input("Please choose an option: ")
