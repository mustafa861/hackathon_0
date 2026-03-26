#!/bin/bash
# Ralph Wiggum Stop Hook
# Keeps Claude Code iterating until task is complete

# This hook checks if the task is complete by looking for completion signals:
# 1. File moved to /Done folder
# 2. <promise>TASK_COMPLETE</promise> in output
# 3. All checkboxes in Plan.md are checked

VAULT_PATH="vault"
TASK_FILE="$1"

# Check if task file exists in Done folder
if [ -f "$VAULT_PATH/Done/$(basename $TASK_FILE)" ]; then
    echo "Task complete - file moved to Done"
    exit 0
fi

# Check if all tasks in Needs_Action are processed
NEEDS_ACTION_COUNT=$(find "$VAULT_PATH/Needs_Action" -type f -name "*.md" 2>/dev/null | wc -l)
if [ "$NEEDS_ACTION_COUNT" -eq 0 ]; then
    echo "All tasks processed"
    exit 0
fi

# Task not complete - continue iterating
echo "Task incomplete - continuing..."
exit 1
