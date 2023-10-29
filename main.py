# main.py
from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import process_commits, list_commits, \
    list_branches
from speckle_and_ai.db_handler import get_previous_results, setup_database
from speckle_and_ai.utilities import count_walls, count_rooms

def main_menu():
    while True:
        print("\n=== Speckle and AI Application ===")
        print("[1] Start")
        print("[2] View Previous Results")
        print("[3] Check")
        print("[4] Exit")
        print("=" * 35)

        choice = input("Please select an option (1/2/3/4): ")

        if choice == "1":
            # Authenticate client
            authenticate_client()

            # List available branches and ask user to select
            available_branches = list_branches()
            selected_branch_idx = input(
                f"Select a branch number (1-{len(available_branches)}): ")
            selected_branch = available_branches[int(selected_branch_idx) - 1]

            # List available commits from the selected branch and ask user to select
            available_commits = list_commits(selected_branch)
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
            if results:
                print("\n=== Previous Results ===")
                for result in results:
                    print("-" * 35)
                    print(f"Commit ID: {result[0]}")
                    print(f"Upload date: {result[1]}")
                    print(f"File name: {result[2]}")
                    print(f"Number of elements: {result[3]}")
                    print(f"Number of wall elements: {result[4]}")
                print("=" * 35)
            else:
                print("No previous results found.")

        elif choice == "3":
            results = get_previous_results()
            commits = list_commits(selected_branch)

            if not commits:
                print("No commits found.")
                continue

            selected_commit_idxs = input(
                "Choose commit numbers separated by commas (e.g., 1,3,5): \n").split(',')

            # Generate ASCII graph for selected commits
            max_elements = max(
                [getattr(commit, 'totalChildrenCount', 0) for commit in commits])

            print("\n=== Commit Summary ===")
            for idx in selected_commit_idxs:
                try:
                    commit_idx = int(idx) - 1
                    commit = commits[commit_idx]
                    bar_length = int(
                        (getattr(commit, 'totalChildrenCount', 0) / max_elements) * 50)
                    bar = '█' * bar_length
                    print("-" * 35)
                    print(f"Commit ID: {commit.id}")
                    print(f"Graph: {bar} ({getattr(commit, 'totalChildrenCount', 0)})")
                except (ValueError, IndexError):
                    print(f"Invalid commit number: {idx}")
            print("=" * 35)

        elif choice == "4":
            print("Exiting the program. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    setup_database()  # Ensure the database and table are set up
    main_menu()