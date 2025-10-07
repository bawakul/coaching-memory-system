#!/usr/bin/env python3
"""
Generate summaries and insights from coaching sessions.
Analyze patterns, progress, and themes over time.
"""

import json
from collections import Counter
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent
SESSIONS_DIR = PROJECT_ROOT / "coaching-sessions" / "sessions"
INDEX_FILE = PROJECT_ROOT / "coaching-sessions" / "index.json"
SUMMARY_FILE = PROJECT_ROOT / "coaching-sessions" / "memory-summary.md"


def load_index():
    """Load the session index."""
    if not INDEX_FILE.exists():
        print("❌ No sessions found. Index file does not exist.")
        return None
    return json.loads(INDEX_FILE.read_text())


def extract_insights_from_session(filepath):
    """Extract insights section from a session file."""
    if not filepath.exists():
        return ""

    content = filepath.read_text()
    lines = content.split("\n")

    insights = []
    in_insights = False
    for line in lines:
        if line.startswith("## Key Insights"):
            in_insights = True
            continue
        if in_insights and line.startswith("##"):
            break
        if in_insights and line.strip():
            insights.append(line)

    return "\n".join(insights).strip()


def analyze_sessions(sessions):
    """Analyze sessions for patterns and themes."""
    if not sessions:
        return None

    # Collect all tags
    all_tags = []
    for session in sessions:
        all_tags.extend(session.get("tags", []))

    tag_counts = Counter(all_tags)

    # Get date range
    dates = [datetime.fromisoformat(s["timestamp"]) for s in sessions]
    earliest = min(dates)
    latest = max(dates)

    # Group sessions by month
    monthly_counts = Counter()
    for date in dates:
        month_key = date.strftime("%Y-%m")
        monthly_counts[month_key] += 1

    return {
        "total_sessions": len(sessions),
        "date_range": (earliest, latest),
        "top_themes": tag_counts.most_common(10),
        "monthly_activity": monthly_counts,
        "recent_topics": [s["topic"] for s in sessions[:5]]
    }


def generate_summary():
    """Generate a comprehensive summary of all coaching sessions."""
    index_data = load_index()
    if not index_data:
        return

    sessions = index_data["sessions"]

    if not sessions:
        print("❌ No sessions to summarize.")
        return

    print("\n" + "=" * 80)
    print("  GENERATING COACHING PROGRESS SUMMARY")
    print("=" * 80 + "\n")

    analysis = analyze_sessions(sessions)

    # Build summary document
    summary_content = f"""# Coaching Progress Summary

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}
**Total Sessions:** {analysis['total_sessions']}
**Time Period:** {analysis['date_range'][0].strftime("%Y-%m-%d")} to {analysis['date_range'][1].strftime("%Y-%m-%d")}

---

## Top Themes & Topics

Based on tags across all sessions:

"""

    for theme, count in analysis['top_themes']:
        summary_content += f"- **{theme}** ({count} session{'s' if count != 1 else ''})\n"

    summary_content += "\n## Recent Topics\n\n"

    for i, topic in enumerate(analysis['recent_topics'], 1):
        summary_content += f"{i}. {topic}\n"

    summary_content += "\n## Monthly Activity\n\n"

    for month in sorted(analysis['monthly_activity'].keys(), reverse=True):
        count = analysis['monthly_activity'][month]
        summary_content += f"- **{month}:** {count} session{'s' if count != 1 else ''}\n"

    summary_content += "\n## Key Insights from Recent Sessions\n\n"

    for session in sessions[:5]:
        filepath = SESSIONS_DIR / session["filename"]
        insights = extract_insights_from_session(filepath)
        if insights and insights != "No specific insights recorded.":
            summary_content += f"### {session['date']} - {session['topic']}\n\n"
            summary_content += f"{insights}\n\n"

    summary_content += """---

## Reflection Questions

Based on your session history, consider:

1. What themes appear most frequently? What does this tell you?
2. Are you making progress on recurring topics?
3. What patterns do you notice in your challenges or breakthroughs?
4. Which areas might benefit from more attention?

---

*This summary is automatically generated from your coaching session history.*
*Update it anytime by running: python3 summarize-progress.py*
"""

    # Save summary to file
    SUMMARY_FILE.write_text(summary_content)

    # Print summary to console
    print(summary_content)

    print("\n" + "=" * 80)
    print(f"✅ Summary saved to: {SUMMARY_FILE}")
    print("=" * 80 + "\n")


def show_quick_stats():
    """Show quick statistics without generating full summary."""
    index_data = load_index()
    if not index_data:
        return

    sessions = index_data["sessions"]

    if not sessions:
        print("\n❌ No sessions recorded yet.\n")
        return

    analysis = analyze_sessions(sessions)

    print("\n" + "=" * 80)
    print("  COACHING SESSIONS - QUICK STATS")
    print("=" * 80)
    print(f"\n📊 Total Sessions: {analysis['total_sessions']}")
    print(f"📅 Time Period: {analysis['date_range'][0].strftime('%Y-%m-%d')} to {analysis['date_range'][1].strftime('%Y-%m-%d')}")
    print(f"\n🏷️  Top 5 Themes:")

    for theme, count in analysis['top_themes'][:5]:
        print(f"   • {theme} ({count})")

    print(f"\n📝 Recent Topics:")
    for i, topic in enumerate(analysis['recent_topics'], 1):
        print(f"   {i}. {topic}")

    print("\n" + "=" * 80)
    print("\nRun 'python3 summarize-progress.py --full' for complete summary")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--full":
        generate_summary()
    else:
        show_quick_stats()
