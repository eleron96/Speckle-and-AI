from speckle_and_ai.commit_utilities import check_option, \
    display_project_info, check_potential_matches, \
    check_last_commit_section_names, check_area_discrepancy
from speckle_and_ai.db_utilities import view_previous_results_option
from speckle_and_ai.menu_utilities import display_main_menu, get_user_choice
from rich.console import Console

console = Console()



def main_menu():
    try:
        while True:
            display_main_menu()
            choice = get_user_choice()

            if choice == "1":
                check_option()
            elif choice == "2":
                console.clear()
                view_previous_results_option()
            elif choice == "3":
                console.clear()
                display_project_info()
            elif choice == "4":
                console.clear()
                check_potential_matches()
            elif choice == "5":
                console.clear()
                check_last_commit_section_names()
            elif choice == "6":
                console.clear()
                check_area_discrepancy()
            elif choice.lower() == "exit":
                print("Exiting the program. Goodbye!")
                exit()
            else:
                print("Invalid choice. Please select a valid option.")
    except KeyboardInterrupt:
        print("\nПрограмма была прервана пользователем. Выход.")


if __name__ == "__main__":
    main_menu()
