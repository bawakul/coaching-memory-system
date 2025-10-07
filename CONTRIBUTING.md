# Contributing to Coaching Memory System

Thanks for your interest in contributing! This project is meant to help people maintain continuity in their coaching conversations with Claude.

## How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/bawakul/coaching-memory-system/issues/new?template=bug_report.md) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Claude Code version)

### Suggesting Features

Have an idea for improvement? [Open a feature request](https://github.com/bawakul/coaching-memory-system/issues/new?template=feature_request.md) with:
- Description of the feature
- Use case (why it would be helpful)
- Any implementation ideas you have

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Test your changes**: Run `./test-system.sh` to verify everything works
5. **Commit with clear messages**: Follow the existing commit style
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Open a Pull Request**

### Development Guidelines

**Code Style:**
- Python: Follow PEP 8 style guidelines
- Bash: Use clear variable names and comments
- Keep scripts simple and readable

**Testing:**
- Test your changes with `./test-system.sh`
- Manually test hooks by starting/ending Claude sessions
- Verify search and summarize tools work correctly

**Documentation:**
- Update README.md if you add features
- Add comments for complex logic
- Include usage examples

### Areas for Contribution

Some ideas if you're looking for where to help:

- **Better error handling**: Improve error messages and recovery
- **Additional export formats**: CSV, JSON, or other formats for sessions
- **Tag management**: Auto-suggest tags, merge similar tags
- **Search improvements**: Fuzzy search, better ranking
- **Visualization**: Charts for progress over time
- **Integration**: Export to journaling apps, notion, etc.
- **Multi-language support**: Internationalization
- **Documentation**: Tutorials, videos, use case examples

### Questions?

Open a [discussion](https://github.com/bawakul/coaching-memory-system/discussions) or reach out via issues.

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on what's best for the community
- Show empathy toward others

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
