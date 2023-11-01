from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import list_commits, list_branches, \
    process_commits, process_single_commit

def check_uniqueness_across_branches():
    branches = list_branches()
    for branch in branches:
        commits = list_commits(branch)
        if commits:
            last_commit = commits[0]  # берем последний коммит
            process_single_commit(last_commit)

def print_commit_summary_for_check(commit_data):
    print(f"File name: {commit_data['file_name']}")
    print(f"Number of elements: {commit_data['object_count']}")
    print(f"Number of rooms: {commit_data['room_count']}")
    print("-" * 35)


def start_option():
    authenticate_client()
    available_branches = list_branches()
    selected_branch_idx = input(
        f"Select a branch number (1-{len(available_branches)}): ")
    selected_branch = available_branches[int(selected_branch_idx) - 1]
    available_commits = list_commits(selected_branch)
    selected_commit_idx = input(
        f"Select a commit number (1-{len(available_commits)}) or press Enter to process all: ")
    if selected_commit_idx:
        selected_commits = [available_commits[int(selected_commit_idx) - 1]]
        process_commits(selected_commits)
    else:
        process_commits(available_commits)


def check_option():
    # Authenticate client
    authenticate_client()

    # List available branches and ask user to select
    available_branches = list_branches()
    print("Select a branch number (1-{}): ".format(len(available_branches)))
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
