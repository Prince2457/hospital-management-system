from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print as rprint

from utils.db_helpers import confirm_delete

confirm_delete("me")