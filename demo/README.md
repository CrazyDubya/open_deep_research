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
- **Works in both full system mode and demo mode (no API keys required)**

### 2. Demo Runner (`demo_runner.py`)
Non-interactive demo showcasing features without requiring API keys:
- Configuration system overview
- Research workflow simulation
- Sample research outputs
- Performance comparison capabilities
- Model selection and feature exploration

### 3. Multi-Provider Comparison (`comparison_demo.py`)
Compare research quality across different:
- Model providers
- Search APIs
- Configuration settings
- Performance metrics and analysis

### 4. Evaluation Demo (`evaluation_demo.py`)
Demonstrates the evaluation framework:
- Report quality assessment
- Comparative analysis between models
- Performance metrics calculation
- Evaluation results export

### 5. Research Scenarios (`scenarios/`)
Pre-configured research scenarios:
- Academic research (ArXiv integration)
- Medical research (PubMed integration)
- Business intelligence
- Technology trends
- Scientific literature review

## Quick Start

### Option 1: Demo Mode (No API Keys Required)

Run any demo without API keys for a full feature demonstration:

```bash
# Interactive demo with mock functionality
python demo/interactive_demo.py

# Non-interactive feature showcase
python demo/demo_runner.py

# Evaluation framework demo
python demo/evaluation_demo.py
```

### Option 2: Full System Mode

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

## Demo Features

### Interactive Demo Features
- ✅ Multiple research configurations
- ✅ Real-time progress tracking
- ✅ Comprehensive report generation
- ✅ Research notes display
- ✅ Automatic file saving
- ✅ Works without API keys (demo mode)
- ✅ Full system integration when API keys available

### Evaluation Demo Features
- ✅ Report quality assessment
- ✅ Multi-model comparison
- ✅ Performance metrics calculation
- ✅ Evaluation results export
- ✅ Model recommendation system

### Demo Runner Features
- ✅ Configuration exploration
- ✅ Feature demonstrations
- ✅ Simulated research workflows
- ✅ Performance comparisons
- ✅ No API keys required

## Configuration Examples

The `configs/` directory contains example configurations for different use cases:

- `fast_research.json` - Quick research with GPT-4o-mini
- `comprehensive_research.json` - Thorough research with GPT-4o
- `anthropic_claude.json` - Claude-based research
- `mixed_providers.json` - Multi-provider research

## Demo Results

All demos save results to the `demo_results/` directory:
- Research reports in Markdown format
- Evaluation results in JSON format
- Configuration exports
- Performance analysis data

## Demo Architecture

The demo system is designed to:
1. **Work without dependencies**: Falls back to mock functionality when the full system isn't available
2. **Showcase all features**: Demonstrates every aspect of the Open Deep Research system
3. **Provide realistic output**: Uses sophisticated mock data that represents real system behavior
4. **Enable easy testing**: Allows users to explore functionality before setting up API keys

## Running Demos

Each demo can be run independently:

```bash
# Interactive research demo
cd /path/to/open_deep_research
python demo/interactive_demo.py

# Feature showcase demo
python demo/demo_runner.py

# Evaluation framework demo  
python demo/evaluation_demo.py

# Comparison demo
python demo/comparison_demo.py

# Academic research scenario
python demo/scenarios/academic_research_demo.py
```

All demos include help options and guided workflows to help users understand the Open Deep Research system capabilities.