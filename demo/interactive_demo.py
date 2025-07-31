#!/usr/bin/env python3
"""
Open Deep Research - Interactive Demo

This demo showcases the full functionality of the Open Deep Research system,
including different model providers, search APIs, and research workflows.
"""

import asyncio
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.syntax import Syntax
import json

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from open_deep_research.deep_researcher import deep_researcher
from open_deep_research.configuration import Configuration, SearchAPI


class InteractiveDemo:
    """Interactive demo for Open Deep Research."""
    
    def __init__(self):
        self.console = Console()
        self.demo_configs = self._load_demo_configs()
        
    def _load_demo_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load predefined demo configurations."""
        return {
            "fast_research": {
                "name": "Fast Research (GPT-4o-mini + Tavily)",
                "config": {
                    "research_model": "openai:gpt-4o-mini",
                    "final_report_model": "openai:gpt-4o-mini",
                    "compression_model": "openai:gpt-4o-mini",
                    "summarization_model": "openai:gpt-4o-mini",
                    "search_api": SearchAPI.TAVILY,
                    "max_researcher_iterations": 2,
                    "max_concurrent_research_units": 3
                }
            },
            "comprehensive_research": {
                "name": "Comprehensive Research (GPT-4o + Tavily)",
                "config": {
                    "research_model": "openai:gpt-4o",
                    "final_report_model": "openai:gpt-4o",
                    "compression_model": "openai:gpt-4o-mini",
                    "summarization_model": "openai:gpt-4o-mini",
                    "search_api": SearchAPI.TAVILY,
                    "max_researcher_iterations": 3,
                    "max_concurrent_research_units": 5
                }
            },
            "anthropic_research": {
                "name": "Anthropic Research (Claude + Native Search)",
                "config": {
                    "research_model": "anthropic:claude-3-5-sonnet-20241022",
                    "final_report_model": "anthropic:claude-3-5-sonnet-20241022",
                    "compression_model": "anthropic:claude-3-5-haiku-20241022",
                    "summarization_model": "anthropic:claude-3-5-haiku-20241022",
                    "search_api": SearchAPI.ANTHROPIC,
                    "max_researcher_iterations": 3,
                    "max_concurrent_research_units": 4
                }
            },
            "mixed_providers": {
                "name": "Mixed Providers (GPT-4o + Claude + Tavily)",
                "config": {
                    "research_model": "openai:gpt-4o",
                    "final_report_model": "anthropic:claude-3-5-sonnet-20241022",
                    "compression_model": "anthropic:claude-3-5-haiku-20241022",
                    "summarization_model": "openai:gpt-4o-mini",
                    "search_api": SearchAPI.TAVILY,
                    "max_researcher_iterations": 3,
                    "max_concurrent_research_units": 5
                }
            }
        }
    
    def display_welcome(self):
        """Display welcome message and features."""
        welcome_text = """
[bold blue]🔬 Open Deep Research - Interactive Demo[/bold blue]

Welcome to the comprehensive demo of Open Deep Research!

[bold green]Features demonstrated:[/bold green]
• Multi-model support (OpenAI, Anthropic, Google)
• Multiple search APIs (Tavily, OpenAI, Anthropic)
• Configurable research workflows
• Real-time progress tracking
• Comprehensive report generation

