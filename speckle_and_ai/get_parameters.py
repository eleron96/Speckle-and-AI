from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.objects import Base
from typing import Dict, Any

STREAM_ID = "9956b252b3"
SERVER_URL = "https://speckle.xyz"
COMMIT_ID = "c480aa3164"

def get_object_parameters(obj: Base) -> Dict[str, Any]:
    if not hasattr(obj, 'parameters'):
        return {}

    parameters_data = obj.parameters
    result_dict = {}

    if isinstance(parameters_data, Base):
        dynamic_params = parameters_data.get_dynamic_member_names()
        for param_name in dynamic_params:
            param = getattr(parameters_data, param_name)
            if isinstance(param, Base):
                param_name = getattr(param, 'name', param_name) # Use a human-readable name, if available
                if hasattr(param, 'value'):
                    result_dict[param_name] = getattr(param, 'value')
                else:
                    # If the parameter does not have a 'value' but has other fields, add them as a dictionary
                    result_dict[param_name] = {attr: getattr(param, attr) for attr in param.get_dynamic_member_names()}
            else:
                result_dict[param_name] = param

    return result_dict


def print_room_details(room: Base):
    room_parameters = get_object_parameters(room)
    print(f"Parameters of the premises with elementId {getattr(room, 'elementId', 'Not specified')}:")

    for param_name, param_value in room_parameters.items():
        if isinstance(param_value, dict):
            print(f"  {param_name}:")
            for nested_key, nested_value in param_value.items():
                print(f"    {nested_key}: {nested_value}")
        else:
            print(f"  {param_name}: {param_value}")
    print("-" * 40)

def find_rooms_recursive(obj):
    rooms = []
    if getattr(obj, 'category', None) == 'Помещения':
        rooms.append(obj)

    if isinstance(obj, Base) and hasattr(obj, "__dict__"):
        for attr_value in obj.__dict__.values():
            if isinstance(attr_value, list):
                for item in attr_value:
                    if isinstance(item, Base):
                        rooms.extend(find_rooms_recursive(item))
            elif isinstance(attr_value, Base):
                rooms.extend(find_rooms_recursive(attr_value))
    return rooms

def find_room_by_id(rooms, target_id):
    for room in rooms:
        if getattr(room, 'elementId', '') == target_id:
            return room
    return None

def main():
    account = get_default_account()
    if not account:
        print("Account not found. Please add an account in the Speckle Manager.")
        return

    client = SpeckleClient(host=SERVER_URL)
    client.authenticate_with_token(account.token)

    commit = client.commit.get(stream_id=STREAM_ID, commit_id=COMMIT_ID)
    root_object_id = commit.referencedObject

    root_object = client.object.get(stream_id=STREAM_ID, object_id=root_object_id)

    rooms = find_rooms_recursive(root_object)
    print(f"Premises found: {len(rooms)}")

    target_id = input("Enter the ID of the room element: ")

    target_room = find_room_by_id(rooms, target_id)

    if target_room:
        print_room_details(target_room)
    else:
        print(f"Premises with elementId {target_id} not found.")

if __name__ == "__main__":
    main()
