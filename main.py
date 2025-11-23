#!/usr/bin/env python3
"""
Telethon Multi-Session Maker
A powerful CLI tool to create multiple Telegram sessions from phone numbers

Developer: @GodmrunaL
Telegram Channel: @Beastx_Bots
"""

import csv
import os
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.text import Text
from rich import box
from telethon.sync import TelegramClient
from telethon import utils
from telethon.errors import (
    PhoneNumberInvalidError,
    ApiIdInvalidError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
    FloodWaitError
)
import time

console = Console()


class SessionMaker:
    """Telethon Session Maker with beautiful terminal interface"""
    
    def __init__(self):
        self.sessions_dir = Path("sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.phone_file = "phone.csv"
        self.api_file = "api.csv"
        self.phones: List[str] = []
        self.api_credentials: List[Tuple[int, str]] = []
        self.use_multiple_apis = False
        self.success_count = 0
        self.failed_count = 0
        
    def print_banner(self):
        """Display welcome banner"""
        banner = Text()
        banner.append("╔═══════════════════════════════════════════════════╗\n", style="bold cyan")
        banner.append("║   ", style="bold cyan")
        banner.append("TELETHON MULTI-SESSION MAKER", style="bold yellow")
        banner.append("            ║\n", style="bold cyan")
        banner.append("╠═══════════════════════════════════════════════════╣\n", style="bold cyan")
        banner.append("║   ", style="bold cyan")
        banner.append("Developer: @GodmrunaL", style="bold green")
        banner.append("                      ║\n", style="bold cyan")
        banner.append("║   ", style="bold cyan")
        banner.append("Channel: @Beastx_Bots", style="bold green")
        banner.append("                      ║\n", style="bold cyan")
        banner.append("╚═══════════════════════════════════════════════════╝", style="bold cyan")
        
        console.print(banner)
        console.print()
        
    def load_phones(self) -> bool:
        """Load phone numbers from CSV file"""
        try:
            if not os.path.exists(self.phone_file):
                console.print(f"[bold red]✗[/bold red] Error: {self.phone_file} not found!")
                console.print(f"[yellow]Creating example {self.phone_file}...[/yellow]")
                self.create_example_phone_csv()
                console.print(f"[green]✓[/green] Example file created. Please add your phone numbers and run again.")
                return False
                
            with open(self.phone_file, 'r', encoding='utf-8') as f:
                lines = f.read().strip().splitlines()
                self.phones = [line.strip() for line in lines if line.strip()]
                
            if not self.phones:
                console.print(f"[bold red]✗[/bold red] Error: {self.phone_file} is empty!")
                return False
                
            console.print(f"[green]✓[/green] Loaded {len(self.phones)} phone number(s) from {self.phone_file}")
            return True
            
        except Exception as e:
            console.print(f"[bold red]✗[/bold red] Error loading {self.phone_file}: {str(e)}")
            return False
            
    def load_api_credentials(self) -> bool:
        """Load API credentials from CSV file or prompt user"""
        
        # Ask user if they want to use CSV file or enter credentials manually
        use_csv = Confirm.ask(
            f"\n[cyan]Do you have API credentials in {self.api_file}?[/cyan]",
            default=False
        )
        
        if use_csv:
            return self.load_api_from_csv()
        else:
            return self.prompt_api_credentials()
            
    def load_api_from_csv(self) -> bool:
        """Load API credentials from CSV file"""
        try:
            if not os.path.exists(self.api_file):
                console.print(f"[bold red]✗[/bold red] Error: {self.api_file} not found!")
                console.print(f"[yellow]Creating example {self.api_file}...[/yellow]")
                self.create_example_api_csv()
                console.print(f"[green]✓[/green] Example file created. Please add your API credentials and run again.")
                return False
                
            with open(self.api_file, 'r', encoding='utf-8') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if len(row) >= 2 and row[0].strip() and row[1].strip():
                        try:
                            api_id = int(row[0].strip())
                            api_hash = row[1].strip()
                            self.api_credentials.append((api_id, api_hash))
                        except ValueError:
                            console.print(f"[yellow]⚠[/yellow] Skipping invalid row: {row}")
                            
            if not self.api_credentials:
                console.print(f"[bold red]✗[/bold red] Error: No valid API credentials found in {self.api_file}!")
                return False
                
            console.print(f"[green]✓[/green] Loaded {len(self.api_credentials)} API credential(s)")
            
            if len(self.api_credentials) > 1:
                self.use_multiple_apis = True
                console.print(f"[cyan]ℹ[/cyan] Using multiple API credentials (one per phone number)")
            else:
                console.print(f"[cyan]ℹ[/cyan] Using single API credential for all phone numbers")
                
            return True
            
        except Exception as e:
            console.print(f"[bold red]✗[/bold red] Error loading {self.api_file}: {str(e)}")
            return False
            
    def prompt_api_credentials(self) -> bool:
        """Prompt user to enter API credentials manually"""
        try:
            console.print()
            console.print(Panel.fit(
                "[yellow]Get your API credentials from:[/yellow]\n"
                "[cyan]https://my.telegram.org/apps[/cyan]",
                title="[bold]API Credentials Required[/bold]",
                border_style="cyan"
            ))
            console.print()
            
            # Ask if user wants to use single or multiple API credentials
            use_multiple = Confirm.ask(
                "[cyan]Do you want to use different API credentials for each phone number?[/cyan]",
                default=False
            )
            
            if use_multiple:
                self.use_multiple_apis = True
                count = len(self.phones)
                console.print(f"[yellow]You need to enter {count} API credential(s)[/yellow]\n")
                
                for i in range(count):
                    console.print(f"[bold cyan]API Credentials #{i+1}[/bold cyan]")
                    api_id = Prompt.ask("  Enter API ID", default="")
                    api_hash = Prompt.ask("  Enter API Hash", default="")
                    
                    if api_id and api_hash:
                        try:
                            self.api_credentials.append((int(api_id), api_hash))
                        except ValueError:
                            console.print(f"[red]Invalid API ID. Using defaults.[/red]")
                            return False
                    console.print()
            else:
                console.print(f"[bold cyan]Enter API Credentials (will be used for all phone numbers)[/bold cyan]")
                api_id = Prompt.ask("  API ID", default="")
                api_hash = Prompt.ask("  API Hash", default="")
                
                if api_id and api_hash:
                    try:
                        self.api_credentials.append((int(api_id), api_hash))
                    except ValueError:
                        console.print(f"[red]Invalid API ID[/red]")
                        return False
                        
            if not self.api_credentials:
                console.print(f"[bold red]✗[/bold red] No API credentials provided!")
                return False
                
            console.print(f"[green]✓[/green] API credentials configured successfully")
            return True
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Operation cancelled by user[/yellow]")
            return False
        except Exception as e:
            console.print(f"[bold red]✗[/bold red] Error: {str(e)}")
            return False
            
    def get_api_for_index(self, index: int) -> Tuple[int, str]:
        """Get API credentials for a specific phone number index"""
        if self.use_multiple_apis and index < len(self.api_credentials):
            return self.api_credentials[index]
        else:
            return self.api_credentials[0]
            
    def create_session(self, phone: str, api_id: int, api_hash: str) -> bool:
        """Create a Telegram session for a phone number"""
        try:
            parsed_phone = utils.parse_phone(phone)
            session_name = f"sessions/{parsed_phone}"
            
            console.print(f"\n[bold cyan]→[/bold cyan] Creating session for [yellow]{parsed_phone}[/yellow]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Connecting to Telegram...", total=None)
                
                client = TelegramClient(session_name, api_id, api_hash)
                client.connect()
                
                if not client.is_user_authorized():
                    progress.update(task, description="Sending code request...")
                    client.send_code_request(parsed_phone)
                    
                    # Stop progress for user input
                    progress.stop()
                    
                    code = Prompt.ask(f"  [cyan]Enter the code sent to {parsed_phone}[/cyan]")
                    
                    try:
                        client.sign_in(parsed_phone, code)
                    except SessionPasswordNeededError:
                        password = Prompt.ask("  [cyan]Enter your 2FA password[/cyan]", password=True)
                        client.sign_in(password=password)
                        
                client.disconnect()
                
            console.print(f"[green]✓[/green] Session created successfully: [bold]{parsed_phone}.session[/bold]")
            self.success_count += 1
            return True
            
        except PhoneNumberInvalidError:
            console.print(f"[red]✗[/red] Invalid phone number: {phone}")
            self.failed_count += 1
            return False
        except ApiIdInvalidError:
            console.print(f"[red]✗[/red] Invalid API ID or API Hash")
            self.failed_count += 1
            return False
        except PhoneCodeInvalidError:
            console.print(f"[red]✗[/red] Invalid verification code")
            self.failed_count += 1
            return False
        except FloodWaitError as e:
            console.print(f"[red]✗[/red] Flood wait error. Please wait {e.seconds} seconds")
            self.failed_count += 1
            return False
        except KeyboardInterrupt:
            console.print(f"\n[yellow]⚠[/yellow] Skipped by user")
            self.failed_count += 1
            return False
        except Exception as e:
            console.print(f"[red]✗[/red] Error: {str(e)}")
            self.failed_count += 1
            return False
            
    def create_example_phone_csv(self):
        """Create example phone.csv file"""
        with open(self.phone_file, 'w', encoding='utf-8') as f:
            f.write("+1234567890\n")
            f.write("+9876543210\n")
            
    def create_example_api_csv(self):
        """Create example api.csv file"""
        with open(self.api_file, 'w', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["123456", "abcdef1234567890abcdef1234567890"])
            writer.writerow(["789012", "1234567890abcdef1234567890abcdef"])
            
    def show_summary(self):
        """Display session creation summary"""
        console.print()
        
        table = Table(title="Session Creation Summary", box=box.ROUNDED, border_style="cyan")
        table.add_column("Status", style="bold", justify="center")
        table.add_column("Count", justify="center")
        
        table.add_row("[green]Successful[/green]", f"[green]{self.success_count}[/green]")
        table.add_row("[red]Failed[/red]", f"[red]{self.failed_count}[/red]")
        table.add_row("[cyan]Total[/cyan]", f"[cyan]{len(self.phones)}[/cyan]")
        
        console.print(table)
        console.print()
        
        if self.success_count > 0:
            console.print(Panel.fit(
                f"[green]Session files saved in:[/green] [bold yellow]sessions/[/bold yellow] directory",
                border_style="green"
            ))
            
    def run(self):
        """Main execution method"""
        try:
            self.print_banner()
            
            # Load phone numbers
            if not self.load_phones():
                return
                
            # Load or prompt for API credentials
            if not self.load_api_credentials():
                return
                
            # Confirm before proceeding
            console.print()
            if not Confirm.ask(
                f"[cyan]Ready to create {len(self.phones)} session(s). Continue?[/cyan]",
                default=True
            ):
                console.print("[yellow]Operation cancelled[/yellow]")
                return
                
            # Create sessions
            console.print()
            console.print("[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
            console.print("[bold]Starting Session Creation...[/bold]")
            console.print("[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
            
            for i, phone in enumerate(self.phones):
                api_id, api_hash = self.get_api_for_index(i)
                self.create_session(phone, api_id, api_hash)
                
                # Small delay between sessions to avoid rate limiting
                if i < len(self.phones) - 1:
                    time.sleep(1)
                    
            # Show summary
            self.show_summary()
            
            # Footer
            console.print()
            console.print(Panel.fit(
                "[bold cyan]Need More Tools?[/bold cyan]\n"
                "[green]Developer:[/green] [yellow]@GodmrunaL[/yellow]\n"
                "[green]Channel:[/green] [yellow]@Beastx_Bots[/yellow]",
                border_style="cyan"
            ))
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]⚠ Operation cancelled by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"\n[bold red]✗ Fatal Error:[/bold red] {str(e)}")
            sys.exit(1)


def main():
    """Entry point"""
    try:
        maker = SessionMaker()
        maker.run()
        
        console.print()
        input("Press Enter to exit...")
        
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        sys.exit(0)


if __name__ == "__main__":
    main()
