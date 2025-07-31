# Open Deep Research - Comprehensive Demo

This directory contains interactive demos showcasing the full functionality of Open Deep Research.

## Available Demos

### 1. Interactive Research Demo (`interactive_demo.py`)
A comprehensive command-line interface that demonstrates:
- Multi-model support (OpenAI, Anthropic, Google)
- Different search APIs (Tavily, OpenAI Web Search, Anthropic Web Search)
- MCP server integration
- Research workflow visualization
- Report generation with different formats

### 2. Multi-Provider Comparison (`comparison_demo.py`)
Compare research quality across different:
- Model providers
- Search APIs
- Configuration settings

### 3. Research Scenarios (`scenarios/`)
Pre-configured research scenarios:
- Academic research (ArXiv integration)
- Medical research (PubMed integration)
- Business intelligence
- Technology trends
- Scientific literature review

### 4. Evaluation Demo (`evaluation_demo.py`)
Demonstrates the evaluation framework:
- Report quality assessment
- Comparative analysis
- Performance metrics

## Quick Start

1. Set up your environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. Run the interactive demo:
```bash
python demo/interactive_demo.py
```

3. Try different scenarios:
```bash
python demo/scenarios/academic_research_demo.py
```

## Configuration Examples

The `configs/` directory contains example configurations for different use cases.