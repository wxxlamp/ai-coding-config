#!/bin/bash
input=$(cat)
cmd=$(echo "$input" | jq -r '.tool_input.command')

# Check if this is a git commit command
if [[ "$cmd" =~ ^git\ commit ]]; then
  # Use Claude non-interactively to regenerate README
  claude -p "Analyze this project and regenerate README.md with current features, usage, and installation instructions" --output-format json > /dev/null 2>&1
fi

# Allow the original command to proceed
echo "{}"