import os
import time
import random
from datetime import datetime
from pyfiglet import figlet_format
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn


console = Console()


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_title():
    ascii_banner = figlet_format("InfoCLI", font="slant")
    console.print(f"[bold magenta]{ascii_banner}[/bold magenta]")


def show_loading(message="Loading..."):
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True
    ) as progress:
        task = progress.add_task(f"[cyan]{message}", total=100)
        for _ in range(10):
            progress.update(task, advance=10)
            time.sleep(0.1)


def choose_country():
    countries = {
        "1": ("USA", "America/New_York", "USD"),
        "2": ("UK", "Europe/London", "GBP"),
        "3": ("Japan", "Asia/Tokyo", "JPY"),
        "4": ("India", "Asia/Kolkata", "INR"),
        "5": ("Germany", "Europe/Berlin", "EUR")
    }
    console.print("[bold yellow]Select a country:[/bold yellow]")
    for key, (name, _, _) in countries.items():
        console.print(f"[green]{key}[/green]: {name}")
    choice = Prompt.ask("Enter number")
    return countries.get(choice, countries["1"])


def get_time_in_country(timezone):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"The simulated time in [bold cyan]{timezone}[/bold cyan] is: [bold green]{now}[/bold green]"


def get_weather_in_country(country):
    temp = random.randint(15, 35)
    return f"The weather in [bold yellow]{country}[/bold yellow] is [bold blue]{temp}°C[/bold blue] and sunny ☀️"


def get_exchange_rate(currency):
    rate = round(random.uniform(0.3, 1.5), 2)
    return f"1 Euro = [bold green]{rate} {currency}[/bold green]"


def main_menu():
    while True:
        clear_screen()
        print_title()
        console.print("[bold white]What would you like to do?[/bold white]")
        console.print("[cyan]1[/cyan]: Get current time in a country")
        console.print("[cyan]2[/cyan]: See weather in a country")
        console.print("[cyan]3[/cyan]: Get currency exchange rate to Euro")
        console.print("[red]4[/red]: Exit")

        choice = Prompt.ask("Choose an option")

        if choice == "4":
            break

        clear_screen()
        print_title()
        country, timezone, currency = choose_country()
        show_loading("Fetching info...")

        if choice == "1":
            console.print(get_time_in_country(timezone))
        elif choice == "2":
            console.print(get_weather_in_country(country))
        elif choice == "3":
            console.print(get_exchange_rate(currency))
        else:
            console.print("[red]Invalid option.[/red]")

        input("\n[Press Enter to return to menu]")


if __name__ == "__main__":
    main_menu()

