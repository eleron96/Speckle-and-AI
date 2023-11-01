# wall_utilities.py

# def count_walls(obj, wall_count=0):
#     """Count the number of wall objects."""
#     # Check if object has 'category' and is a Wall
#     if getattr(obj, 'category', None) == 'Walls':
#         wall_count += 1
#
#     # Recursive search for nested objects
#     nested_objects = getattr(obj, 'objects', None) or getattr(obj, 'elements', None)
#     if nested_objects and isinstance(nested_objects, list):
#         for nested_obj in nested_objects:
#             wall_count = count_walls(nested_obj, wall_count)
#
#     return wall_count

def count_walls(obj):
    """Count the number of wall objects."""
    wall_count = 0

    # Check if the current object is a wall
    if getattr(obj, 'category', None) == 'Walls':
        wall_count += 1

    # If we have 'elements' or 'objects', we need to check each element inside them
    for element in getattr(obj, 'elements', []) or getattr(obj, 'objects', []):
        wall_count += count_walls(element)

    return wall_count

