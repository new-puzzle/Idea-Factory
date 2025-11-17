# 🚀 Quick Start Guide - Idea Factory

Get started with Idea Factory in under 5 minutes!

## Prerequisites

- Python 3.9 or higher installed
- Anthropic API key ([Get one free](https://console.anthropic.com/))

## Installation

### Option 1: Using the Run Script (Easiest)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Idea-Factory

# 2. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Run the script
./run.sh
```

The script will guide you through running the app!

### Option 2: Manual Setup

```bash
# 1. Clone and navigate
git clone <your-repo-url>
cd Idea-Factory

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install frontend dependencies
cd frontend
pip install -r requirements.txt

# 4. Set up API key
cd ..
cp .env.example .env
# Edit .env: ANTHROPIC_API_KEY=your_actual_key_here

# 5. Run the app
cd frontend
streamlit run app.py
```

## First Steps

1. **Open your browser** to http://localhost:8501

2. **Try an example**:
   - Click on "blockchain + education"
   - Wait for 10 creative ideas to generate

3. **Refine an idea**:
   - Go to the "Results" tab
   - Click "Refine" on any idea you like
   - View the detailed plan in "Refinement" tab

4. **Visualize**:
   - Go to "Visualization" tab
   - Click "Create Mind Map"
   - See your ideas as a structured diagram

## Example Topics to Try

- `quantum physics + storytelling`
- `artificial intelligence + agriculture`
- `psychology + video games`
- `renewable energy + fashion`
- `blockchain + healthcare`
- `virtual reality + education`

## Mobile Usage

Simply open the same URL on your mobile device!

The app is fully optimized for mobile browsers:
- Large, tappable buttons
- Responsive layout
- Easy navigation

## Troubleshooting

### "Module not found" error
```bash
# Make sure you installed dependencies
cd frontend
pip install -r requirements.txt
```

### "API key not found" error
```bash
# Check your .env file exists and has the key
cat .env
# Should show: ANTHROPIC_API_KEY=sk-ant-...

# Make sure you're running from the right directory
export $(cat .env | xargs)  # Linux/Mac
streamlit run app.py
```

### Port already in use
```bash
# Run on a different port
streamlit run app.py --server.port 8502
```

### App won't start
```bash
# Check Python version (needs 3.9+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Tips for Best Results

### Topic Ideas
- **Combine different fields**: Mix technical + creative (e.g., "robotics + dance")
- **Be specific**: "machine learning + urban planning" vs just "AI"
- **Think cross-disciplinary**: Unexpected combinations often yield the best ideas!

### Refining Ideas
- Select ideas that resonate with your interests
- The refinement provides actionable tasks and resources
- Download plans for offline reference

### Visualization
- Use mind maps for presentations
- Great for brainstorming sessions
- Export the Mermaid code to use in other tools

## Next Steps

1. ✅ Generate your first set of ideas
2. ✅ Refine an interesting idea
3. ✅ Create a visualization
4. 📖 Read [README.md](README.md) for full features
5. 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) to deploy your own instance
6. 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Getting Help

- Check the [README](README.md) for detailed documentation
- Review code comments in `frontend/app.py`
- Open an issue on GitHub

## Pro Tips

**Save Your Ideas**:
- Use the download buttons to save ideas as text files
- Copy Mermaid code for use in documentation

**API Usage**:
- Each idea generation uses ~1000 tokens
- Each refinement uses ~2000 tokens
- Monitor usage in Anthropic console

**Performance**:
- Ideas are cached in session state
- Refresh browser to start fresh
- Close unused tabs to save memory

**Mobile**:
- Add to home screen for app-like experience
- Works offline for viewing saved ideas
- Use landscape mode for mind maps

---

**Happy Idea Generating! 💡**

Built with ❤️ using Streamlit and Claude AI
