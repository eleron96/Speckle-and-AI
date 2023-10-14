# from specklepy.api import operations
# from specklepy.api.client import SpeckleClient
# from specklepy.api.credentials import get_default_account
# from specklepy.transports.server import ServerTransport
#
# # Replace the following variables with your data
# HOST = 'https://speckle.xyz/'
# STREAM_ID = 'f378cb19eb'
# COMMIT_ID = 'c41fb59d87'  # If you don't know the COMMIT_ID, you can retrieve it from the Speckle interface or API
#
# # Create and authenticate a client
# client = SpeckleClient(host=HOST)
# account = get_default_account()
# client.authenticate_with_account(account)
#
# # Get the data of the specified commit
# commit = client.commit.get(STREAM_ID, COMMIT_ID)
#
# # Create an authenticated server transport from the client and retrieve the commit object
# transport = ServerTransport(client=client, stream_id=STREAM_ID)
# res = operations.receive(commit.referencedObject, transport)
#
# # Extract the data
# upload_date = commit.createdAt  # Upload date, it may not be the exact file upload date
# file_name = commit.message  # File name (in this case, it's the commit message, might not be the exact file name)
# object_count = res.totalChildrenCount  # Number of elements
#
# # Output the data
# print(f"Upload Date: {upload_date}")
# print(f"File Name: {file_name}")
# print(f"Number of Elements: {object_count}")

#_____________________________________________________

# from specklepy.api import operations
# from specklepy.api.client import SpeckleClient
# from specklepy.api.credentials import get_default_account
# from specklepy.transports.server import ServerTransport
#
# # Replace the following variables with your data
# HOST = 'https://speckle.xyz/'
# STREAM_ID = 'f378cb19eb'
#
# # Create and authenticate the client
# client = SpeckleClient(host=HOST)
# account = get_default_account()
# client.authenticate_with_account(account)
#
# # Get all commits from the stream. Please check Speckle documentation for potential updates to this method.
# commits = client.commit.list(STREAM_ID)
#
# # Iterate through each commit
# for commit in commits:
#     # Create an authenticated server transport from the client and get the commit object
#     transport = ServerTransport(client=client, stream_id=STREAM_ID)
#     res = operations.receive(commit.referencedObject, transport)
#
#     # Extract data
#     upload_date = commit.createdAt  # Upload date, may not be the exact date the file was uploaded
#     file_name = commit.message  # File name (commit message)
#     object_count = res.totalChildrenCount  # Number of elements
#
#     # Output data
#     print(f"Commit ID: {commit.id}")
#     print(f"Upload date: {upload_date}")
#     print(f"File name: {file_name}")
#     print(f"Number of elements: {object_count}")
#     print("------------------------------")

#__________


from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.transports.server import ServerTransport

# Replace the following variables with your data
HOST = 'https://speckle.xyz/'
STREAM_ID = 'f378cb19eb'
# Create and authenticate the client
client = SpeckleClient(host=HOST)
account = get_default_account()
client.authenticate_with_account(account)

# Fetch commits from the stream
commits = client.commit.list(STREAM_ID)


def count_walls(obj, wall_count=0):
    # Check if object has 'category' and is a Wall
    if getattr(obj, 'category', None) == 'Walls':
        wall_count += 1

    # Recursive search for nested objects
    nested_objects = getattr(obj, 'objects', None) or getattr(obj, 'elements', None)
    if nested_objects and isinstance(nested_objects, list):
        for nested_obj in nested_objects:
            wall_count = count_walls(nested_obj, wall_count)

    return wall_count


# Iterate through each commit
for commit in commits:
    # Create an authenticated server transport from the client and get the commit object
    transport = ServerTransport(client=client, stream_id=STREAM_ID)
    res = operations.receive(commit.referencedObject, transport)

    # Debug: Inspecting elements within res
    if hasattr(res, 'elements') and isinstance(res.elements, list) and res.elements:
        pass
        # print(f"Inspecting first element within res.elements: {res.elements[0]}")
        # print(f"Properties of the first element: {dir(res.elements[0])}")
    else:
        print("No elements found in res object")

    # Extract data
    upload_date = getattr(commit, 'createdAt', None)
    file_name = getattr(commit, 'message', None)
    object_count = getattr(res, 'totalChildrenCount', None)

    # Attempt to count "wall" elements
    wall_count = count_walls(res)

    # Output data
    print(f"Commit ID: {commit.id}")
    print(f"Upload date: {upload_date}")
    print(f"File name: {file_name}")
    print(f"Number of elements: {object_count}")
    print(f"Number of wall elements: {wall_count}")
    print("------------------------------")





