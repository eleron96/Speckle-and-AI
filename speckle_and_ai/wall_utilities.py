def count_walls(obj):
    """Count the number of wall objects."""
    wall_count = 0

    # Check if the current object is a wall
    if getattr(obj, 'category', None) == 'Walls':
        wall_count += 1

    # If we have 'elements' or 'objects', we need to check each element
    # inside them
    for element in getattr(obj, 'elements', []) or getattr(obj, 'objects', []):
        wall_count += count_walls(element)

    return wall_count

