from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

console = Console()
console.print(Panel("Welcome to HMS", title="Hospital Management System", border_style="cyan"))

table = Table(title="Patients".upper(),title_style="bold".title())
table.add_column("ID", style="cyan",)
table.add_column("Name", style="white")
table.add_column("Phone", style="green")

table.add_row("1", "Prince Nkansah", "0244123456")
table.add_row("2", "Kwame Asante", "0277999888")
table.add_row("3", "Ama Mensah", "0209876543")

console.print(table)