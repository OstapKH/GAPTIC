# 🧬 GAPTIC
## Genetic Algorithm Prompt-Tuned Injection for Code

GAPTIC is a sophisticated genetic algorithm-based approach to prompt-tuned injection for code generation, designed to explore and optimize prompt engineering strategies.

## 📋 Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Ollama Commands](#ollama-commands)
- [CodeQL Analysis](#codeql-analysis)

## 🚀 Installation

### Prerequisites

Before getting started, you'll need to install Ollama. Visit [Ollama's official website](https://ollama.ai/) for detailed installation instructions.

### Ollama Commands

#### 🔧 Basic Operations
```bash
# Download a model
ollama pull llama3.1:8b

# Run a model
ollama run llama3.1:8b

# List available models
ollama list

# Delete a model
ollama delete llama3.1:8b
```

#### ⚙️ Model Execution
```bash
# Generate code with a prompt
ollama generate --model llama3.1:8b --prompt "print('Hello, world!')"

# Run with specific temperature
ollama run llama3.1:8b --temperature 0.5
```

#### 💻 Popular Code Models
```bash
# CodeLlama 7B Instruct
ollama run codellama:7b-instruct

# StarCoder 2 Instruct
ollama run starcoder2:3b

# DeepSeek-R1 1.5B
ollama run deepseek-r1:1.5b
```

## 🔍 CodeQL Analysis

### Installation

#### macOS (using Homebrew)
```bash
brew install codeql
```

#### Other Systems
1. Visit https://github.com/github/codeql-cli-binaries/releases
2. Download the appropriate version for your OS
3. Extract the archive and add the directory to your PATH

### Setup and Usage

1. Create your workspace:
```bash
mkdir codeql-analysis
cd codeql-analysis
```

2. Create a CodeQL database:
```bash
codeql database create vuln-subprocess-db --language=python --source-root=..
```

3. Set up CodeQL libraries:
```bash
# Create directory for CodeQL libraries
mkdir -p codeql-home/codeql-repo

# Clone the CodeQL repository
git clone https://github.com/github/codeql.git codeql-home/codeql-repo
```

4. Run analysis:
```bash
# Using built-in CodeQL queries
codeql database analyze vuln-subprocess-db \
  codeql-home/codeql-repo/python/ql/src/Security/CWE-078 \
  --format=sarif-latest \
  --output=subprocess-results.sarif

# Basic analysis
codeql database analyze subprocess-vuln.ql --format=sarif-latest --output=subprocess-vuln.sarif
```