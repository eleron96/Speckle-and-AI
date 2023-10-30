# main.py
from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import process_commits, list_commits, \
    list_branches, process_single_commit
from speckle_and_ai.db_handler import DatabaseHandler

db = DatabaseHandler()


def print_commit_summary_for_check(commit_data):
    """Print a simplified summary of the processed commit for the
    check option."""
    print(f"File name: {commit_data['file_name']}")
    print(f"Number of elements: {commit_data['object_count']}")
    print(f"Number of rooms: {commit_data['room_count']}")
    print("------------------------------")


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
                        selected_commits = [
                            available_commits[selected_commit_idx]]
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

        elif choice == "3":
            # List available branches and ask user to select
            available_branches = list_branches()
            selected_branch_idx = input(
                f"Select a branch number (1-{len(available_branches)}): ")
            selected_branch = available_branches[int(selected_branch_idx) - 1]
            commits = list_commits(selected_branch)
            if not commits:
                print("No commits found.")
                continue
            selected_commit_idxs = input(
                "Choose commit numbers separated by commas (e.g., 1,3,5): \n").split(
                ',')

            commit_datas = []
            for idx in selected_commit_idxs:
                try:
                    commit_idx = int(idx) - 1
                    commit = commits[commit_idx]
                    commit_data = process_single_commit(commit)
                    commit_datas.append(commit_data)
                    print_commit_summary_for_check(commit_data)
                except (ValueError, IndexError):
                    print(f"Invalid commit number: {idx}")

            # Находим коммит с самой последней датой
            latest_commit_data = max(commit_datas,
                                     key=lambda x: x['upload_date'])

            # Сравниваем комнаты каждого коммита с самым последним коммитом
            for commit_data in commit_datas:
                if commit_data['commit_id'] == latest_commit_data['commit_id']:
                    continue  # Пропускаем сравнение с самим собой

                # Сравниваем room_ids между коммитами
                added_rooms = set(latest_commit_data['room_ids']) - set(
                    commit_data['room_ids'])
                removed_rooms = set(commit_data['room_ids']) - set(
                    latest_commit_data['room_ids'])

                # Выводим разницу в количестве комнат
                if added_rooms:
                    print(
                        f"Added rooms from {commit_data['file_name']} compared to {latest_commit_data['file_name']}: {len(added_rooms)}")
                if removed_rooms:
                    print(
                        f"Removed rooms from {commit_data['file_name']} compared to {latest_commit_data['file_name']}: {len(removed_rooms)}")
                print("------------------------------")


        elif choice == "4":
            print("Exiting the program. Goodbye!")
            exit()

        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.")


if __name__ == "__main__":
    db.setup_database()  # Ensure the database and table are set up
    main_menu()