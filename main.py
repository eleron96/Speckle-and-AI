# main.py
from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import process_commits, list_commits
from speckle_and_ai.db_handler import get_previous_results, setup_database


def main_menu():
    while True:
        print("\nMain Menu:")
        print("[1] Start")
        print("[2] View Previous Results")
        print("[3] Exit")

        choice = input("Please select an option (1/2/3): ")

        if choice == "1":
            # Authenticate client
            authenticate_client()

            # List available commits and ask user to select
            available_commits = list_commits()
            selected_commit_idx = input(
                f"Select a commit number (1-{len(available_commits)}) or press Enter to process all: ")

            if selected_commit_idx:
                try:
                    selected_commit_idx = int(selected_commit_idx) - 1
                    if 0 <= selected_commit_idx < len(available_commits):
                        selected_commits = [available_commits[selected_commit_idx]]
                        process_commits(selected_commits)
                        continue  # Return to the menu after processing
                    else:
                        print("Invalid selection. Try again.")
                        continue
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue

            # If no specific commit was selected, process all
            process_commits(available_commits)

        elif choice == "2":
            # Display previous results from the database
            results = get_previous_results()
            for result in results:
                print(f"\nCommit ID: {result[0]}")
                print(f"Upload date: {result[1]}")
                print(f"File name: {result[2]}")
                print(f"Number of elements: {result[3]}")
                print(f"Number of wall elements: {result[4]}")
                print("------------------------------")

        elif choice == "3":
            print("Exiting the program. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    setup_database()  # Ensure the database and table are set up
    main_menu()
