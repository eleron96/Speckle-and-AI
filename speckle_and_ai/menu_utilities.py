def display_main_menu():
    """Display the main menu options."""
    menu_width = 40

    print("\n" + " Speckle and AI Application ".center(menu_width, "="))
    print("[1]".ljust(4) + "Commit Info".ljust(menu_width - 4))
    print("[2]".ljust(4) + "View Previous Results".ljust(menu_width - 4))
    print("[3]".ljust(4) + "Project Info".ljust(menu_width - 4))
    print("[4]".ljust(4) + "Check Potential Matches of Room Names".ljust(
        menu_width - 4))
    print("[5]".ljust(4) + "Check Last Commit Section Names".ljust(
        menu_width - 4))
    print("[6]".ljust(4) + "Check area discrepancy".ljust(
        menu_width - 4))
    print("Type 'exit' to exit the program".ljust(menu_width))
    print("=" * menu_width)


def get_user_choice():
    return input()
