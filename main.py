from speckle_and_ai.commit_utilities import check_option, \
    display_project_info, check_potential_matches
from speckle_and_ai.db_utilities import view_previous_results_option
from speckle_and_ai.menu_utilities import display_main_menu, get_user_choice


def main_menu():

    while True:
        display_main_menu()
        choice = get_user_choice()

        if choice == "1":
            check_option()
        elif choice == "2":
            view_previous_results_option()
        elif choice == "3":
            display_project_info()
        elif choice == "4":
            check_potential_matches()
        elif choice.lower() == "exit":
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main_menu()
