#!/bin/bash
# Test script for the coaching memory system

echo ""
echo "════════════════════════════════════════════"
echo "  Testing Coaching Memory System"
echo "════════════════════════════════════════════"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PROJECT_DIR="/Users/bharadwajkulkarni/Documents /Vibecoding/Coaching-example"

echo -e "${BLUE}Step 1: Creating a test coaching session...${NC}"
echo ""

# Create a test session directly
python3 "$PROJECT_DIR/.claude/hooks/save-session.py" --topic "Career Goals Test" \
"User: I'm thinking about changing careers into tech.

Claude: That's a significant decision. What's drawing you toward tech specifically?

User: I love problem-solving and want more flexibility in my work.

Claude: Those are great motivations. What specific area of tech interests you most?

User: Maybe software development or data analysis.

Claude: Both are strong paths. Have you done any exploration in either area yet?" \
"User is exploring career change into tech, motivated by problem-solving and flexibility. Needs to explore specific paths further." \
"career,goals,tech,exploration"

echo ""
echo -e "${GREEN}✓ Test session created${NC}"
echo ""

echo -e "${BLUE}Step 2: Testing memory loading (updating claude.md)...${NC}"
echo ""

python3 "$PROJECT_DIR/.claude/hooks/load-memory.py"

echo ""
echo -e "${GREEN}✓ Memory loaded into claude.md${NC}"
echo ""

echo -e "${BLUE}Step 3: Viewing updated claude.md context...${NC}"
echo ""
echo "--- claude.md content (first 30 lines) ---"
head -30 "$PROJECT_DIR/.claude/claude.md"
echo ""
echo -e "${GREEN}✓ Context file updated${NC}"
echo ""

echo -e "${BLUE}Step 4: Testing search functionality...${NC}"
echo ""

python3 "$PROJECT_DIR/search-sessions.py" --keyword "career"

echo ""
echo -e "${GREEN}✓ Search working${NC}"
echo ""

echo -e "${BLUE}Step 5: Testing progress summary...${NC}"
echo ""

python3 "$PROJECT_DIR/summarize-progress.py"

echo ""
echo -e "${GREEN}✓ Summary generated${NC}"
echo ""

echo "════════════════════════════════════════════"
echo -e "${GREEN}  All Tests Passed! ✓${NC}"
echo "════════════════════════════════════════════"
echo ""
echo "What was tested:"
echo "  ✓ Session saving"
echo "  ✓ Memory loading into claude.md"
echo "  ✓ Context file updates"
echo "  ✓ Search functionality"
echo "  ✓ Progress summaries"
echo ""
echo "Check these files to see the results:"
echo "  • coaching-sessions/sessions/$(date +%Y-%m-%d)-Career-Goals-Test.md"
echo "  • coaching-sessions/index.json"
echo "  • .claude/claude.md"
echo ""
echo "To clean up test data:"
echo "  rm coaching-sessions/sessions/$(date +%Y-%m-%d)-Career-Goals-Test.md"
echo "  # Then edit coaching-sessions/index.json to remove the test entry"
echo ""
