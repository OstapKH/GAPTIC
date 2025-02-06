# GAPTIC – Genetic Algorithm Prompt-Tuned Injection for Code

GAPTIC is a genetic algorithm-based approach to prompt-tuned injection for code generation.

## Installation

### Prerequisites

First, you need to install Ollama. Visit [Ollama's official website](https://ollama.ai/) for installation instructions.

### Ollama Commands

#### Basic Commands
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

#### Model Execution
```bash
# Generate code with a prompt
ollama generate --model llama3.1:8b --prompt "print('Hello, world!')"

# Run with specific temperature
ollama run llama3.1:8b --temperature 0.5
```

#### Popular Code Models
```bash
# CodeLlama 7B Instruct
ollama run codellama:7b-instruct

# StarCoder 2 Instruct
ollama run starcoder2:3b

# DeepSeek-R1 1.5B
ollama run deepseek-r1:1.5b
```


## CodeQL Analysis

```bash
codeql database analyze subprocess-vuln.ql --format=sarif-latest --output=subprocess-vuln.sarif
```

# For macOS (using Homebrew)
brew install codeql

# For other systems, download from GitHub:
# 1. Go to https://github.com/github/codeql-cli-binaries/releases
# 2. Download the appropriate version for your OS
# 3. Extract the archive and add the directory to your PATH

# Create and navigate to a directory
mkdir codeql-analysis
cd codeql-analysis


# Create a CodeQL database for your Python code
codeql database create vuln-subprocess-db --language=python --source-root=..

# Inside the codeql-analysis directory, run the following command

# Create a directory for CodeQL libraries
mkdir -p codeql-home/codeql-repo

# Clone the CodeQL repository
git clone https://github.com/github/codeql.git codeql-home/codeql-repo


## To use built-in CodeQL queries
codeql database analyze vuln-subprocess-db \
  codeql-home/codeql-repo/python/ql/src/Security/CWE-078 \
  --format=sarif-latest \
  --output=subprocess-results.sarif