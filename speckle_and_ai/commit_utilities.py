import re

from specklepy.api import operations
from specklepy.transports.server import ServerTransport

from speckle_and_ai.authentication import authenticate_client
from speckle_and_ai.commit_processor import (
    list_commits, list_branches, process_commits, process_single_commit,
    get_commits, print_commit_summary, print_total_summary
)
from speckle_and_ai.config import client, STREAM_ID
from speckle_and_ai.extract_check_area_discrepancy import \
    extract_check_area_discrepancy
from speckle_and_ai.section_name_extractor import \
    extract_section_name_from_rooms

from rich.console import Console
from rich.progress import Progress
from rich.table import Table

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


def identify_alphabets(text):
    if text is None:
        return 'Undefined'
    alphabets = set()
    for char in text:
        if re.match('[а-яА-Я]', char):
            alphabets.add('Cyrillic')
        elif re.match('[a-zA-Z]', char):
            alphabets.add('Latin')
    return ', '.join(alphabets) if alphabets else 'Undefined'


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

    error_messages = set()
    for name in room_names:
        matches = potential_matches(name, room_names.keys())
        for match in matches:
            sorted_names = sorted([name, match])
            error_message = f"\033[91m\033[1m{sorted_names[0]} и {sorted_names[1]} - Potential matches\033[0m"
            error_messages.add(error_message)

    for error_message in error_messages:
        print(error_message)


def potential_matches(name, all_names):
    matches = []
    for other_name in all_names:
        # Check if either name is None
        if name is None or other_name is None:
            continue  # Skip if either is None

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
    console = Console()
    all_commits = []
    branches = list_branches(print_to_console=False)
    for branch in branches:
        commits = get_commits(branch)
        if commits:
            all_commits.append(commits[0])

    room_names = {}
    with Progress(console=console, expand=True) as progress:
        task = progress.add_task("[green]Processing commits...",
                                 total=len(all_commits))
        for commit in all_commits:
            commit_data = process_single_commit(commit)
            room_types = commit_data.get("room_types", {})
            for room_type, count in room_types.items():
                room_names[room_type] = 1
            progress.update(task, advance=1)

    checked_pairs = set()
    found_matches = False

    alphabet_table = Table(show_header=True, header_style="bold cyan")
    alphabet_table.add_column("Room name", style="bold", width=20)
    alphabet_table.add_column("Alphabets", style="dim")

    console.print("\n[bold]Check for the use of alphabets:[/bold]")
    for name in room_names:
        alphabet_info = identify_alphabets(name)
        # Применяем условную логику для стилизации
        if "Latin" in alphabet_info:
            alphabet_info = alphabet_info.replace("Latin",
                                                  "[green]Latin[/green]")
        if "Cyrillic" in alphabet_info:
            alphabet_info = alphabet_info.replace("Cyrillic",
                                                  "[red]Cyrillic[/red]")
        alphabet_table.add_row(name, alphabet_info)
    console.print(alphabet_table)

    console.print("\n[bold]Check for potential name matches:[/bold]")
    matches_table = Table(show_header=True, header_style="bold magenta")
    matches_table.add_column("Name 1", style="dim", width=12)
    matches_table.add_column("Name 2", style="dim", width=12)
    matches_table.add_column("Status", justify="right")

    for name in room_names:
        matches = potential_matches(name, room_names.keys())
        for match in matches:
            if (name, match) not in checked_pairs and (
            match, name) not in checked_pairs:
                matches_table.add_row(name, match, "Potential matches")
                found_matches = True
                checked_pairs.add((name, match))

    if found_matches:
        console.print(matches_table)
    else:
        console.print("[green bold]Not detected[/green bold]")


def display_project_info():
    """Display project information."""
    all_commits_data = []
    branches = list_branches(print_to_console=False)
    for branch in branches:
        commits = get_commits(branch)
        if commits:
            latest_commit = commits[0]
            commit_data = process_single_commit(latest_commit)
            all_commits_data.append(commit_data)
            print_commit_summary(commit_data, branch)

    print_total_summary(all_commits_data)


