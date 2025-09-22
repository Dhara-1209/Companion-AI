# Ollama Local Model Setup for 8GB RAM

## Installation
# Windows: Download from https://ollama.ai/download
# Or via PowerShell:
winget install Ollama.Ollama

## Best Models for 8GB RAM:
ollama pull phi3:mini        # 3.8GB - Microsoft, very efficient
ollama pull llama3.2:3b      # 2GB - Meta's latest compact model  
ollama pull gemma2:2b        # 1.6GB - Google's efficient model
ollama pull qwen2:1.5b       # 1GB - Alibaba's compact model

## Test the model:
ollama run phi3:mini "Hello! Can you help with appliance troubleshooting?"

## Memory Usage:
# phi3:mini    - Uses ~4GB RAM (perfect for 8GB system)
# llama3.2:3b  - Uses ~3GB RAM (leaves 5GB for system)
# gemma2:2b    - Uses ~2GB RAM (very light)