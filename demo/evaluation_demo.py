#!/usr/bin/env python3
"""
Open Deep Research - Evaluation Demo

This demo showcases the evaluation framework for research quality assessment
and comparison capabilities.
"""

import sys
from pathlib import Path
from typing import Dict, Any, List
from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import json
import time
import random

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


class EvaluationDemo:
    """Evaluation demo for Open Deep Research."""
    
    def __init__(self):
        self.console = Console()
        self.sample_reports = self._generate_sample_reports()
        
    def _generate_sample_reports(self) -> List[Dict[str, Any]]:
        """Generate sample research reports for evaluation."""
        return [
            {
                "id": "report_1",
                "topic": "AI in Climate Change Research",
                "model": "openai:gpt-4o",
                "search_api": "tavily",
                "final_report": """
# AI in Climate Change Research

## Executive Summary
Artificial Intelligence is revolutionizing climate change research through advanced modeling, 
prediction systems, and data analysis capabilities.

## Key Findings
1. Machine learning models improve climate prediction accuracy by 25%
2. AI-powered satellite analysis enables real-time deforestation monitoring
3. Deep learning algorithms optimize renewable energy grid management

## Detailed Analysis
Current AI applications include:
- Climate modeling and simulation
- Environmental monitoring
- Carbon footprint optimization
- Renewable energy forecasting

## Recommendations
1. Increase investment in AI climate research
2. Develop standardized AI climate datasets
3. Foster international AI collaboration
                """,
                "sources_count": 15,
                "research_time": 45.2
            },
            {
                "id": "report_2", 
                "topic": "AI in Climate Change Research",
                "model": "anthropic:claude-3-5-sonnet-20241022",
                "search_api": "anthropic_web_search",
                "final_report": """
# Artificial Intelligence Applications in Climate Science

## Overview
This comprehensive analysis examines how artificial intelligence technologies
are transforming climate change research methodologies and outcomes.

## Core Findings
- AI enhances climate model precision through ensemble learning
- Satellite imagery analysis via deep learning identifies environmental changes
- Predictive algorithms support climate adaptation strategies
- Machine learning optimizes sustainable resource management

## Technical Analysis
The integration of AI in climate research encompasses:
1. Data processing and pattern recognition
2. Predictive modeling and forecasting
3. Real-time monitoring systems
4. Decision support frameworks

## Strategic Implications
Organizations should prioritize AI development for climate applications.
                """,
                "sources_count": 12,
                "research_time": 38.7
            },
            {
                "id": "report_3",
                "topic": "Quantum Computing Applications", 
                "model": "openai:gpt-4o-mini",
                "search_api": "tavily",
                "final_report": """
# Quantum Computing Applications

## Summary
Quantum computing shows promise in cryptography, optimization, and simulation.

## Findings
- Quantum algorithms solve certain problems exponentially faster
- Current limitations include error rates and coherence time
- Commercial applications emerging in finance and pharmaceuticals

## Applications
1. Cryptography and security
2. Drug discovery
3. Financial modeling
4. Traffic optimization
                """,
                "sources_count": 8,
                "research_time": 22.1
            }
        ]
    
    def display_welcome(self):
        """Display welcome message for evaluation demo."""
        welcome_text = """
[bold blue]📊 Open Deep Research - Evaluation Demo[/bold blue]

This demo showcases the research evaluation framework:

[bold green]Evaluation Features:[/bold green]
• Report quality assessment
• Multi-model comparison analysis
• Performance metrics calculation
• Research effectiveness scoring

[bold yellow]Demo Capabilities:[/bold yellow]
• Compare reports from different models
• Analyze research quality metrics
• Generate evaluation summaries
• Export comparison results
        """
        self.console.print(Panel(welcome_text, title="Evaluation Demo", border_style="blue"))
    
    def show_sample_reports(self):
        """Display available sample reports."""
        self.console.print("\n[bold]Sample Research Reports:[/bold]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=12)
        table.add_column("Topic", min_width=20)
        table.add_column("Model", min_width=20)
        table.add_column("Search API", min_width=15)
        table.add_column("Sources", justify="right")
        table.add_column("Time (s)", justify="right")
        
        for report in self.sample_reports:
            table.add_row(
                report["id"],
                report["topic"],
                report["model"],
                report["search_api"],
                str(report["sources_count"]),
                f"{report['research_time']:.1f}"
            )
        
        self.console.print(table)
    
    def evaluate_report_quality(self, report: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate the quality of a research report."""
        # Simulate evaluation process
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Evaluating report quality...", total=None)
            time.sleep(2)  # Simulate processing
        
        # Generate mock evaluation scores
        report_length = len(report["final_report"])
        sources = report["sources_count"]
        
        # Quality metrics (simulated)
        comprehensiveness = min(1.0, report_length / 1000)
        source_diversity = min(1.0, sources / 20)
        structure_quality = random.uniform(0.7, 0.95)
        accuracy_score = random.uniform(0.75, 0.92)
        clarity_score = random.uniform(0.8, 0.95)
        
        return {
            "comprehensiveness": comprehensiveness,
            "source_diversity": source_diversity, 
            "structure_quality": structure_quality,
            "accuracy": accuracy_score,
            "clarity": clarity_score,
            "overall_score": (comprehensiveness + source_diversity + structure_quality + accuracy_score + clarity_score) / 5
        }
    
    def compare_reports(self, reports: List[Dict[str, Any]]):
        """Compare multiple research reports."""
        self.console.print("\n[bold blue]Report Comparison Analysis[/bold blue]")
        
        # Evaluate each report
        evaluations = []
        for report in reports:
            self.console.print(f"\nEvaluating: {report['id']} ({report['model']})")
            evaluation = self.evaluate_report_quality(report)
            evaluation["report_id"] = report["id"]
            evaluation["model"] = report["model"]
            evaluation["search_api"] = report["search_api"]
            evaluations.append(evaluation)
        
        # Display comparison table
        self.console.print("\n[bold]Evaluation Results:[/bold]")
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Report", min_width=12)
        table.add_column("Model", min_width=20)
        table.add_column("Overall", justify="right")
        table.add_column("Comprehensive", justify="right")
        table.add_column("Sources", justify="right")
        table.add_column("Structure", justify="right")
        table.add_column("Accuracy", justify="right")
        table.add_column("Clarity", justify="right")
        
        for eval_result in evaluations:
            table.add_row(
                eval_result["report_id"],
                eval_result["model"].split(":")[-1],
                f"{eval_result['overall_score']:.3f}",
                f"{eval_result['comprehensiveness']:.3f}",
                f"{eval_result['source_diversity']:.3f}",
                f"{eval_result['structure_quality']:.3f}",
                f"{eval_result['accuracy']:.3f}",
                f"{eval_result['clarity']:.3f}"
            )
        
        self.console.print(table)
        
        # Find best performing report
        best_report = max(evaluations, key=lambda x: x["overall_score"])
        self.console.print(f"\n[bold green]Best Performing Report:[/bold green] {best_report['report_id']} ({best_report['model']})")
        self.console.print(f"Overall Score: {best_report['overall_score']:.3f}")
        
        return evaluations
    
    def analyze_model_performance(self, evaluations: List[Dict[str, Any]]):
        """Analyze performance by model type."""
        self.console.print("\n[bold blue]Model Performance Analysis[/bold blue]")
        
        # Group by model
        model_scores = {}
        for eval_result in evaluations:
            model = eval_result["model"]
            if model not in model_scores:
                model_scores[model] = []
            model_scores[model].append(eval_result["overall_score"])
        
        # Calculate averages
        performance_table = Table(show_header=True, header_style="bold magenta")
        performance_table.add_column("Model", min_width=25)
        performance_table.add_column("Avg Score", justify="right")
        performance_table.add_column("Reports", justify="right")
        performance_table.add_column("Recommendation", min_width=20)
        
        for model, scores in model_scores.items():
            avg_score = sum(scores) / len(scores)
            recommendation = "Excellent" if avg_score > 0.85 else "Good" if avg_score > 0.75 else "Needs Improvement"
            
            performance_table.add_row(
                model,
                f"{avg_score:.3f}",
                str(len(scores)),
                recommendation
            )
        
        self.console.print(performance_table)
    
    def export_evaluation_results(self, evaluations: List[Dict[str, Any]]):
        """Export evaluation results to a file."""
        results_dir = Path("demo_results")
        results_dir.mkdir(exist_ok=True)
        
        filename = results_dir / "evaluation_results.json"
        
        export_data = {
            "evaluation_summary": {
                "total_reports": len(evaluations),
                "average_score": sum(e["overall_score"] for e in evaluations) / len(evaluations),
                "best_model": max(evaluations, key=lambda x: x["overall_score"])["model"],
                "evaluation_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            },
            "detailed_results": evaluations
        }
        
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        self.console.print(f"\n[green]✓[/green] Evaluation results exported to: {filename}")
    
    async def run_demo(self):
        """Run the evaluation demo."""
        self.display_welcome()
        
        while True:
            try:
                self.console.print("\n[bold]Evaluation Demo Options:[/bold]")
                self.console.print("1. View Sample Reports")
                self.console.print("2. Evaluate Single Report") 
                self.console.print("3. Compare Multiple Reports")
                self.console.print("4. Model Performance Analysis")
                self.console.print("5. Export Results")
                self.console.print("6. Exit Demo")
                
                choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6"])
                
                if choice == "1":
                    self.show_sample_reports()
                
                elif choice == "2":
                    self.show_sample_reports()
                    report_id = Prompt.ask("Select report ID to evaluate", choices=[r["id"] for r in self.sample_reports])
                    report = next(r for r in self.sample_reports if r["id"] == report_id)
                    evaluation = self.evaluate_report_quality(report)
                    
                    self.console.print(f"\n[bold]Evaluation Results for {report_id}:[/bold]")
                    for metric, score in evaluation.items():
                        self.console.print(f"  {metric.replace('_', ' ').title()}: {score:.3f}")
                
                elif choice == "3":
                    # Compare reports on same topic
                    topic_reports = [r for r in self.sample_reports if r["topic"] == "AI in Climate Change Research"]
                    if len(topic_reports) >= 2:
                        evaluations = self.compare_reports(topic_reports)
                        self.analyze_model_performance(evaluations)
                    else:
                        self.console.print("[yellow]Not enough reports for comparison[/yellow]")
                
                elif choice == "4":
                    # Analyze all reports
                    all_evaluations = []
                    for report in self.sample_reports:
                        eval_result = self.evaluate_report_quality(report)
                        eval_result.update({
                            "report_id": report["id"],
                            "model": report["model"],
                            "search_api": report["search_api"]
                        })
                        all_evaluations.append(eval_result)
                    
                    self.analyze_model_performance(all_evaluations)
                
                elif choice == "5":
                    # Generate and export results
                    all_evaluations = []
                    self.console.print("\n[bold]Generating comprehensive evaluation...[/bold]")
                    for report in self.sample_reports:
                        eval_result = self.evaluate_report_quality(report)
                        eval_result.update({
                            "report_id": report["id"],
                            "model": report["model"],
                            "search_api": report["search_api"]
                        })
                        all_evaluations.append(eval_result)
                    
                    self.export_evaluation_results(all_evaluations)
                
                elif choice == "6":
                    break
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]Demo interrupted by user.[/yellow]")
                break
            except Exception as e:
                self.console.print(f"[bold red]Unexpected error:[/bold red] {str(e)}")
                if not Confirm.ask("Would you like to continue?", default=True):
                    break
        
        self.console.print("\n[bold blue]Thank you for exploring the Open Deep Research Evaluation Framework![/bold blue]")


async def main():
    """Main entry point for the evaluation demo."""
    demo = EvaluationDemo()
    await demo.run_demo()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())