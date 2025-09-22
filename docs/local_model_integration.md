# CompanionAI - Local Model Implementation Guide

## Option 1: Nvidia NIM Integration
```python
# Replace Groq with Nvidia NIM API
from openai import OpenAI

# Nvidia NIM client (compatible with OpenAI API)
nim_client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

# Use models like:
# - meta/llama-3.1-8b-instruct
# - microsoft/phi-3-medium-4k-instruct
# - mistralai/mixtral-8x7b-instruct-v0.1
```

## Option 2: Local Model with Ollama
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a good local model
ollama pull llama3.1:8b
ollama pull phi3:medium
```

## Option 3: Transformers Local Model
```python
from transformers import AutoTokenizer, AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    torch_dtype=torch.float16,
    device_map="auto"
)
```

## Benefits of Each Approach:
- **Nvidia NIM**: Production-ready, optimized inference
- **Ollama**: Easy local setup, privacy-focused
- **Transformers**: Full control, customizable