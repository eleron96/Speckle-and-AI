from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import list_commits, list_branches, \
    process_single_commit, process_commits
from speckle_and_ai.db_handler import DatabaseHandler

db = DatabaseHandler()


def print_commit_summary_for_check(commit_data):
    print(f"File name: {commit_data['file_name']}")
    print(f"Number of elements: {commit_data['object_count']}")
    print(f"Number of rooms: {commit_data['room_count']}")
    print("-" * 35)


def start_option():
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
                return  # Return to the menu after processing
            else:
                print("Invalid selection. Try again.")
                return
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

    # If no specific commit was selected, process all
    process_commits(available_commits)


def view_previous_results_option():
    # Display previous results from the database
    results = db.get_previous_results()
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


def check_option():
    # Authenticate client
    authenticate_client()

    # List available branches and ask user to select
    available_branches = list_branches()
    print("Select a branch number (1-{}): ".format(len(available_branches)))
    for i, branch in enumerate(available_branches, 1):
        print(f"[{i}] {branch}")
    selected_branch_idx = input()
    selected_branch = available_branches[int(selected_branch_idx) - 1]

    # List available commits from the selected branch and ask user to select
    available_commits = list_commits(selected_branch)
    if not available_commits:
        print("No commits found for the selected branch.")
        return

    for i, commit in enumerate(available_commits, 1):
        print(
            f"[{i}] File name: {commit.message}, Upload date: {commit.createdAt}, Commit ID: {commit.id}")

    selected_commit_idxs = input(
        "Select commit numbers separated by commas (e.g., 1,3,5) or press Enter to process all: ").split(
        ',')

    selected_commits = []
    for idx in selected_commit_idxs:
        try:
            commit_idx = int(idx) - 1
            selected_commits.append(available_commits[commit_idx])
        except (ValueError, IndexError):
            print(f"Invalid commit number: {idx}")

    for idx, commit in enumerate(selected_commits, 1):
        commit_data = process_single_commit(commit)
        print_commit_summary_for_check(commit_data)


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
            start_option()
        elif choice == "2":
            view_previous_results_option()
        elif choice == "3":
            check_option()
        elif choice == "4":
            print("Exiting the program. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    db.setup_database()  # Ensure the database and table are set up
    main_menu()
