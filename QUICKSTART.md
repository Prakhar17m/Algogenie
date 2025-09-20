# 🚀 Quick Start Guide - AlgoGenie

## Prerequisites ✅
- Python 3.8+ installed
- Docker Desktop installed and running
- OpenAI API key

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key:
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### 3. Test Setup
```bash
python test_setup.py
```

### 4. Run the Application

**Web Interface (Recommended):**
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser.

**Command Line Interface:**
```bash
python main.py
```

## What's Included

- ✅ **Web Interface**: Beautiful Streamlit app with real-time chat
- ✅ **CLI Interface**: Command-line version for quick testing
- ✅ **Docker Integration**: Safe code execution in containers
- ✅ **Multi-Agent System**: Problem solver + code executor agents
- ✅ **Error Handling**: Comprehensive error checking and validation
- ✅ **Setup Scripts**: Automated installation and testing

## Troubleshooting

### Common Issues:

1. **"OPENAI_API_KEY not found"**
   - Set your API key in the `.env` file

2. **"Docker not available"**
   - Install Docker Desktop and make sure it's running

3. **Import errors**
   - Run `pip install -r requirements.txt`

4. **Permission errors**
   - Make sure Docker Desktop is running and you have proper permissions

## Next Steps

1. Set your OpenAI API key in `.env`
2. Run `python test_setup.py` to verify everything works
3. Start coding with `streamlit run app.py`!

---

**Happy Coding! 🧠✨**
