# Contributing to Idea Factory

Thank you for your interest in contributing to Idea Factory! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- Report bugs and issues
- Suggest new features or improvements
- Improve documentation
- Submit code changes
- Share your use cases and ideas

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the problem
3. **Expected Behavior**: What you expected to happen
4. **Actual Behavior**: What actually happened
5. **Environment**:
   - OS (Windows/Mac/Linux)
   - Python version
   - Browser (if frontend issue)
6. **Screenshots**: If applicable
7. **Error Messages**: Full error messages or stack traces

## 💡 Suggesting Features

When suggesting new features:

1. **Use Case**: Describe the problem or use case
2. **Proposed Solution**: How you envision it working
3. **Alternatives**: Any alternative solutions you've considered
4. **Examples**: Examples or mockups if applicable

## 🔧 Development Setup

### Prerequisites

- Python 3.9+
- Git
- Anthropic API key

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR_USERNAME/Idea-Factory.git
   cd Idea-Factory
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   # Frontend
   cd frontend
   pip install -r requirements.txt

   # Backend
   cd ../backend
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

5. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Code Style Guidelines

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Add comments for complex logic

**Example:**

```python
def generate_ideas(topic: str) -> list[str]:
    """
    Generate creative ideas based on the given topic.

    Args:
        topic: The topic or concept combination to generate ideas for

    Returns:
        List of generated ideas as strings

    Raises:
        ValueError: If topic is empty
        APIError: If Claude API call fails
    """
    if not topic:
        raise ValueError("Topic cannot be empty")

    # Implementation here
    pass
```

### Streamlit UI

- Keep UI components organized by function
- Use consistent spacing and styling
- Ensure mobile responsiveness
- Add helpful tooltips and placeholders
- Use session state appropriately

### FastAPI Backend

- Use type hints for all parameters and return types
- Document endpoints with clear docstrings
- Handle errors gracefully
- Validate input data with Pydantic models

## 🧪 Testing

Before submitting:

1. **Manual Testing**
   - Test all affected features
   - Test on different screen sizes (mobile/desktop)
   - Test error scenarios
   - Verify no console errors

2. **Code Quality**
   - Run linting: `pylint your_file.py`
   - Format code: `black your_file.py`
   - Check types: `mypy your_file.py`

## 📤 Submitting Changes

### Pull Request Process

1. **Update your fork**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: your feature description"
   ```

   **Commit Message Format:**
   - `feat: Add new visualization option`
   - `fix: Correct API error handling`
   - `docs: Update README with deployment info`
   - `style: Format code with black`
   - `refactor: Simplify idea generation logic`
   - `test: Add tests for refinement endpoint`

3. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create Pull Request**
   - Go to the original repository on GitHub
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template:
     - **Description**: What changes you made and why
     - **Testing**: How you tested the changes
     - **Screenshots**: If UI changes
     - **Checklist**: Complete the checklist

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] Performance improvement

## Testing
- [ ] Tested locally
- [ ] Tested on mobile
- [ ] No console errors
- [ ] Error handling works

## Screenshots
(if applicable)

## Checklist
- [ ] Code follows project style guidelines
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

## 🎯 Feature Development Guidelines

### Adding New Endpoints

1. **Backend** (`backend/main.py`):
   ```python
   @app.post("/your-endpoint", response_model=YourResponse)
   async def your_endpoint(request: YourRequest):
       """Clear docstring"""
       try:
           # Implementation
           return YourResponse(data=result)
       except Exception as e:
           raise HTTPException(status_code=500, detail=str(e))
   ```

2. **Frontend** (`frontend/app.py`):
   ```python
   def call_your_endpoint(data):
       """Call your new endpoint"""
       with st.spinner("Processing..."):
           # API call or direct Claude call
           result = # your logic
           return result
   ```

3. **Update UI**: Add button/form to trigger the feature

### Modifying Prompts

Prompts are critical to output quality. When modifying:

1. **Test thoroughly** with various inputs
2. **Document changes** in commit message
3. **Preserve format** requirements (bullet points, tables, etc.)
4. **Consider edge cases** (very short/long inputs)

### Adding UI Components

1. **Mobile-first**: Design for mobile, enhance for desktop
2. **Consistent styling**: Use existing CSS classes
3. **Accessibility**: Use proper labels and alt text
4. **Loading states**: Add spinners for async operations
5. **Error feedback**: Clear error messages

## 📚 Documentation

When updating documentation:

- **README.md**: User-facing documentation
- **DEPLOYMENT.md**: Deployment instructions
- **CONTRIBUTING.md**: This file
- **Code comments**: For complex logic
- **Docstrings**: For functions and classes

## 🔒 Security

- **Never commit** API keys or secrets
- **Validate input** on both frontend and backend
- **Sanitize output** to prevent XSS
- **Use environment variables** for configuration
- **Report security issues** privately to maintainers

## 🤝 Code Review Process

All submissions require review. Reviewers will check:

- Code quality and style
- Functionality and testing
- Documentation
- Security considerations
- Performance impact

Be responsive to feedback and make requested changes promptly.

## 🎉 Recognition

Contributors will be:
- Mentioned in release notes
- Added to contributors list
- Credited in documentation

## 📞 Getting Help

If you need help:

1. Check existing documentation
2. Search existing issues
3. Ask in discussions
4. Reach out to maintainers

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Idea Factory! 🎉
