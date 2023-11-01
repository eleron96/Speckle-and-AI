from speckle_and_ai.config import STREAM_ID
from speckle_and_ai.menu_utilities import display_main_menu, get_user_choice
from speckle_and_ai.commit_utilities import start_option, check_option, \
    check_uniqueness_across_branches, check_room_name_uniqueness, \
    check_uniqueness_in_branch
from speckle_and_ai.db_utilities import view_previous_results_option

def main_menu():
    while True:
        display_main_menu()
        choice = get_user_choice()

        if choice == "1":
            start_option()
        elif choice == "2":
            view_previous_results_option()
        elif choice == "3":
            check_option()
        elif choice == "4":
            check_uniqueness_across_branches()
        elif choice == "5":
            print("Exiting the program. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")

if __name__ == "__main__":
    main_menu()
