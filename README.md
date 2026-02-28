# drawio-swimlane-flowchart

Claude Code skill for generating draw.io swimlane (cross-functional) business process flowcharts.

## Install

### From GitHub (private repo)

```bash
# User-level (all projects)
npx github:tmiyakawa-tsp/drawio-swimlane-flowchart --global

# Project-level (current project only)
npx github:tmiyakawa-tsp/drawio-swimlane-flowchart --project
```

### Uninstall

```bash
npx github:tmiyakawa-tsp/drawio-swimlane-flowchart --uninstall --global
npx github:tmiyakawa-tsp/drawio-swimlane-flowchart --uninstall --project
```

## Usage

Once installed, the skill is automatically available in Claude Code. Trigger it by saying:

- "フローチャートを作って"
- "業務フローを作成して"
- "swimlane図を作って"
- ".drawioファイルを作成して"

## What it does

- Generates vertical swimlane flowcharts in draw.io XML format
- Supports multiple lanes (departments/roles) with color coding
- Includes process nodes, decision diamonds, start/end nodes, and sticky notes
- Analyzes meeting notes or text descriptions to extract workflow structure (Phase 1)
- Produces ready-to-use `.drawio` files (Phase 2)

## Skill Contents

- `skill/SKILL.md` - Main skill definition and instructions
- `skill/references/xml-structure.md` - XML structure specification for draw.io format
- `skill/assets/example_swimlane.drawio` - Example output file
