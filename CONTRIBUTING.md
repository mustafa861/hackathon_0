# Contributing to Personal AI Employee

Thank you for your interest in contributing to the Personal AI Employee project! This document provides guidelines for contributing.

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs
- Include detailed reproduction steps
- Provide system information (OS, Python version)
- Include relevant log files from `vault/Logs/`

### Suggesting Features
- Open a GitHub Issue with the "enhancement" label
- Describe the use case and benefits
- Explain how it fits into the architecture
- Consider security implications

### Submitting Code

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/hackathon_0.git
   cd hackathon_0
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the code style (PEP 8 for Python)
   - Add comments for complex logic
   - Update documentation if needed
   - Add tests for new features

4. **Test your changes**
   ```bash
   # Run test suite
   python tests/test_system.py

   # Test with dry-run mode
   export DRY_RUN=true
   python src/orchestrator.py vault/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description of your feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**
   - Describe what your PR does
   - Reference any related issues
   - Include screenshots/demos if applicable

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use docstrings for classes and functions

Example:
```python
def process_email(email_id: str, vault_path: Path) -> dict:
    """
    Process an email and create action file.

    Args:
        email_id: Gmail message ID
        vault_path: Path to Obsidian vault

    Returns:
        dict: Processing result with status and file path
    """
    pass
```

### Markdown
- Use clear headings
- Include code examples
- Keep lines under 100 characters
- Use tables for structured data

## Project Structure

### Adding a New Watcher
1. Create file in `src/watchers/`
2. Inherit from `BaseWatcher`
3. Implement `check_for_updates()` and `create_action_file()`
4. Add to `ecosystem.config.js`
5. Update documentation

Example:
```python
from base_watcher import BaseWatcher

class CustomWatcher(BaseWatcher):
    def __init__(self, vault_path: str):
        super().__init__(vault_path, check_interval=60)

    def check_for_updates(self) -> list:
        # Your implementation
        pass

    def create_action_file(self, item) -> Path:
        # Your implementation
        pass
```

### Adding a New MCP Server
1. Create file in `src/mcp/`
2. Implement `handle_tool_call()` function
3. Add to `.claude/mcp.json`
4. Document available tools
5. Add tests

### Adding Tests
1. Create test file in `tests/`
2. Use unittest framework
3. Test both success and failure cases
4. Mock external APIs
5. Run tests before submitting PR

## Documentation

### Code Comments
- Explain WHY, not WHAT
- Document complex algorithms
- Note security considerations
- Include usage examples

### README Updates
- Update if adding new features
- Add setup instructions for new dependencies
- Update troubleshooting section
- Keep examples current

## Security Guidelines

### Never Commit
- Credentials or API keys
- `.env` files
- OAuth tokens
- Session data
- Personal information

### Always
- Use environment variables for secrets
- Implement approval gates for sensitive actions
- Log all actions comprehensively
- Test with dry-run mode first
- Consider rate limiting

## Testing

### Manual Testing
1. Initialize fresh vault
2. Test each watcher individually
3. Test orchestrator coordination
4. Test approval workflow
5. Verify logging

### Automated Testing
```bash
# Run all tests
python tests/test_system.py

# Run specific test
python -m unittest tests.test_system.TestWatchers
```

## Release Process

### Version Numbers
- Follow Semantic Versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Creating a Release
1. Update version in relevant files
2. Update CHANGELOG.md
3. Create git tag
4. Push to GitHub
5. Create release notes

## Community

### Communication
- GitHub Issues for bugs and features
- GitHub Discussions for questions
- Pull Requests for code contributions

### Code of Conduct
- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Focus on the project goals

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## Questions?

- Open a GitHub Issue
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Personal AI Employee! 🤖
