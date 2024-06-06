def extract_area_float_numbers(obj):
    room_count = 0
    room_ids = []
    room_types = {}
    room_section = {}

    # Check if the current object is a room
    if getattr(obj, 'category', None) == 'Помещения':
        room_ids.append(obj.elementId)



        if hasattr(obj, "parameters"):
            param_obj = obj.parameters
            for param_name, param_value in param_obj.__dict__.items():
                if hasattr(param_value, 'name'):
                    print(f"{param_value.name}: {param_value.value}")

    # If we have 'elements', we need to check each element inside 'elements'
    for element in getattr(obj, 'elements', []):
        count, ids, types = extract_area_float_numbers(element)
        room_section.update(ids)
        room_ids.extend(ids)

    return room_count, room_ids, room_types, room_section