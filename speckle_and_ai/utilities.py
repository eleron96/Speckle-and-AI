# utilities.py

def count_walls(obj, wall_count=0):
    # Check if object has 'category' and is a Wall
    if getattr(obj, 'category', None) == 'Walls':
        wall_count += 1

    # Recursive search for nested objects
    nested_objects = getattr(obj, 'objects', None) or getattr(obj, 'elements', None)
    if nested_objects and isinstance(nested_objects, list):
        for nested_obj in nested_objects:
            wall_count = count_walls(nested_obj, wall_count)

    return wall_count


def count_rooms(obj, room_count=0):
    # Проверка на уровне объекта
    if getattr(obj, 'category', None) == 'Помещения':
        room_count += 1

    # Если у нас есть 'elements', то мы должны проверить каждый элемент внутри 'elements'
    elements = getattr(obj, 'elements', None)
    if elements and isinstance(elements, list):
        for element in elements:
            # Рекурсивно проверяем вложенные 'elements'
            room_count = count_rooms(element, room_count)

    return room_count



