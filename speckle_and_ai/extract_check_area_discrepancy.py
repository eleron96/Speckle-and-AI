def extract_check_area_discrepancy(obj):
    discrepancy_rooms = []

    # Check if the current object is a room
    if getattr(obj, 'category', None) == 'Помещения' and hasattr(obj,
                                                                 "parameters"):
        param_obj = obj.parameters
        area = None
        rounded_area = None
        for param_name, param_value in param_obj.__dict__.items():
            if hasattr(param_value, 'name'):
                if param_value.name == 'Площадь':
                    area = param_value.value
                elif param_value.name == 'Speech_Площадь округлённая':
                    rounded_area = param_value.value

        if area and rounded_area and abs(area - rounded_area) > 0.4:
            discrepancy_info = {
                'id': obj.elementId,
                'name': obj.name,
                'area': area,
                'rounded_area': rounded_area
            }
            discrepancy_rooms.append(discrepancy_info)

    # If we have 'elements', we need to check each element inside 'elements'
    for element in getattr(obj, 'elements', []):
        discrepancy_rooms.extend(extract_check_area_discrepancy(element))

    return discrepancy_rooms

