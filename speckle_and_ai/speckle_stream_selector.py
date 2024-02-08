from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account


def authenticate_client():
    """
    Аутентификация клиента с использованием аккаунта по умолчанию из Speckle Manager.
    """
    account = get_default_account()
    if not account:
        print(
            "Не удалось найти аккаунт по умолчанию. Убедитесь, что вы добавили аккаунт в Speckle Manager.")
        exit(1)

    client = SpeckleClient(host=account.serverInfo.url)
    client.authenticate_with_token(
        account.token)  # Обновлено для использования нового метода
    return client


def get_streams(client):
    """
    Получение списка доступных streams.
    """
    streams = client.stream.list()
    return streams


def select_stream(streams):
    """
    Выбор stream пользователем.
    """
    print("Доступные проекты (streams):")
    for i, stream in enumerate(streams):
        print(f"{i + 1}: {stream.name} - {stream.id}")

    try:
        choice = int(input("Выберите номер проекта: ")) - 1
        selected_stream = streams[choice]
        return selected_stream
    except KeyboardInterrupt:
        print("\nПрограмма прервана пользователем. Выход.")
        exit(0)
    except ValueError:
        print("Некорректный ввод. Пожалуйста, введите номер проекта.")
        return select_stream(
            streams)  # Рекурсивно вызываем снова, если ввод некорректен
    except IndexError:
        print(
            "Выбран некорректный номер проекта. Пожалуйста, выберите существующий номер.")
        return select_stream(
            streams)  # Рекурсивно вызываем снова, если выбран некорректный номер


def main():
    """
    Основная функция программы, возвращает выбранный STREAM_ID.
    """
    client = authenticate_client()
    streams = get_streams(client)
    if streams:
        selected_stream = select_stream(streams)
        return selected_stream.id  # Возвращаем STREAM_ID выбранного проекта
    else:
        print("Нет доступных проектов (streams).")
        exit(1)


if __name__ == "__main__":
    main()
