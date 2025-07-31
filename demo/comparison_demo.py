#!/usr/bin/env python3
"""
Model Comparison Demo for Open Deep Research

This demo compares research quality across different model providers
and configurations to showcase the flexibility of the system.
"""

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.table import Table
from rich.layout import Layout
import json

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from open_deep_research.deep_researcher import deep_researcher
from open_deep_research.configuration import Configuration, SearchAPI


class ModelComparisonDemo:
    """Demo comparing different model providers and configurations."""
    
    def __init__(self):
        self.console = Console()
        self.comparison_configs = self._get_comparison_configs()
        
    def _get_comparison_configs(self) -> List[Dict[str, Any]]:
        """Get different configurations for comparison."""
        configs = []
        
        # Check which API keys are available
        has_openai = bool(os.getenv("OPENAI_API_KEY"))
        has_anthropic = bool(os.getenv("ANTHROPIC_API_KEY"))
        has_google = bool(os.getenv("GOOGLE_API_KEY"))
        
        if has_openai:
            configs.extend([
                {
                    "name": "OpenAI GPT-4o (Comprehensive)",
                    "provider": "OpenAI",
                    "config": Configuration(
                        research_model="openai:gpt-4o",
                        final_report_model="openai:gpt-4o",
                        compression_model="openai:gpt-4o-mini",
                        summarization_model="openai:gpt-4o-mini",
                        search_api=SearchAPI.TAVILY,
                        max_researcher_iterations=3,
                        max_concurrent_research_units=5
                    )
                },
                {
                    "name": "OpenAI GPT-4o-mini (Fast)",
                    "provider": "OpenAI",
                    "config": Configuration(
                        research_model="openai:gpt-4o-mini",
                        final_report_model="openai:gpt-4o-mini",
                        compression_model="openai:gpt-4o-mini",
                        summarization_model="openai:gpt-4o-mini",
                        search_api=SearchAPI.TAVILY,
                        max_researcher_iterations=2,
                        max_concurrent_research_units=3
                    )
                }
            ])
        
        if has_anthropic:
            configs.extend([
                {
                    "name": "Anthropic Claude (Sonnet)",
                    "provider": "Anthropic",
                    "config": Configuration(
                        research_model="anthropic:claude-3-5-sonnet-20241022",
                        final_report_model="anthropic:claude-3-5-sonnet-20241022",
                        compression_model="anthropic:claude-3-5-haiku-20241022",
                        summarization_model="anthropic:claude-3-5-haiku-20241022",
                        search_api=SearchAPI.TAVILY,  # Use Tavily instead of native search for reliability
                        max_researcher_iterations=3,
                        max_concurrent_research_units=4
                    )
                }
            ])
        
        if has_google:
            configs.append({
                "name": "Google Gemini",
                "provider": "Google",
                "config": Configuration(
                    research_model="google_genai:gemini-1.5-pro",
                    final_report_model="google_genai:gemini-1.5-pro",
                    compression_model="google_genai:gemini-1.5-flash",
                    summarization_model="google_genai:gemini-1.5-flash",
                    search_api=SearchAPI.TAVILY,
                    max_researcher_iterations=3,
                    max_concurrent_research_units=4
                )
            })
        
        # Mixed provider configuration if multiple APIs available
        if has_openai and has_anthropic:
            configs.append({
                "name": "Mixed Providers (Best of Both)",
                "provider": "Mixed",
                "config": Configuration(
                    research_model="openai:gpt-4o",
                    final_report_model="anthropic:claude-3-5-sonnet-20241022",
                    compression_model="anthropic:claude-3-5-haiku-20241022",
                    summarization_model="openai:gpt-4o-mini",
                    search_api=SearchAPI.TAVILY,
                    max_researcher_iterations=3,
                    max_concurrent_research_units=5
                )
            })
        
        return configs
    
    def display_intro(self):
        """Display introduction to the comparison demo."""
        intro_text = """
[bold blue]🔬 Model Comparison Demo[/bold blue]

This demo compares research quality across different model providers
and configurations using the same research topic.

[bold green]What we compare:[/bold green]
• Research depth and accuracy
• Response time and efficiency
• Report structure and quality
• Citation and source quality
• Cost-effectiveness

[bold yellow]Available Providers:[/bold yellow]
• OpenAI (GPT-4o, GPT-4o-mini)
• Anthropic (Claude 3.5 Sonnet/Haiku)
• Google (Gemini 1.5 Pro/Flash)
• Mixed provider configurations
        """
        self.console.print(Panel(intro_text, title="Model Comparison", border_style="blue"))
    
    async def run_comparison_research(self, topic: str) -> List[Dict[str, Any]]:
        """Run research using all available configurations."""
        results = []
        
        total_configs = len(self.comparison_configs)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=self.console
        ) as progress:
            main_task = progress.add_task("Running model comparison...", total=total_configs)
            
            for i, config_info in enumerate(self.comparison_configs):
                config_name = config_info["name"]
                provider = config_info["provider"]
                config = config_info["config"]
                
                progress.update(main_task, description=f"Testing {config_name}...")
                
                start_time = time.time()
                
                try:
                    research_input = {
                        "messages": [{"role": "user", "content": topic}]
                    }
                    
                    result = await deep_researcher.ainvoke(
                        research_input,
                        config={"configurable": config.model_dump()}
                    )
                    
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    results.append({
                        "config_name": config_name,
                        "provider": provider,
                        "config": config,
                        "result": result,
                        "duration": duration,
                        "success": True,
                        "error": None
                    })
                    
                    self.console.print(f"[green]✓[/green] {config_name} completed in {duration:.1f}s")
                
                except Exception as e:
                    end_time = time.time()
                    duration = end_time - start_time
                    
                    results.append({
                        "config_name": config_name,
                        "provider": provider,
                        "config": config,
                        "result": None,
                        "duration": duration,
                        "success": False,
                        "error": str(e)
                    })
                    
                    self.console.print(f"[red]✗[/red] {config_name} failed: {str(e)}")
                
                progress.update(main_task, advance=1)
        
        return results
    
    def analyze_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze and compare the results."""
        analysis = {
            "total_configs": len(results),
            "successful_configs": len([r for r in results if r["success"]]),
            "failed_configs": len([r for r in results if not r["success"]]),
            "average_duration": sum(r["duration"] for r in results if r["success"]) / max(1, len([r for r in results if r["success"]])),
            "fastest_config": None,
            "slowest_config": None,
            "longest_report": None,
            "shortest_report": None,
            "provider_performance": {}
        }
        
        successful_results = [r for r in results if r["success"]]
        
        if successful_results:
            # Find fastest and slowest
            analysis["fastest_config"] = min(successful_results, key=lambda x: x["duration"])
            analysis["slowest_config"] = max(successful_results, key=lambda x: x["duration"])
            
            # Find longest and shortest reports
            results_with_reports = [r for r in successful_results if r["result"] and "final_report" in r["result"]]
            if results_with_reports:
                analysis["longest_report"] = max(results_with_reports, key=lambda x: len(x["result"]["final_report"]))
                analysis["shortest_report"] = min(results_with_reports, key=lambda x: len(x["result"]["final_report"]))
            
            # Provider performance
            provider_stats = {}
            for result in successful_results:
                provider = result["provider"]
                if provider not in provider_stats:
                    provider_stats[provider] = {"count": 0, "total_duration": 0, "reports": []}
                
                provider_stats[provider]["count"] += 1
                provider_stats[provider]["total_duration"] += result["duration"]
                
                if result["result"] and "final_report" in result["result"]:
                    provider_stats[provider]["reports"].append(len(result["result"]["final_report"]))
            
            for provider, stats in provider_stats.items():
                analysis["provider_performance"][provider] = {
                    "average_duration": stats["total_duration"] / stats["count"],
                    "average_report_length": sum(stats["reports"]) / len(stats["reports"]) if stats["reports"] else 0,
                    "success_rate": stats["count"] / len([r for r in results if r["provider"] == provider])
                }
        
        return analysis
    
    def display_comparison_results(self, results: List[Dict[str, Any]], analysis: Dict[str, Any], topic: str):
        """Display comprehensive comparison results."""
        self.console.print(f"\n[bold green]📊 Comparison Results for:[/bold green] {topic}")
        self.console.print("="*80)
        
        # Summary table
        summary_table = Table(title="Performance Summary", show_header=True, header_style="bold magenta")
        summary_table.add_column("Configuration", style="cyan", min_width=20)
        summary_table.add_column("Provider", style="blue", min_width=12)
        summary_table.add_column("Status", style="green", min_width=10)
        summary_table.add_column("Duration (s)", style="yellow", min_width=12)
        summary_table.add_column("Report Length", style="white", min_width=15)
        
        for result in results:
            status = "✓ Success" if result["success"] else "✗ Failed"
            duration = f"{result['duration']:.1f}"
            
            if result["success"] and result["result"] and "final_report" in result["result"]:
                report_length = len(result["result"]["final_report"])
                report_length_str = f"{report_length:,} chars"
            else:
                report_length_str = "N/A"
            
            summary_table.add_row(
                result["config_name"],
                result["provider"],
                status,
                duration,
                report_length_str
            )
        
        self.console.print(summary_table)
        
        # Analysis summary
        if analysis["successful_configs"] > 0:
            self.console.print(f"\n[bold blue]📈 Analysis Summary:[/bold blue]")
            self.console.print(f"• Successful configurations: {analysis['successful_configs']}/{analysis['total_configs']}")
            self.console.print(f"• Average duration: {analysis['average_duration']:.1f} seconds")
            
            if analysis["fastest_config"]:
                self.console.print(f"• Fastest: {analysis['fastest_config']['config_name']} ({analysis['fastest_config']['duration']:.1f}s)")
            
            if analysis["slowest_config"]:
                self.console.print(f"• Slowest: {analysis['slowest_config']['config_name']} ({analysis['slowest_config']['duration']:.1f}s)")
            
            # Provider performance
            if analysis["provider_performance"]:
                self.console.print(f"\n[bold yellow]🏆 Provider Performance:[/bold yellow]")
                for provider, stats in analysis["provider_performance"].items():
                    self.console.print(f"• {provider}: {stats['average_duration']:.1f}s avg, {stats['average_report_length']:.0f} chars avg")
        
        # Show sample reports
        successful_results = [r for r in results if r["success"] and r["result"] and "final_report" in r["result"]]
        if successful_results:
            self.console.print(f"\n[bold blue]📄 Sample Report Previews:[/bold blue]")
            
            for i, result in enumerate(successful_results[:3]):  # Show first 3 successful results
                preview = result["result"]["final_report"][:300] + "..." if len(result["result"]["final_report"]) > 300 else result["result"]["final_report"]
                self.console.print(Panel(
                    preview,
                    title=f"{result['config_name']} ({result['duration']:.1f}s)",
                    border_style="blue"
                ))
    
    def save_comparison_results(self, results: List[Dict[str, Any]], analysis: Dict[str, Any], topic: str):
        """Save detailed comparison results."""
        # Create comparison results directory
        results_dir = Path("demo_results/comparisons")
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_topic = safe_topic.replace(' ', '_')[:40]
        timestamp = int(time.time())
        
        # Save detailed results as JSON
        json_filename = results_dir / f"comparison_{safe_topic}_{timestamp}.json"
        
        # Prepare data for JSON (remove non-serializable parts)
        json_data = {
            "topic": topic,
            "timestamp": timestamp,
            "analysis": analysis,
            "results": []
        }
        
        for result in results:
            json_result = {
                "config_name": result["config_name"],
                "provider": result["provider"],
                "duration": result["duration"],
                "success": result["success"],
                "error": result["error"],
                "report_length": len(result["result"]["final_report"]) if result["success"] and result["result"] and "final_report" in result["result"] else 0
            }
            json_data["results"].append(json_result)
        
        with open(json_filename, 'w') as f:
            json.dump(json_data, f, indent=2)
        
        # Save markdown report
        md_filename = results_dir / f"comparison_{safe_topic}_{timestamp}.md"
        
        content = f"# Model Comparison Report: {topic}\n\n"
        content += f"Generated at: {time.ctime(timestamp)}\n\n"
        
        content += "## Summary\n\n"
        content += f"- Total configurations tested: {analysis['total_configs']}\n"
        content += f"- Successful runs: {analysis['successful_configs']}\n"
        content += f"- Failed runs: {analysis['failed_configs']}\n"
        content += f"- Average duration: {analysis['average_duration']:.1f} seconds\n\n"
        
        content += "## Configuration Results\n\n"
        for result in results:
            content += f"### {result['config_name']}\n"
            content += f"- Provider: {result['provider']}\n"
            content += f"- Duration: {result['duration']:.1f} seconds\n"
            content += f"- Status: {'Success' if result['success'] else 'Failed'}\n"
            
            if result['success'] and result['result'] and 'final_report' in result['result']:
                content += f"- Report length: {len(result['result']['final_report']):,} characters\n"
                content += f"\n#### Report Preview:\n"
                preview = result['result']['final_report'][:500] + "..." if len(result['result']['final_report']) > 500 else result['result']['final_report']
                content += f"```\n{preview}\n```\n"
            elif not result['success']:
                content += f"- Error: {result['error']}\n"
            
            content += "\n"
        
        content += "## Analysis\n\n"
        if analysis["fastest_config"]:
            content += f"**Fastest configuration:** {analysis['fastest_config']['config_name']} ({analysis['fastest_config']['duration']:.1f}s)\n\n"
        
        if analysis["provider_performance"]:
            content += "**Provider Performance:**\n"
            for provider, stats in analysis["provider_performance"].items():
                content += f"- {provider}: {stats['average_duration']:.1f}s average duration\n"
        
        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.console.print(f"[green]✓[/green] Comparison results saved to:")
        self.console.print(f"  JSON: {json_filename}")
        self.console.print(f"  Markdown: {md_filename}")
    
    async def run_demo(self):
        """Run the model comparison demo."""
        self.display_intro()
        
        if not self.comparison_configs:
            self.console.print("[red]Error:[/red] No API keys available for comparison.")
            self.console.print("Please set at least OPENAI_API_KEY and TAVILY_API_KEY in your .env file.")
            return
        
        self.console.print(f"\n[bold]Available configurations for comparison:[/bold] {len(self.comparison_configs)}")
        for config in self.comparison_configs:
            self.console.print(f"• {config['name']} ({config['provider']})")
        
        # Demo research topic
        topic = "The impact of large language models on software development productivity"
        
        self.console.print(f"\n[bold yellow]Research Topic:[/bold yellow] {topic}")
        self.console.print("This topic will be used to compare all available configurations.\n")
        
        try:
            # Run comparison research
            results = await self.run_comparison_research(topic)
            
            # Analyze results
            analysis = self.analyze_results(results)
            
            # Display results
            self.display_comparison_results(results, analysis, topic)
            
            # Save results
            self.save_comparison_results(results, analysis, topic)
            
            self.console.print("\n[bold blue]🎉 Model comparison demo completed![/bold blue]")
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Demo interrupted by user.[/yellow]")
        except Exception as e:
            self.console.print(f"[bold red]Error during comparison:[/bold red] {str(e)}")


async def main():
    """Main entry point for the comparison demo."""
    demo = ModelComparisonDemo()
    await demo.run_demo()


if __name__ == "__main__":
    # Check if we're in the right directory
    if not Path("src/open_deep_research").exists():
        print("Error: Please run this demo from the project root directory.")
        sys.exit(1)
    
    asyncio.run(main())