[bold yellow]Prerequisites:[/bold yellow]
• API keys configured in .env file
• Internet connection for search APIs
        """
        self.console.print(Panel(welcome_text, title="Welcome", border_style="blue"))
    
    def check_environment(self) -> bool:
        """Check if required environment variables are set."""
        required_vars = ["OPENAI_API_KEY", "TAVILY_API_KEY"]
        optional_vars = ["ANTHROPIC_API_KEY", "GOOGLE_API_KEY"]
        
        missing_required = [var for var in required_vars if not os.getenv(var)]
        missing_optional = [var for var in optional_vars if not os.getenv(var)]
        
        if missing_required:
            self.console.print(f"[bold red]Error:[/bold red] Missing required environment variables: {', '.join(missing_required)}")
            self.console.print("Please set them in your .env file.")
            return False
        
        if missing_optional:
            self.console.print(f"[yellow]Warning:[/yellow] Missing optional environment variables: {', '.join(missing_optional)}")
            self.console.print("Some configurations may not work without these.")
        
        self.console.print("[green]✓[/green] Environment check passed!")
        return True
    
    def select_configuration(self) -> Configuration:
        """Allow user to select a research configuration."""
        self.console.print("\n[bold]Available Research Configurations:[/bold]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Configuration", min_width=20)
        table.add_column("Description", min_width=30)
        
        config_list = list(self.demo_configs.items())
        for i, (key, config_info) in enumerate(config_list, 1):
            description = f"Models: {config_info['config'].get('research_model', 'N/A')}"
            description += f" | Search: {config_info['config'].get('search_api', 'N/A').value if hasattr(config_info['config'].get('search_api', 'N/A'), 'value') else config_info['config'].get('search_api', 'N/A')}"
            table.add_row(str(i), config_info["name"], description)
        
        self.console.print(table)
        
        while True:
            try:
                choice = int(Prompt.ask("Select configuration", choices=[str(i) for i in range(1, len(config_list) + 1)]))
                selected_key = config_list[choice - 1][0]
                config_dict = self.demo_configs[selected_key]["config"]
                
                # Create Configuration object
                return Configuration(**config_dict)
            except (ValueError, IndexError):
                self.console.print("[red]Invalid choice. Please try again.[/red]")
    
    def get_research_topic(self) -> str:
        """Get research topic from user."""
        self.console.print("\n[bold]Research Topic Selection:[/bold]")
        
        # Provide some example topics
        examples = [
            "The impact of artificial intelligence on climate change research",
            "Recent developments in quantum computing applications",
            "Sustainable energy solutions for urban environments",
            "The role of machine learning in drug discovery",
            "Blockchain technology in supply chain management"
        ]
        
        self.console.print("Example topics:")
        for i, example in enumerate(examples, 1):
            self.console.print(f"  {i}. {example}")
        
        self.console.print("\nYou can use one of the examples above or enter your own topic.")
        
        use_example = Confirm.ask("Would you like to use an example topic?")
        
        if use_example:
            while True:
                try:
                    choice = int(Prompt.ask("Select example", choices=[str(i) for i in range(1, len(examples) + 1)]))
                    return examples[choice - 1]
                except (ValueError, IndexError):
                    self.console.print("[red]Invalid choice. Please try again.[/red]")
        else:
            return Prompt.ask("Enter your research topic")
    
    async def run_research(self, topic: str, config: Configuration) -> Optional[Dict[str, Any]]:
        """Run the research process with progress tracking."""
        self.console.print(f"\n[bold green]Starting Research:[/bold green] {topic}")
        self.console.print(f"[bold blue]Configuration:[/bold blue] {config.research_model} + {config.search_api.value}")
        
        # Prepare the input
        research_input = {
            "messages": [{"role": "user", "content": topic}]
        }
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.console
            ) as progress:
                task = progress.add_task("Conducting research...", total=None)
                
                # Run the research
                result = await deep_researcher.ainvoke(
                    research_input,
                    config={"configurable": config.model_dump()}
                )
                
                progress.update(task, description="Research completed!")
            
            return result
            
        except Exception as e:
            self.console.print(f"[bold red]Error during research:[/bold red] {str(e)}")
            return None
    
    def display_results(self, result: Dict[str, Any], topic: str):
        """Display the research results."""
        if not result:
            return
        
        self.console.print("\n" + "="*80)
        self.console.print(f"[bold green]Research Results for:[/bold green] {topic}")
        self.console.print("="*80)
        
        # Display final report
        if "final_report" in result:
            self.console.print("\n[bold blue]Final Report:[/bold blue]")
            self.console.print(Panel(result["final_report"], border_style="blue"))
        
        # Display raw notes if available
        if "notes" in result and result["notes"]:
            show_notes = Confirm.ask("\nWould you like to see the research notes?", default=False)
            if show_notes:
                self.console.print("\n[bold yellow]Research Notes:[/bold yellow]")
                for i, note in enumerate(result["notes"], 1):
                    self.console.print(f"\n[dim]Note {i}:[/dim]")
                    self.console.print(note)
        
        # Save results option
        save_results = Confirm.ask("\nWould you like to save the results to a file?", default=True)
        if save_results:
            self.save_results(result, topic)
    
    def save_results(self, result: Dict[str, Any], topic: str):
        """Save research results to a file."""
        # Create results directory
        results_dir = Path("demo_results")
        results_dir.mkdir(exist_ok=True)
        
        # Generate filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')[:50]
        filename = results_dir / f"research_{safe_topic}.md"
        
        # Create markdown content
        content = f"# Research Report: {topic}\n\n"
        content += f"Generated by Open Deep Research\n\n"
        
        if "final_report" in result:
            content += "## Final Report\n\n"
            content += result["final_report"] + "\n\n"
        
        if "notes" in result and result["notes"]:
            content += "## Research Notes\n\n"
            for i, note in enumerate(result["notes"], 1):
                content += f"### Note {i}\n\n"
                content += note + "\n\n"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.console.print(f"[green]✓[/green] Results saved to: {filename}")
    
    async def run_demo(self):
        """Run the interactive demo."""
        self.display_welcome()
        
        if not self.check_environment():
            return
        
        while True:
            try:
                # Select configuration
                config = self.select_configuration()
                
                # Get research topic
                topic = self.get_research_topic()
                
                # Run research
                result = await self.run_research(topic, config)
                
                # Display results
                self.display_results(result, topic)
                
                # Ask if user wants to continue
                if not Confirm.ask("\nWould you like to conduct another research?", default=True):
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Demo interrupted by user.[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
                if not Confirm.ask("Would you like to continue?", default=True):
                    break
        
        self.console.print("\n[bold blue]Thank you for using Open Deep Research Demo![/bold blue]")


async def main():
    """Main entry point for the demo."""
    demo = InteractiveDemo()
    await demo.run_demo()


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("src/open_deep_research").exists():
        print("Error: Please run this demo from the project root directory.")
        sys.exit(1)
    
    asyncio.run(main())