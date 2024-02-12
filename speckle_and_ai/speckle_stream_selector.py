from rich.console import Console
from rich.table import Table
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account

console = Console()

def authenticate_client():
    """
    Аутентификация клиента с использованием аккаунта по умолчанию из Speckle Manager.
    """
    account = get_default_account()
    if not account:
        console.print(
            "Не удалось найти аккаунт по умолчанию. Убедитесь, что вы добавили аккаунт в Speckle Manager.",
            style="bold red")
        exit(1)

    client = SpeckleClient(host=account.serverInfo.url)
    client.authenticate_with_token(account.token)
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
    console.print("[bold]Доступные проекты (streams):[/bold]", justify="left")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Номер", style="dim")
    table.add_column("Название", min_width=20)
    table.add_column("ID", min_width=20)

    for i, stream in enumerate(streams):
        table.add_row(str(i + 1), stream.name, stream.id)

    console.print(table, justify="left")

    try:
        choice = int(console.input("Выберите номер проекта: ")) - 1
        selected_stream = streams[choice]
        console.print(
            f"Выбран проект: [bold]{selected_stream.name}[/bold] с ID: [bold]{selected_stream.id}[/bold]",
            justify="left")
        return selected_stream
    except KeyboardInterrupt:
        console.print("\nПрограмма прервана пользователем. Выход.",
                      style="bold red")
        exit(0)
    except ValueError:
        console.print("Некорректный ввод. Пожалуйста, введите номер проекта.",
                      style="bold yellow")
        return select_stream(streams)
    except IndexError:
        console.print(
            "Выбран некорректный номер проекта. Пожалуйста, выберите существующий номер.",
            style="bold yellow")
        return select_stream(streams)


def main():
    """
    Основная функция программы, возвращает выбранный STREAM_ID.
    """
    client = authenticate_client()
    streams = get_streams(client)
    if streams:
        selected_stream = select_stream(streams)
        return selected_stream.id
    else:
        console.print("Нет доступных проектов (streams).", style="bold red")
        exit(1)


if __name__ == "__main__":
    main()
