# 🤝 Contributing to Advanced SEO Crawler

Thank you for your interest in contributing to the Advanced SEO Crawler project! We welcome contributions from developers, SEO professionals, cybersecurity researchers, and anyone passionate about web automation and data analysis.

## 📋 Table of Contents

- [🎯 How to Contribute](#how-to-contribute)
- [🐛 Reporting Bugs](#reporting-bugs)
- [✨ Feature Requests](#feature-requests)
- [🔧 Development Setup](#development-setup)
- [📝 Code Style Guidelines](#code-style-guidelines)
- [🧪 Testing Requirements](#testing-requirements)
- [📚 Documentation Standards](#documentation-standards)
- [🔒 Security Considerations](#security-considerations)
- [📄 License Agreement](#license-agreement)

## 🎯 How to Contribute

### Types of Contributions Welcome

1. **🐛 Bug Fixes**: Fix issues in existing functionality
2. **✨ New Features**: Add new crawling capabilities or logging features
3. **📝 Documentation**: Improve or expand documentation
4. **🧪 Tests**: Add or improve test coverage
5. **🔧 Performance**: Optimize existing code for better performance
6. **🌐 Proxy Sources**: Add new proxy providers or regions
7. **🤖 AI Integration**: Enhance AI/ML capabilities
8. **🔍 SEO Tools**: Improve SEO analysis features

### Contribution Process

1. **Fork the Repository**
   ```bash
   git clone https://github.com/your-username/seo-crawler-tor-ga.git
   cd seo-crawler-tor-ga
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/issue-description
   ```

3. **Make Your Changes**
   - Follow our code style guidelines
   - Add tests for new functionality
   - Update documentation as needed

4. **Test Your Changes**
   ```bash
   python -m pytest tests/
   python -m flake8 src/
   python -m black src/ --check
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new proxy rotation algorithm"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Use our PR template
   - Provide clear description of changes
   - Link any related issues

## 🐛 Reporting Bugs

### Before Reporting

1. **Search Existing Issues**: Check if the bug has already been reported
2. **Test with Latest Version**: Ensure you're using the most recent code
3. **Minimal Reproduction**: Create the smallest possible example that demonstrates the bug

### Bug Report Template

```markdown
## Bug Description
Brief description of the issue

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., macOS 14.0, Ubuntu 22.04]
- Python Version: [e.g., 3.9.7]
- Browser: [e.g., Chrome 119.0]
- Tor Version: [if applicable]

## Additional Context
Any other relevant information, logs, or screenshots
```

## ✨ Feature Requests

### Feature Request Guidelines

1. **Check Existing Requests**: Search for similar feature requests
2. **Clear Use Case**: Explain why this feature would be valuable
3. **Implementation Ideas**: Suggest how it might work (optional)
4. **Breaking Changes**: Note if this would require breaking changes

### Feature Request Template

```markdown
## Feature Description
Clear description of the proposed feature

## Use Case
Explain the problem this feature would solve

## Proposed Solution
How you envision this feature working

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other relevant information
```

## 🔧 Development Setup

### Prerequisites

- **Python 3.8+**
- **Git**
- **Chrome/Chromium Browser**
- **Tor Browser** (for testing Tor features)

### Environment Setup

1. **Clone and Setup**
   ```bash
   git clone https://github.com/jedixcom/seo-crawler-tor-ga.git
   cd seo-crawler-tor-ga
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv dev-env
   source dev-env/bin/activate  # On Windows: dev-env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Setup Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Run Initial Tests**
   ```bash
   python -m pytest tests/ -v
   ```

### Development Dependencies

```txt
# Testing
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-mock>=3.10.0

# Code Quality
black>=23.0.0
flake8>=6.0.0
isort>=5.12.0
mypy>=1.0.0

# Pre-commit Hooks
pre-commit>=3.0.0

# Documentation
sphinx>=6.0.0
sphinx-rtd-theme>=1.2.0
```

## 📝 Code Style Guidelines

### Python Style

We follow **PEP 8** with some specific preferences:

```python
# Good: Clear, descriptive names
def extract_seo_metadata(html_content: str) -> Dict[str, Any]:
    """Extract SEO metadata from HTML content."""
    metadata = {}
    
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', html_content)
    if title_match:
        metadata['title'] = title_match.group(1).strip()
    
    return metadata

# Good: Type hints and docstrings
class ProxyRotator:
    """Manages proxy rotation with health monitoring."""
    
    def __init__(self, proxy_list: List[str]) -> None:
        self.proxies = proxy_list
        self.current_index = 0
    
    def get_next_proxy(self) -> Optional[str]:
        """Get the next available proxy."""
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        return proxy
```

### Code Formatting

- **Line Length**: Maximum 88 characters (Black default)
- **Imports**: Use `isort` for import organization
- **Type Hints**: Required for all public functions and methods
- **Docstrings**: Use Google-style docstrings

### Naming Conventions

```python
# Variables and functions: snake_case
user_agent = "Mozilla/5.0 ..."
def parse_robots_txt(content: str) -> Dict[str, List[str]]:

# Classes: PascalCase
class TorBrowserManager:
class GoogleAnalyticsTracker:

# Constants: UPPER_SNAKE_CASE
DEFAULT_TIMEOUT = 30
MAX_RETRY_ATTEMPTS = 3

# Private methods: _leading_underscore
def _validate_proxy_format(self, proxy: str) -> bool:
```

## 🧪 Testing Requirements

### Test Structure

```
tests/
├── unit/                   # Unit tests
│   ├── test_proxy_manager.py
│   ├── test_tor_browser.py
│   └── test_logging_system.py
├── integration/            # Integration tests
│   ├── test_full_workflow.py
│   └── test_database_integration.py
├── fixtures/              # Test data
│   ├── sample_html.html
│   └── proxy_list.txt
└── conftest.py            # Pytest configuration
```

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from your_module import ProxyManager

class TestProxyManager:
    """Test suite for ProxyManager class."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.proxy_list = ["proxy1:8080", "proxy2:8080"]
        self.manager = ProxyManager(self.proxy_list)
    
    def test_get_next_proxy_rotation(self):
        """Test that proxies are rotated correctly."""
        # Test first proxy
        assert self.manager.get_next_proxy() == "proxy1:8080"
        
        # Test second proxy
        assert self.manager.get_next_proxy() == "proxy2:8080"
        
        # Test rotation back to first
        assert self.manager.get_next_proxy() == "proxy1:8080"
    
    @patch('requests.get')
    def test_proxy_health_check(self, mock_get):
        """Test proxy health checking functionality."""
        mock_get.return_value.status_code = 200
        
        result = self.manager.check_proxy_health("proxy1:8080")
        assert result is True
        
        mock_get.assert_called_once()
```

### Test Coverage

- **Minimum Coverage**: 80% for new code
- **Critical Paths**: 95% coverage for core functionality
- **Run Coverage**: `pytest --cov=src tests/`

## 📚 Documentation Standards

### Code Documentation

```python
def crawl_website(url: str, proxy: Optional[str] = None, 
                 stealth_mode: bool = True) -> CrawlResult:
    """Crawl a website with optional proxy and stealth mode.
    
    Args:
        url: The URL to crawl
        proxy: Optional proxy in format "host:port"
        stealth_mode: Whether to use anti-detection measures
        
    Returns:
        CrawlResult object containing scraped data and metadata
        
    Raises:
        CrawlError: If the website cannot be accessed
        ProxyError: If proxy connection fails
        
    Example:
        >>> crawler = WebCrawler()
        >>> result = crawler.crawl_website("https://example.com")
        >>> print(result.title)
        "Example Domain"
    """
```

### README Updates

When adding new features, update:

1. **Feature List**: Add to the main features section
2. **Usage Examples**: Provide code examples
3. **Installation**: Update if new dependencies are required
4. **Configuration**: Document new configuration options

### API Documentation

- Use **Sphinx** for API documentation
- Generate docs: `sphinx-build -b html docs/ docs/_build/`
- Host on GitHub Pages or ReadTheDocs

## 🔒 Security Considerations

### Security Guidelines

1. **No Hardcoded Secrets**: Use environment variables
2. **Input Validation**: Sanitize all user inputs
3. **Safe Defaults**: Choose secure default configurations
4. **Error Handling**: Don't expose sensitive information in errors
5. **Dependencies**: Keep dependencies updated

### Reporting Security Issues

**Do NOT create public issues for security vulnerabilities.**

Instead:
1. Email: security@jedix.com
2. Include detailed description
3. Provide steps to reproduce
4. Suggest fixes if possible

We will:
- Acknowledge within 48 hours
- Provide timeline for fixes
- Credit you in security advisories (if desired)

## 📄 License Agreement

By contributing to this project, you agree that:

1. **Your contributions** will be licensed under the MIT License
2. **You have the right** to submit the contribution
3. **You understand** the ethical usage requirements
4. **You will not submit** malicious or harmful code

### Contributor License Agreement

For significant contributions, we may ask you to sign a Contributor License Agreement (CLA) to ensure the project can be maintained and distributed effectively.

## 🎉 Recognition

### Contributors

All contributors will be:
- **Listed** in the CONTRIBUTORS.md file
- **Credited** in release notes for their contributions
- **Mentioned** in documentation for significant features
- **Invited** to join the core team (for substantial contributions)

### Types of Recognition

- 🥇 **Gold Contributors**: Major features or architectural improvements
- 🥈 **Silver Contributors**: Significant bug fixes or documentation
- 🥉 **Bronze Contributors**: Small fixes, typos, or minor improvements

## 🆘 Getting Help

### Community Support

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Email**: development@jedix.com for development questions
- **Discord**: Join our developer community (link in README)

### Development Questions

For development-specific questions:

1. **Check Documentation**: Review existing docs first
2. **Search Issues**: Look for similar questions
3. **Ask in Discussions**: Use GitHub Discussions for questions
4. **Be Specific**: Provide context and relevant code

## 🚀 Release Process

### Versioning

We use **Semantic Versioning** (SemVer):
- **MAJOR.MINOR.PATCH** (e.g., 2.1.3)
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

### Release Checklist

1. **Update Version**: Bump version numbers
2. **Update Changelog**: Document all changes
3. **Run Tests**: Ensure all tests pass
4. **Update Docs**: Refresh documentation
5. **Create Release**: Tag and create GitHub release
6. **Announce**: Share with community

---

Thank you for contributing to the Advanced SEO Crawler project! Your contributions help make web automation and SEO analysis more accessible to developers and professionals worldwide.

For questions about this contributing guide, please open an issue or contact us at development@jedix.com.
