# 🔄 OpenRouter Setup Guide

## Why OpenRouter?

OpenRouter provides access to multiple AI models through a single API, including:
- **Free models** (no cost!)
- **Open-source models** (Llama, Phi, etc.)
- **Commercial models** (GPT-4, Claude, Gemini)
- **Better pricing** than direct API access

## 🚀 Quick Setup

### Step 1: Get OpenRouter API Key

1. **Visit**: https://openrouter.ai/keys
2. **Sign up** for a free account
3. **Generate** an API key
4. **Copy** the key (starts with `sk-or-...`)

### Step 2: Update Environment

Edit your `.env` file:
```env
OPENROUTER_API_KEY=sk-or-your-actual-key-here
```

### Step 3: Choose a Model

Edit `config/constant.py` to select your preferred model:

**Free Models (Recommended for testing):**
```python
MODEL = 'meta-llama/llama-3.1-8b-instruct:free'
# or
MODEL = 'microsoft/phi-3-medium-128k-instruct:free'
```

**Paid Models (Higher quality):**
```python
MODEL = 'google/gemini-flash-1.5'
# or
MODEL = 'anthropic/claude-3.5-sonnet'
# or
MODEL = 'openai/gpt-4o-mini'
```

### Step 4: Test the Setup

```bash
python test_openrouter.py
```

### Step 5: Run the Application

```bash
# CLI version
python main.py

# Web interface
python -m streamlit run app.py
```

## 📊 Available Models

### Free Models
| Model | Provider | Quality | Speed |
|-------|----------|---------|-------|
| `meta-llama/llama-3.1-8b-instruct:free` | Meta | Good | Fast |
| `microsoft/phi-3-medium-128k-instruct:free` | Microsoft | Good | Fast |
| `microsoft/phi-3-mini-4k-instruct:free` | Microsoft | Basic | Very Fast |

### Paid Models
| Model | Provider | Quality | Cost |
|-------|----------|---------|------|
| `google/gemini-flash-1.5` | Google | Excellent | Low |
| `anthropic/claude-3.5-sonnet` | Anthropic | Excellent | Medium |
| `openai/gpt-4o-mini` | OpenAI | Excellent | Low |
| `openai/gpt-4o` | OpenAI | Excellent | High |

## 🔧 Troubleshooting

### Common Issues:

1. **"Invalid API key"**
   - Check your API key is correct
   - Make sure it starts with `sk-or-`

2. **"Model not available"**
   - Try a different model from the list above
   - Check if the model name is exactly correct

3. **"Quota exceeded"**
   - Free models have usage limits
   - Consider upgrading to paid models
   - Wait for quota reset

4. **"Rate limit exceeded"**
   - Wait a few minutes and try again
   - Consider using a different model

## 💡 Tips

- **Start with free models** to test the setup
- **Use paid models** for production use
- **Monitor usage** on your OpenRouter dashboard
- **Switch models easily** by changing `config/constant.py`

## 🎯 Next Steps

Once OpenRouter is set up:
1. Run `python test_openrouter.py` to verify
2. Try `python main.py` for CLI version
3. Use `python -m streamlit run app.py` for web interface
4. Enjoy solving DSA problems with AI! 🧠✨
