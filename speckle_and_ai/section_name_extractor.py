# def extract_section_name_from_rooms(obj):
#     room_count = 0
#     room_ids = []
#     room_types = {}
#     room_section = {}
#
#     # Check if the current object is a room
#     if getattr(obj, 'category', None) == 'Помещения':
#         room_ids.append(obj.elementId)
#
#
#
#         # if hasattr(obj, "parameters"):
#         #     param_obj = obj.parameters
#         #     for param_name, param_value in param_obj.__dict__.items():
#         #         if hasattr(param_value, 'name'):
#         #             print(f"{param_value.name}: {param_value.value}")
#
#         if hasattr(obj, "parameters"):
#             param_obj = obj.parameters
#             for param_name, param_value in param_obj.__dict__.items():
#                 if hasattr(param_value,
#                            'name') and param_value.name == 'Speech_Корпус.Секция короткое':
#                     print(f"{param_value.name}: {param_value.value}")
#
#     # If we have 'elements', we need to check each element inside 'elements'
#     for element in getattr(obj, 'elements', []):
#         count, ids, types = extract_section_name_from_rooms(element)
#         room_section.update(ids)
#         room_ids.extend(ids)
#
#     return room_count, room_ids, room_types, room_section


def extract_section_name_from_rooms(obj):
    room_section = set()

    # Check if the current object is a room
    if getattr(obj, 'category', None) == 'Помещения' and hasattr(obj, "parameters"):
        param_obj = obj.parameters
        for param_name, param_value in param_obj.__dict__.items():
            if hasattr(param_value, 'name') and param_value.name == 'Speech_Корпус.Секция короткое':
                room_section.add(param_value.value)

    # If we have 'elements', we need to check each element inside 'elements'
    for element in getattr(obj, 'elements', []):
        room_section.update(extract_section_name_from_rooms(element))

    return room_section

