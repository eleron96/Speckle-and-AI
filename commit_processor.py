# commit_processor.py
from config import client, STREAM_ID
from utilities import count_walls
from specklepy.api import operations
from specklepy.transports.server import ServerTransport
from db_handler import save_result


def process_commits(commits_to_process=None):
    if not commits_to_process:
        commits_to_process = client.commit.list(STREAM_ID)

    # Iterate through each commit in the commits_to_process list
    for commit in commits_to_process:
        # Create an authenticated server transport from the client and get the commit object
        transport = ServerTransport(client=client, stream_id=STREAM_ID)
        res = operations.receive(commit.referencedObject, transport)

        # Extract data
        upload_date = getattr(commit, 'createdAt', None)
        file_name = getattr(commit, 'message', None)
        object_count = getattr(res, 'totalChildrenCount', None)

        # Attempt to count "wall" elements
        wall_count = count_walls(res)

        # Save the results to the database
        save_result(commit.id, upload_date, file_name, object_count, wall_count)

        # Output data
        print(f"Commit ID: {commit.id}")
        print(f"Upload date: {upload_date}")
        print(f"File name: {file_name}")
        print(f"Number of elements: {object_count}")
        print(f"Number of wall elements: {wall_count}")
        print("------------------------------")


def list_commits():
    commits = client.commit.list(STREAM_ID)
    for idx, commit in enumerate(commits):
        print(
            f"[{idx + 1}] Commit ID: {commit.id}, Upload date: {getattr(commit, 'createdAt', 'Unknown')}, File name: {getattr(commit, 'message', 'Unknown')}")
    return commits