def check_last_commit_section_names():
    branches = list_branches(print_to_console=False)
    console = Console()
    output_messages = []

    with Progress() as progress:
        task = progress.add_task("[green]Checking branches...",
                                 total=len(branches))

        for branch in branches:
            if branch.lower() == "main":
                progress.advance(task)
                continue

            output_messages.append(f"Checking branch: [bold green]{branch}[/]")

            commits = get_commits(branch_name=branch)
            if not commits:
                output_messages.append(f"No commits found for branch: {branch}")
                progress.advance(task)
                continue

            commits.sort(key=lambda x: getattr(x, 'createdAt', None),
                         reverse=True)
            last_commit = commits[0]

            try:
                transport = ServerTransport(client=client, stream_id=STREAM_ID)
                res = operations.receive(last_commit.referencedObject,
                                         transport)
                room_section = extract_section_name_from_rooms(res)

                if len(room_section) > 1:
                    message = "[red]Warning: more than 1 value in the corpus:[/]\n" \
                              "[red]Corpus section short:[/]"
                    for section in room_section:
                        message += f"\n[red]{section}[/]"
                    output_messages.append(message)
                else:
                    for section in room_section:
                        output_messages.append(
                            f"Corpus section short: {section}")
            except Exception as e:
                output_messages.append(
                    f"Error while extracting section name: {e}")

            output_messages.append("-" * 40)
            progress.advance(task)

    for message in output_messages:
        console.print(message)


console = Console()


def check_area_discrepancy():
    branches = list_branches(print_to_console=False)
    discrepancy_reports = []

    with Progress() as progress:
        task1 = progress.add_task("[cyan]Processing branches...",
                                  total=len(branches))

        for branch in branches:
            if branch.lower() == "main":
                progress.advance(task1)
                continue

            commits = get_commits(branch_name=branch)
            if not commits:
                progress.advance(task1)
                continue

            commits.sort(key=lambda x: getattr(x, 'createdAt', None),
                         reverse=True)
            last_commit = commits[0]

            try:
                # Теперь передаем stream_id вместе с last_commit и client
                transport = ServerTransport(client=client, stream_id=STREAM_ID)
                res = operations.receive(last_commit.referencedObject,
                                         transport)
                room_section = extract_check_area_discrepancy(res)
                discrepancy_reports.append((branch,
                                            getattr(last_commit, 'message',
                                                    None), room_section))
            except Exception as e:
                discrepancy_reports.append(
                    (branch, "Corpus section short: " + str(e), None))

            progress.advance(task1)

    # После обработки всех веток, выводим собранную информацию
    for branch, commit_message, rooms in discrepancy_reports:
        console.print(f"Checking branch: [bold green]{branch}[/bold green]")
        console.print(f"Commit Message: [bold]{commit_message}[/bold]",
                      style="bold green")
        if rooms:
            print_discrepancy_rooms(rooms, commit_message)
        else:
            console.print("The rooms have been mapped", style="bold green")
        console.print("-" * 40)


def print_discrepancy_rooms(discrepancy_rooms, commit_message):
    if discrepancy_rooms:
        console.print("The rooms have not been mapped!", style="bold red")
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("№", style="dim")
        table.add_column("Rooms", style="dim")
        table.add_column("Name")
        table.add_column("Area in Revit")
        table.add_column("Rounded Area")
        table.add_column("Level")
        table.add_column("Room Number")

        for index, room in enumerate(discrepancy_rooms, start=1):
            table.add_row(
                str(index),
                f"{room['id']}",
                f"{room['name']}",
                f"{room['area']}",
                f"{room['rounded_area']}",
                f"{room['level_name']}",
                f"{room['room_number']}"
            )
        console.print(table)


def check_residential_areas():
    """This is a placeholder for the inspection of residential premises"""
    console = Console()
    console.print("This is a placeholder for the inspection of residential premises.")
