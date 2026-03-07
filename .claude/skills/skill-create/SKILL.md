---
name: skill-create
description: Create a new Claude Code skill with proper directory structure. Use when you need to add reusable automation to your workflow or create scripts and references.
---

# Skill Create

Create a new Claude Code skill, script, or reference file with proper structure and validation.

## Usage

```
skill: "skill-create", args: "<name> [<description>]"
```

## Arguments

- `name` (required): Name of the item to create. Use lowercase letters, numbers, hyphens.
- `description` (optional): Brief description of what this item does.

## Examples

```
skill: "skill-create", args: "commit Generate conventional commit message"
skill: "skill-create", args: "deploy Deploy to production environment"
skill: "skill-create", args: "test-runner Run project tests"
```

---

When invoked, follow these steps:

1. **Parse arguments**: Split args string to extract `name` and optional `description`.
   - If no args provided, prompt: "What name for the skill/script/reference?"
   - If description not provided, prompt: "What does this do? (brief description)"

2. **Validate name**: Check it follows conventions:
   - Lowercase letters, numbers, hyphens only
   - No spaces or special characters
   - Starts with a letter
   - Examples: `commit`, `pr-create`, `test-runner`
   - If invalid, explain rules and ask for a new name

3. **Determine file type**: Ask user to select type:
   - **skill** (default): A reusable Claude Code skill
   - **script**: An executable script
   - **reference**: A reference document or knowledge base

4. **Gather details** based on selected type:

   ### For Skill:
   - **Usage pattern**: Example invocation with args
   - **Arguments list**: Parameters the skill accepts (name, required/optional, description)
   - **Behavior**: What Claude should do when this skill is invoked (step by step)
   - **When to use**: Context for when this skill is most helpful

   ### For Script:
   - **Language**: Shell (bash/zsh), Python, Node.js, Ruby, etc.
   - **Parameters**: Command-line arguments the script accepts
   - **Functionality**: Step-by-step description of what the script does
   - **Make executable**: Whether to chmod +x (default: yes)

   ### For Reference:
   - **Topic area**: What domain this reference covers
   - **Key sections**: Main sections to include
   - **Code examples**: Whether to include example code

5. **Generate file preview** based on type:

   ### Skill Template (Official Format):
   Save to: `.claude/skills/{name}/SKILL.md`

   ```markdown
   ---
   name: {skill-name}
   description: {When to use this skill. Use when you need to...}
   ---

   # {Title}

   {Longer description of what this skill does}

   ## Usage

   ```
   skill: "{name}", args: "{example-args}"
   ```

   ## Arguments

   - `{arg1}` ({required/optional}): {description}
   - `{arg2}` ({required/optional}): {description}

   ---

   When invoked, {describe what Claude should do}:

   1. {First step}
   2. {Second step}
   3. {Third step}
   ```

   ### Script Template:
   Save to: `.claude/skills/{name}/{script-name}.{ext}`

   ```bash
   #!/usr/bin/env {interpreter}
   #
   # {name} - {description}
   #
   # Usage: {usage example}
   #

   {script content based on functionality description}
   ```

   ### Reference Template:
   Save to: `.claude/skills/{name}/REFERENCE.md`

   ```markdown
   ---
   name: {reference-name}
   description: {Brief description of what this reference covers}
   ---

   # {Title}

   {Description}

   ## Overview

   {overview content}

   ## {Section 1}

   {section content}

   ## Examples

   ```{language}
   {code example}
   ```
   ```

6. **Show preview and confirm**: Display the generated content and ask:
   - "Save this file to `{filepath}`?"
   - "Edit before saving?" (allow user to modify)
   - "Cancel?" (abort)

7. **Save the file** to appropriate location:
   - Skills: `.claude/skills/{name}/SKILL.md`
   - Scripts: `.claude/skills/{name}/{script-name}.{ext}`
   - References: `.claude/skills/{name}/REFERENCE.md`

   Create parent directories if needed using `mkdir -p`.

8. **Set permissions**: If script type and user requested, run `chmod +x` on the file.

9. **Confirm success**: Report:
   - File created at `{filepath}`
   - How to use it (e.g., `skill: "{name}"` or run the script)
   - Suggestion to test it

10. **Validate structure (optional but recommended)**: run the bundled Python verifier:
    ```bash
    python3 .claude/skills/skill-create/validate_skill.py {name}
    ```
    The script will walk the new directory and ensure frontmatter, naming,
    and executable bits all conform to the conventions laid out below.  Fix any
    warnings or errors before committing the new skill.

---

## Guidelines for Creating Skills

### Official Skill Directory Structure

```
.claude/skills/
├── skill-create/
│   └── SKILL.md
├── commit/
│   └── SKILL.md
└── deploy/
    ├── SKILL.md
    └── deploy.sh
```

### Official Skill Format Structure

Every skill file must follow this exact structure:

```markdown
---
name: skill-name
description: Clear description of what this does. Use when you need to...
---

# Title

## Usage

```
skill: "name", args: "args"
```

## Arguments

- `arg` (required/optional): Description

---

When invoked, action:

1. Step one
2. Step two
```

### Key Principles

- **Directory per skill**: Each skill gets its own directory under `.claude/skills/`
- **SKILL.md**: The main skill file must be named `SKILL.md` (uppercase)
- **YAML Frontmatter Required**: Must include `name` and `description` fields between `---` markers
- **description format**: End with "Use when you need to..." pattern for clarity
- **Single responsibility**: Each skill does one thing well
- **Clear steps**: Numbered steps telling Claude exactly what to do
- **Examples matter**: Always include usage examples

### Naming Conventions

- Use lowercase with hyphens for directory names: `pr-create/`, not `prCreate/`
- Use action-oriented names: `commit/`, `test-run/`, `deploy-prod/`
- Main file always named `SKILL.md` (uppercase)
- Additional files (scripts, references) can be in the same directory

### Built‑in Validation Script

A helper script lives alongside this skill and can be run after creation to
check that the new item satisfies the structural rules described throughout
this document.  It is written in Python and has no external dependencies.  To
execute it:

```bash
chmod +x .claude/skills/skill-create/validate_skill.py  # one-time only
python3 .claude/skills/skill-create/validate_skill.py <skill-name>
```

The validator ensures the following:

1. The directory exists under `.claude/skills/`.
2. There is either a `SKILL.md` or `REFERENCE.md` file with a YAML
   frontmatter block containing a `name:` field that matches the directory
   name.
3. Any supplementary script files are executable and start with a shebang.
4. No other stray files are present.

Errors cause a non‑zero exit code; warnings are printed but not fatal.  Use the
output to correct problems before committing.

### File Locations

| Type | Location |
|------|----------|
| Skills | `.claude/skills/{name}/SKILL.md` |
| Scripts | `.claude/skills/{name}/{script-name}.{ext}` |
| References | `.claude/skills/{name}/REFERENCE.md` |
