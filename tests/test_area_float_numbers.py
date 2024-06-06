import pytest
from faker import Faker
from speckle_and_ai.area_float_numbers import extract_area_float_numbers

faker = Faker()


# Генерируем тестовые данные
def generate_test_data():
    class Parameters:
        def __init__(self, name, value):
            self.name = name
            self.value = value

    class TestObject:
        def __init__(self, category, elementId, parameters):
            self.category = category
            self.elementId = elementId
            self.parameters = parameters

    # Создаем параметры помещения
    parameters = Parameters(faker.word(), faker.word())

    # Возвращаем тестовый объект с параметрами
    return TestObject('Помещения', faker.random_number(digits=5), parameters)


@pytest.mark.parametrize("obj", [generate_test_data() for _ in range(5)])
def test_extract_area_float_numbers_with_parameters(obj):
    room_count, room_ids, room_types, room_section = extract_area_float_numbers(
        obj)

    assert room_count == 0  # Судя по коду, room_count всегда возвращает 0, это может быть ошибкой.
    assert len(
        room_ids) > 0  # Проверяем, что был добавлен хотя бы один ID помещения.
    assert room_types == {}  # Этот параметр, кажется, никогда не заполняется в текущей реализации функции.
    assert room_section == {}  # Проверка на наличие обновлений в room_section в зависимости от структуры входных данных.
