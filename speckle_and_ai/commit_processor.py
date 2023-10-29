from .config import client, STREAM_ID
from .utilities import count_walls, count_rooms
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from .db_handler import save_result

def process_commits(commits_to_process=None):
    if not commits_to_process:
        commits_to_process = client.commit.list(STREAM_ID)

    for commit in commits_to_process:
        transport = ServerTransport(client=client, stream_id=STREAM_ID)
        res = operations.receive(commit.referencedObject, transport)

        upload_date = getattr(commit, 'createdAt', None)
        file_name = getattr(commit, 'message', None)
        object_count = getattr(res, 'totalChildrenCount', None)

        wall_count = count_walls(res)
        room_count = count_rooms(res)  # Count rooms

        save_result(commit.id, upload_date, file_name, object_count, wall_count)

        print(f"Commit ID: {commit.id}")
        print(f"Upload date: {upload_date}")
        print(f"File name: {file_name}")
        print(f"Number of elements: {object_count}")
        print(f"Number of wall elements: {wall_count}")
        print(f"Number of rooms: {room_count}")  # Print room count
        print("------------------------------")
        return res

def process_commits_checks(commits_to_process=None):
    if not commits_to_process:
        commits_to_process = client.commit.list(STREAM_ID)

    for commit in commits_to_process:
        transport = ServerTransport(client=client, stream_id=STREAM_ID)
        res = operations.receive(commit.referencedObject, transport)

        upload_date = getattr(commit, 'createdAt', None)
        file_name = getattr(commit, 'message', None)
        object_count = getattr(res, 'totalChildrenCount', None)

        wall_count = count_walls(res)
        room_count = count_rooms(res)  # Count rooms

        save_result(commit.id, upload_date, file_name, object_count, wall_count)

        print(f"File name: {file_name}")
        print(f"Number of elements: {object_count}")
        print(f"Number of rooms: {room_count}\n")  # Print room count
        return res

def list_commits(branch_name):
    commits = client.commit.list(STREAM_ID)
    filtered_commits = [commit for commit in commits if getattr(commit, 'branchName', '') == branch_name]
    for idx, commit in enumerate(filtered_commits):
        print(
            f"[{idx + 1}] "
            f"File name: {getattr(commit, 'message', 'Unknown')}, "
            f"Upload date: {getattr(commit, 'createdAt', 'Unknown')}, "
            f"Commit ID: {commit.id}")
    return filtered_commits





def list_branches():
    # Используйте Speckle API для получения списка веток.
    branches = client.branch.list(STREAM_ID)
    for idx, branch in enumerate(branches):
        print(f"[{idx + 1}] {branch.name}")
    return [branch.name for branch in branches]
