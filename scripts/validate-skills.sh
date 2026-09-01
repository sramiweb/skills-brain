#!/bin/bash
# Validate all SKILL.md files locally
# Usage: ./scripts/validate-skills.sh

set -e

echo "🔍 Validating SKILL.md files..."

ERRORS=0

for file in $(find . -name "SKILL.md" | sort); do
  echo "Checking $file"

  # Check required frontmatter fields
  if ! grep -q "^name:" "$file"; then
    echo "  ❌ Missing 'name' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^description:" "$file"; then
    echo "  ❌ Missing 'description' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^license:" "$file"; then
    echo "  ❌ Missing 'license' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^version:" "$file"; then
    echo "  ❌ Missing 'version' in frontmatter"
    ERRORS=$((ERRORS + 1))
  fi

  # Check required sections
  if ! grep -q "^## Purpose" "$file"; then
    echo "  ❌ Missing '## Purpose' section"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^## Workflow" "$file"; then
    echo "  ❌ Missing '## Workflow' section"
    ERRORS=$((ERRORS + 1))
  fi

  if ! grep -q "^## Examples" "$file"; then
    echo "  ❌ Missing '## Examples' section"
    ERRORS=$((ERRORS + 1))
  fi

  # Check YAML frontmatter delimiters
  if ! head -n 1 "$file" | grep -q "^---$"; then
    echo "  ❌ Invalid YAML frontmatter (missing opening ---)"
    ERRORS=$((ERRORS + 1))
  fi
done

if [ $ERRORS -eq 0 ]; then
  echo "✅ All SKILL.md files are valid!"
  exit 0
else
  echo ""
  echo "❌ Found $ERRORS error(s)"
  exit 1
fi
