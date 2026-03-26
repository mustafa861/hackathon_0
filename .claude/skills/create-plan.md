---
name: create-plan
description: Create a Plan.md file for multi-step tasks with reasoning and action items
---

# Create Plan Skill

This skill creates structured Plan.md files for complex tasks that require multiple steps.

## Usage

When a complex task is detected, this skill:
1. Analyzes the task requirements
2. Breaks down into actionable steps
3. Creates a Plan.md file with checkboxes
4. Saves to vault/Plans/ folder

## Example

```bash
claude create-plan "Process client invoice and send payment reminder"
```

## Plan Structure

```markdown
# Plan: [Task Name]

## Context
[Background information]

## Steps
- [ ] Step 1: Description
- [ ] Step 2: Description
- [ ] Step 3: Description

## Expected Outcome
[What success looks like]

## Notes
[Additional considerations]
```

## Implementation

The orchestrator uses this skill when processing complex requests from Needs_Action folder.
