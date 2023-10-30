# speckle_and_ai/room_utilities.py
def count_rooms(obj):
    """Count the number of room objects and return their elementIds."""
    room_count = 0
    room_ids = []

    # Check object level
    if getattr(obj, 'category', None) == 'Помещения':
        room_count += 1
        room_ids.append(obj.elementId)

    # If we have 'elements', we need to check each element inside 'elements'
    elements = getattr(obj, 'elements', None)
    if elements and isinstance(elements, list):
        for element in elements:
            # Recursively check nested 'elements'
            count, ids = count_rooms(element)
            room_count += count
            room_ids.extend(ids)

    return room_count, room_ids
