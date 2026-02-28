#!/usr/bin/env node

const fs = require("fs");
const path = require("path");

const SKILL_NAME = "drawio-swimlane-flowchart";

function printUsage() {
  console.log(`
Usage: npx drawio-swimlane-flowchart [options]

Install the draw.io swimlane flowchart skill for Claude Code.

Options:
  --global, -g     Install to ~/.claude/skills/ (user-level, all projects)
  --project, -p    Install to ./.claude/skills/ (project-level, current dir)
  --uninstall      Remove the installed skill
  --help, -h       Show this help message

Examples:
  npx drawio-swimlane-flowchart --global
  npx drawio-swimlane-flowchart --project
  npx drawio-swimlane-flowchart --uninstall --global
`);
}

function getTargetDir(isGlobal) {
  if (isGlobal) {
    const home =
      process.env.HOME ||
      process.env.USERPROFILE ||
      path.join(process.env.HOMEDRIVE || "C:", process.env.HOMEPATH || "\\");
    return path.join(home, ".claude", "skills", SKILL_NAME);
  }
  return path.join(process.cwd(), ".claude", "skills", SKILL_NAME);
}

function copyRecursive(src, dest) {
  if (!fs.existsSync(src)) {
    console.error(`Source not found: ${src}`);
    process.exit(1);
  }

  const stat = fs.statSync(src);
  if (stat.isDirectory()) {
    fs.mkdirSync(dest, { recursive: true });
    const entries = fs.readdirSync(src);
    for (const entry of entries) {
      copyRecursive(path.join(src, entry), path.join(dest, entry));
    }
  } else {
    fs.mkdirSync(path.dirname(dest), { recursive: true });
    fs.copyFileSync(src, dest);
  }
}

function removeRecursive(dir) {
  if (fs.existsSync(dir)) {
    fs.rmSync(dir, { recursive: true, force: true });
    return true;
  }
  return false;
}

function install(isGlobal) {
  const targetDir = getTargetDir(isGlobal);
  const skillSrc = path.join(__dirname, "..", "skill");

  if (!fs.existsSync(skillSrc)) {
    console.error("Error: skill directory not found in package.");
    process.exit(1);
  }

  console.log(`Installing ${SKILL_NAME}...`);
  console.log(`  Target: ${targetDir}`);

  copyRecursive(skillSrc, targetDir);

  const scope = isGlobal ? "user-level (all projects)" : "project-level";
  console.log(`\nInstalled successfully! (${scope})`);
  console.log(`  Location: ${targetDir}`);
  console.log(`\nThe skill is now available in Claude Code.`);
  console.log(
    `Trigger: "flowchart", "swimlane", "draw.io", "business flow" etc.`
  );
}

function uninstall(isGlobal) {
  const targetDir = getTargetDir(isGlobal);

  if (removeRecursive(targetDir)) {
    console.log(`Uninstalled ${SKILL_NAME} from ${targetDir}`);
  } else {
    console.log(`${SKILL_NAME} not found at ${targetDir}`);
  }
}

function main() {
  const args = process.argv.slice(2);

  if (args.includes("--help") || args.includes("-h")) {
    printUsage();
    process.exit(0);
  }

  const isGlobal = args.includes("--global") || args.includes("-g");
  const isProject = args.includes("--project") || args.includes("-p");
  const isUninstall = args.includes("--uninstall");

  if (!isGlobal && !isProject) {
    console.log("Please specify installation scope:\n");
    console.log("  --global, -g     Install for all projects (~/.claude/skills/)");
    console.log("  --project, -p    Install for current project (./.claude/skills/)");
    console.log("\nExample: npx drawio-swimlane-flowchart --global");
    process.exit(1);
  }

  if (isGlobal && isProject) {
    console.error("Error: Cannot specify both --global and --project.");
    process.exit(1);
  }

  if (isUninstall) {
    uninstall(isGlobal);
  } else {
    install(isGlobal);
  }
}

main();
