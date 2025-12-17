import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import print as rprint
import questionary

from src.api import ApiClient
from src.aws_handler import AWSClient

console = Console()
api = ApiClient()
aws = AWSClient()

language_map = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Romanian": "ro"
}

def print_banner():
    console.clear()
    ascii_art = r"""
 _        _______  _______  _        _______           _______             _______  _______  _______  _______  _______  _______  _______ 
( (    /|(  ____ \(  ___  )( (    /|(  ____ \|\     /|(  ____ \           (  ____ \(  ____ \(  ____ )(  ___  )(  ____ )(  ____ \(  ____ )
|  \  ( || (    \/| (   ) ||  \  ( || (    \/| )   ( || (    \/           | (    \/| (    \/| (    )|| (   ) || (    )|| (    \/| (    )|
|   \ | || (__    | |   | ||   \ | || (__    | | _ | || (_____             | (_____ | |      | (____)|| (___) || (____)|| (__    | (____)|
| (\ \) ||  __)   | |   | || (\ \) ||  __)   | |( )| |(_____  )            (_____  )| |      |     __)|  ___  ||  _____)|  __)   |     __)
| | \   || (      | |   | || | \   || (      | || || |      ) |                  ) || |      | (\ (   | (   ) || (      | (      | (\ (   
| )  \  || (____/\| (___) || )  \  || (____/\| () () |/\____) |            /\____) || (____/\| ) \ \__| )   ( || )      | (____/\| ) \ \__
|/    )_)(_______/(_______)|/    )_)(_______/(_______)\_______)            \_______)(_______/|/   \__/|/     \||/       (_______/|/   \__/
"""

    console.print(Panel.fit(
        f"[bold cyan]{ascii_art}[/bold cyan]",
        subtitle="[dim]Powered by NeoCity Press Institute v1.0[/dim]",
        border_style="green",
        padding=(1, 1)
    ))

def fetch_and_display_news(selected_country, selected_topic, selected_language_code):
    #Fetch Data
    country_info = None
    articles = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True
    ) as progress:
        
        #Country Data
        task1 = progress.add_task(description="Fetching Country Data...", total=1)
        country_info = api.get_country_details(selected_country)
        time.sleep(0.5)
        progress.advance(task1)

        if not country_info:
            console.print(f"[bold red]Could not find data for {selected_country}[/bold red]")
            return

        #News Data
        task2 = progress.add_task(description=f"Fetching News for {selected_topic}...", total=1)
        articles = api.get_news(
            country_code=country_info['cca2'],
            topic=selected_topic,
            language=selected_language_code
        )
        progress.advance(task2)

    #Display Country Info
    console.print(Panel(
        f"[bold]Capital:[/bold] {country_info['capital']}\n"
        f"[bold]Currency:[/bold] {country_info['currency']}\n"
        f"[bold]Language:[/bold] {country_info['language']}",
        title=f"[bold yellow]{country_info['name']}[/bold yellow]",
        expand=False
    ))

    #Process & Save News
    if not articles:
        console.print(f"[yellow]No news found for topic '{selected_topic}' in {selected_country}.[/yellow]")
        return

    table = Table(title=f"Latest {selected_topic} News in {selected_country}")
    table.add_column("No.", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Source", style="magenta")

    with console.status("[bold blue]Archiving to AWS DynamoDB & S3...[/bold blue]"):
        for idx, article in enumerate(articles, 1):
            aws.save_article(article, selected_topic)
            title = article.get('title', 'No Title')
            source = article.get('link', 'Unknown')
            table.add_row(str(idx), title[:60] + "...", source)

    console.print(table)
    console.print(f"\n[bold green]✔ Successfully saved {len(articles)} articles to AWS![/bold green]")

def main():
    print_banner()

    #Initialize AWS Resources
    with console.status("[bold green]Checking AWS Resources...[/bold green]", spinner="dots"):
        aws.init_resources()
        time.sleep(1)
    console.print("[green]✔ AWS Connection Established[/green]")

    while True:
        #User Selections about Country and News Topic
        countries = ["Romania","United States", "United Kingdom", "France", "Germany", "Spain", "Exit"]
        
        selected_country = questionary.select(
            "Select a Country (fan favourites):",
            choices=countries
        ).ask()

        if selected_country == "Exit":
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)

        while True:
            topics = ["technology","business","sports","politics","education","entertainment","science","health","world", "Back"]
            selected_topic = questionary.select(
                "Select a News Topic:",
                choices=topics
            ).ask()

            if selected_topic == "Back":
                break

            while True:
                #Default language input for display, but API logic in this demo defaults to EN to ensure results
                languages = ["English", "Spanish", "French", "German", "Romanian", "Back"]
                language = questionary.select(
                    "Select Preferred Language:",
                    choices=languages
                ).ask()

                if language == "Back":
                    break

                selected_language_code = language_map.get(language, "en")
                
                fetch_and_display_news(selected_country, selected_topic, selected_language_code)
                
                questionary.press_any_key_to_continue().ask()
                break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Exiting...[/red]")
        sys.exit(0)