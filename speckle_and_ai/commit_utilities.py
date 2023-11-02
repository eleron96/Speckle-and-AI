from tqdm import tqdm

from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import list_commits, list_branches, \
    process_commits, process_single_commit, get_commits, print_commit_summary, \
    print_total_summary


confusing_letters = {
    'a': 'а',
    'o': 'о',
    'e': 'е',
    'p': 'р',
    'c': 'с',
    'k': 'к',
    'x': 'х',
    'B': 'В',
    'M': 'М',
    'H': 'Н',
    'K': 'К',
    'X': 'Х',
    'A': 'А',
    'O': 'О',
    'P': 'Р',
    'C': 'С',
    'T': 'Т',
    'E': 'Е'
}


def check_room_name_uniqueness():
    all_commits = []
    branches = list_branches(print_to_console=False)
    for branch in branches:
        commits = get_commits(branch)
        all_commits.extend(commits)

    room_names = {}
    for commit in all_commits:
        commit_data = process_single_commit(commit)
        room_types = commit_data.get("room_types", {})
        for room_type, count in room_types.items():
            room_names[room_type] = 1

    error_messages = set()  # Используем множество для хранения уникальных
    # сообщений об ошибках
    for name in room_names:
        matches = potential_matches(name, room_names.keys())
        for match in matches:
            # Убедимся, что сообщение добавляется в множество только один раз
            sorted_names = sorted([name, match])
            error_message = f"\033[91m\033[1m{sorted_names[0]} и {sorted_names[1]} - потенциальные совпадения\033[0m"
            error_messages.add(error_message)  # Добавляем сообщение в множество

    for error_message in error_messages:
        print(error_message)


def potential_matches(name, all_names):
    matches = []
    for other_name in all_names:
        if other_name != name and len(name) == len(other_name):
            is_potential_match = False
            for i in range(len(name)):
                if name[i] in confusing_letters and confusing_letters[
                    name[i]] == other_name[i]:
                    is_potential_match = True
                    break
                elif other_name[i] in confusing_letters and confusing_letters[
                    other_name[i]] == name[i]:
                    is_potential_match = True
                    break
            if is_potential_match:
                matches.append(other_name)
    return matches


def print_commit_summary_for_check(commit_data):
    print(f"\033[1;32m\n{'File name:':<25} {commit_data['file_name']}\033[0m")
    print(f"{'Number of elements:':<25} {commit_data['object_count']}")
    print(f"{'Number of rooms:':<25} {commit_data['room_count']}")
    print("-" * 35)


def start_option():
    authenticate_client()
    available_branches = list_branches()
    selected_branch_idx = input(
        f"Select a branch number (1-{len(available_branches)}): ")
    selected_branch = available_branches[int(selected_branch_idx) - 1]
    available_commits = list_commits(selected_branch)
    selected_commit_idx = input(
        f"Select a commit number (1-{len(available_commits)}) or press Enter "
        f"to process all: ")
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

    selected_commit_idxs = input(
        "Select commit numbers separated by commas (e.g., 1,3,5): ").split(
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


def check_potential_matches():
    """Check for potential room name matches across the latest commits of all
    branches."""
    all_commits = []
    branches = list_branches(print_to_console=False)
    for branch in branches:
        # Получаем только последний коммит каждой ветки
        commits = get_commits(branch)
        if commits:
            all_commits.append(commits[0])

    room_names = {}
    for commit in tqdm(all_commits, desc="", ncols=70,
                       bar_format="Processing commits: {bar}| {percentage:3.0f}%"):
        commit_data = process_single_commit(commit)
        room_types = commit_data.get("room_types", {})
        for room_type, count in room_types.items():
            room_names[room_type] = 1

    checked_pairs = set()
    found_matches = False

    for name in room_names:
        matches = potential_matches(name, room_names.keys())
        for match in matches:
            if (name, match) not in checked_pairs and (
                    match, name) not in checked_pairs:
                print()
                print(
                    f"\033[91m\033[1m{name} и {match} - потенциальные "
                    f"совпадения\033[0m")
                found_matches = True
                checked_pairs.add((name, match))

    if not found_matches:
        print("\033[92m\033[1mПотенциальные совпадения не обнаружены\033[0m")


def display_project_info():
    """Display project information."""
    all_commits_data = []
    branches = list_branches(print_to_console=False)
    for branch in branches:
        commits = get_commits(branch)
        if commits:  # проверяем, есть ли коммиты в этом branch
            latest_commit = commits[0]  # берем последний commit
            commit_data = process_single_commit(latest_commit)
            all_commits_data.append(commit_data)
            print_commit_summary(commit_data, branch)

    print_total_summary(all_commits_data)
