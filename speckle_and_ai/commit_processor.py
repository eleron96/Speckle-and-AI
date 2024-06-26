from specklepy.api import operations
from specklepy.transports.server import ServerTransport

from .config import client, STREAM_ID
from .db_handler import DatabaseHandler
from .room_utilities import count_rooms

db = DatabaseHandler()


def get_commits(branch_name=None):
    """Retrieve commits. If branch_name is provided, filter by branch."""
    limit = 100
    commits = client.commit.list(STREAM_ID, limit=limit)

    if branch_name:
        commits = [commit for commit in commits if
                   getattr(commit, 'branchName', '') == branch_name]

    return commits


def print_total_summary(all_commits_data):
    total_elements = sum(
        commit_data['object_count'] for commit_data in all_commits_data)
    total_rooms = sum(
        commit_data['room_count'] for commit_data in all_commits_data)

    # Собираем информацию о типах квартир
    total_room_types = {}
    for commit_data in all_commits_data:
        for room_type, count in commit_data['room_types'].items():
            total_room_types[room_type] = total_room_types.get(room_type,
                                                               0) + count

    print(f"{'Overall Total:':-^35}")
    print(f"{'Number of elements:':<25} {total_elements}")
    print(f"{'Number of rooms:':<25} {total_rooms}")
    print(f"{'Apartment Types':-^35}")
    for room_type, count in total_room_types.items():
        print(f"{room_type} - {count}")
    print("******************************")


def process_single_commit(commit):
    """Process a single commit and return its data."""
    transport = ServerTransport(client=client, stream_id=STREAM_ID)
    res = operations.receive(commit.referencedObject, transport)
    upload_date = getattr(commit, 'createdAt', None)
    file_name = getattr(commit, 'message', None)
    object_count = getattr(res, 'totalChildrenCount', None)
    room_count, room_ids, room_types = count_rooms(res)

    db.save_result(commit.id, upload_date, file_name, object_count)

    return {
        "commit_id": commit.id,
        "upload_date": upload_date,
        "file_name": file_name,
        "object_count": object_count,
        "room_count": room_count,
        "room_types": room_types,
        "room_ids": room_ids
    }

def process_commits(commits_to_process=None):
    """Process multiple commits."""
    if not commits_to_process:
        commits_to_process = get_commits()

    results = []
    for commit in commits_to_process:
        result = process_single_commit(commit)
        results.append(result)
        print_commit_summary(result)

    return results


def print_commit_summary(commit_data, branch_name):
    print(f"\033[1;32m{'Branch name:':<25} {branch_name}\033[0m")
    print(f"{'File name:':<25} {commit_data['file_name']}")
    print(f"{'Commit ID:':<25} {commit_data['commit_id']}")
    print(f"{'Upload date:':<25} {commit_data['upload_date']}")
    print(f"{'Number of elements:':<25} {commit_data['object_count']}")
    print(f"{'Number of rooms:':<25} {commit_data['room_count']}")
    print("-" * 20)


def list_commits(branch_name, print_to_console=True):
    """List commits for a specific branch."""
    commits = get_commits(branch_name)
    if print_to_console:
        for idx, commit in enumerate(commits):
            print(
                f"[{idx + 1}] "
                f"File name: {getattr(commit, 'message', 'Unknown')}, "
                f"Upload date: {getattr(commit, 'createdAt', 'Unknown')}, "
                f"Commit ID: {commit.id}"
            )
    return commits


def list_branches(print_to_console=True):
    """List available branches."""
    branches = client.branch.list(STREAM_ID)
    if print_to_console:
        for idx, branch in enumerate(branches):
            print(f"[{idx + 1}] {branch.name}")
    return [branch.name for branch in branches]
