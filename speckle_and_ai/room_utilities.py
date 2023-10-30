# room_utilities.py

def count_rooms(obj, room_count=0):
    """Count the number of room objects."""
    # Check object level
    if getattr(obj, 'category', None) == 'Помещения':
        room_count += 1

    # If we have 'elements', we need to check each element inside 'elements'
    elements = getattr(obj, 'elements', None)
    if elements and isinstance(elements, list):
        for element in elements:
            # Recursively check nested 'elements'
            room_count = count_rooms(element, room_count)

    return room_count
