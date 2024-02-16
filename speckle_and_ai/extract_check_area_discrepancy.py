# def extract_check_area_discrepancy(obj):
#     discrepancy_rooms = []
#
#     # Check if the current object is a room
#     if getattr(obj, 'category', None) == 'Помещения' and hasattr(obj,
#                                                                  "parameters"):
#         param_obj = obj.parameters
#         area = None
#         rounded_area = None
#         for param_name, param_value in param_obj.__dict__.items():
#             if hasattr(param_value, 'name'):
#                 if param_value.name == 'Площадь':
#                     area = param_value.value
#                 elif param_value.name == 'Speech_Площадь округлённая':
#                     rounded_area = param_value.value
#
#         if area and rounded_area and abs(area - rounded_area) > 0.4:
#             discrepancy_info = {
#                 'id': obj.elementId,
#                 'name': obj.name,
#                 'area': area,
#                 'rounded_area': rounded_area
#             }
#             discrepancy_rooms.append(discrepancy_info)
#
#     # If we have 'elements', we need to check each element inside 'elements'
#     for element in getattr(obj, 'elements', []):
#         discrepancy_rooms.extend(extract_check_area_discrepancy(element))
#
#     return discrepancy_rooms


def extract_check_area_discrepancy(obj):
    discrepancy_rooms = []

    # Check if the current object is a room
    if getattr(obj, 'category', None) == 'Помещения' and hasattr(obj, "parameters"):
        param_obj = obj.parameters
        area = None
        rounded_area = None
        other_params = {}
        level_name = None
        room_number = None

        for param_name, param_value in param_obj.__dict__.items():
            if hasattr(param_value, 'name'):
                normalized_param_name = param_value.name.lower()  # Normalize parameter name to lowercase
                if normalized_param_name == 'площадь':
                    area = param_value.value
                elif normalized_param_name == 'speech_площадь округлённая':
                    rounded_area = param_value.value
                elif normalized_param_name == 'уровень' and level_name is None:  # Check if level_name is not already set
                    level_name = param_value.value
                elif normalized_param_name == 'номер' and room_number is None:  # Check if room_number is not already set
                    room_number = param_value.value
                else:
                    other_params[param_value.name] = param_value.value

        if area is not None and rounded_area is not None and abs(area - rounded_area) > 0.4:
            discrepancy_info = {
                'id': obj.elementId,
                'name': obj.name,
                'area': area,
                'rounded_area': rounded_area,
                'level_name': level_name,
                'room_number': room_number
            }
            # Add other parameters to the discrepancy info
            discrepancy_info.update(other_params)
            discrepancy_rooms.append(discrepancy_info)

    # If we have 'elements', we need to check each element inside 'elements'
    for element in getattr(obj, 'elements', []):
        discrepancy_rooms.extend(extract_check_area_discrepancy(element))

    return discrepancy_rooms
