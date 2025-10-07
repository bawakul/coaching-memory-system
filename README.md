# Life Coaching Memory System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.7%2B-blue)
![Claude Code](https://img.shields.io/badge/Claude%20Code-required-orange)

A local system for tracking and storing your life coaching conversations with Claude, giving Claude persistent memory across sessions.

## ✨ Features

- 🧠 **Persistent Memory** - Claude remembers your previous conversations
- 🔍 **Searchable Archive** - Find past sessions by keyword, tag, or date
- 📊 **Progress Tracking** - Analyze patterns and themes over time
- 🔒 **Privacy First** - All data stored locally on your machine
- ⚡ **Automatic** - Hooks handle memory loading and saving seamlessly

## Overview

This system uses **Claude Code hooks** to automatically:
- Load relevant memories at the start of each session
- Save conversations at the end of each session
- Maintain continuity across coaching sessions

## How It Works

### Automatic Memory (Hooks)

**When you start a session:**
1. The `SessionStart` hook runs automatically
2. Recent coaching sessions are loaded into `.claude/claude.md`
3. Claude reads this context and "remembers" your previous conversations

**When you end a session:**
1. The `SessionEnd` hook prompts you to save the conversation
2. You provide: topic, insights, and tags
3. Session is saved to `coaching-sessions/sessions/`
4. Index is updated for future searching

### Manual Tools

**Search Sessions:**
```bash
python3 search-sessions.py                    # Interactive search
python3 search-sessions.py --keyword "goals"  # Search by keyword
python3 search-sessions.py --tag "career"     # Search by tag
python3 search-sessions.py --date 2025-10-07  # Search by date
python3 search-sessions.py --tags             # List all tags
python3 search-sessions.py --all              # Show all sessions
```

**Summarize Progress:**
```bash
python3 summarize-progress.py        # Quick stats
python3 summarize-progress.py --full # Full summary report
```

**Manual Save (if you skipped the hook):**
```bash
python3 .claude/hooks/save-session.py
```

## Directory Structure

```
.
├── .claude/
│   ├── claude.md                    # Context file (auto-updated)
│   ├── config.json                  # Hooks configuration
│   └── hooks/
│       ├── session-start.sh         # Loads memories on start
│       ├── session-end.sh           # Saves session on end
│       ├── load-memory.py           # Updates claude.md
│       └── save-session.py          # Saves conversations
│
├── coaching-sessions/
│   ├── sessions/                    # Individual session files
│   │   └── YYYY-MM-DD-topic.md
│   ├── index.json                   # Searchable index
│   └── memory-summary.md            # Generated summaries
│
├── search-sessions.py               # Search tool
├── summarize-progress.py            # Summary tool
└── README.md                        # This file
```

## Getting Started

### Prerequisites

- **Claude Code CLI** - [Installation instructions](https://docs.claude.com/en/docs/claude-code/installation)
- **Python 3** - Typically pre-installed on macOS/Linux, download from [python.org](https://www.python.org/downloads/) for Windows
- **Git** - For cloning the repository

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/bawakul/coaching-memory-system.git
   cd coaching-memory-system
   ```

2. **Test the system (optional):**
   ```bash
   ./test-system.sh
   ```
   This creates a sample session and verifies everything works.

3. **Start using it:**
   ```bash
   claude
   ```

That's it! No dependencies to install, no configuration needed.

### Using the System

1. **Start a coaching session** (in this directory):
   ```bash
   claude
   ```
   Claude will automatically load memories from previous sessions.

2. **Have your conversation** with Claude as your coach.

3. **End the session** (Ctrl+D or exit):
   The hook will prompt you to save:
   - Session topic
   - Conversation content
   - Key insights
   - Tags (e.g., "career", "relationships", "goals")

4. **Search your history** anytime:
   ```bash
   python3 search-sessions.py
   ```

5. **Review your progress** periodically:
   ```bash
   python3 summarize-progress.py --full
   ```

## Features

### Automatic Memory
- Claude remembers your journey, goals, and progress
- Recent sessions are automatically loaded
- Maintains coaching continuity

### Searchable Archive
- Find sessions by keyword, tag, or date
- Track recurring themes
- Review past insights

### Progress Tracking
- Analyze patterns over time
- Identify top themes
- Monitor monthly activity
- Generate reflection prompts

## Tips

- **Be consistent with tags**: Use the same tags for related topics (e.g., "career", "work-life-balance")
- **Capture insights**: Take a moment to write meaningful insights after each session
- **Review regularly**: Use `summarize-progress.py` monthly to reflect on patterns
- **Search before sessions**: Use `search-sessions.py` to review relevant past conversations

## Privacy

All data is stored **locally** on your machine:
- No cloud storage
- No external services
- Plain text markdown files
- You have complete control

## Customization

### Modify Context Loading
Edit `.claude/hooks/load-memory.py` to change:
- Number of recent sessions loaded
- How context is formatted
- What information is included

### Adjust Hooks
Edit `.claude/config.json` to:
- Enable/disable automatic saving
- Add additional hooks
- Customize hook behavior

### Session Format
Sessions are stored as markdown in `coaching-sessions/sessions/`
Feel free to edit them directly if needed.

## Troubleshooting

**Hooks not running?**
- Make sure you're running Claude Code in this directory
- Check that hook scripts are executable: `chmod +x .claude/hooks/*.sh .claude/hooks/*.py`

**Can't find old sessions?**
- Check `coaching-sessions/index.json` for session list
- Use `search-sessions.py --all` to see everything

**Want to disable hooks temporarily?**
- Rename `.claude/config.json` to disable all hooks
- Rename it back to re-enable

## Learn More

- [Claude Code Hooks Documentation](https://docs.claude.com/en/docs/claude-code/hooks)
- [Claude Code Custom Commands](https://docs.claude.com/en/docs/claude-code/commands)

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Built with [Claude Code](https://claude.com/claude-code) - AI-powered coding assistant.

---

**Ready to start?** Just run `claude` in this directory and begin your first coaching session!
