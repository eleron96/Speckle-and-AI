def count_rooms(obj):
    room_count = 0
    room_ids = []
    room_types = {}

    # Check if the current object is a room
    if getattr(obj, 'category', None) == 'Помещения':
        room_count += 1
        room_ids.append(obj.elementId)

        # Check for the room type parameter
        if hasattr(obj, "parameters"):
            param_obj = obj.parameters
            if hasattr(param_obj, "КГ_Тип помещения короткий"):
                param_value = getattr(param_obj,
                                      'КГ_Тип помещения короткий').value
                # print(f"Found room type: {param_value}")  # Debug message
                if param_value in room_types:
                    room_types[param_value] += 1
                else:
                    room_types[param_value] = 1

    # If we have 'elements', we need to check each element inside 'elements'
    for element in getattr(obj, 'elements', []):
        count, ids, types = count_rooms(element)
        room_count += count
        room_ids.extend(ids)
        for key, value in types.items():
            if key in room_types:
                room_types[key] += value
            else:
                room_types[key] = value

    return room_count, room_ids, room_types


def check_room_name_uniqueness(all_commits_data):
    all_room_ids = [room_id for commit_data in all_commits_data for room_id in
                    commit_data['room_ids']]
    unique_room_ids = set(all_room_ids)
    if len(all_room_ids) != len(unique_room_ids):
        print("Есть неуникальные имена помещений!")
    else:
        print("Все имена помещений уникальны!")
