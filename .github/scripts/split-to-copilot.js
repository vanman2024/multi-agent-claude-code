#!/usr/bin/env node

/**
 * Simple script to extract Copilot tasks from an issue and create sub-issues
 * Usage: node .github/scripts/split-to-copilot.js <issue-number>
 */

const { execSync } = require('child_process');

const issueNumber = process.argv[2];
if (!issueNumber) {
  console.error('Usage: node split-to-copilot.js <issue-number>');
  process.exit(1);
}

// Get issue body
const issueBody = execSync(`gh issue view ${issueNumber} --json body -q .body`).toString();

// Extract Copilot tasks
const copilotSection = issueBody.match(/## Copilot Tasks([\s\S]*?)(?=##|$)/);
if (!copilotSection) {
  console.log('No Copilot Tasks section found');
  process.exit(0);
}

const tasks = copilotSection[1].match(/- \[ \] (.+)/g);
if (!tasks) {
  console.log('No tasks found in Copilot Tasks section');
  process.exit(0);
}

// Create sub-issues for each task
tasks.forEach(task => {
  const taskDescription = task.replace('- [ ] ', '');
  
  const command = `gh issue create \
    --title "${taskDescription}" \
    --body "This is a sub-task of #${issueNumber}\n\n## Acceptance Criteria\n- [ ] ${taskDescription}\n- [ ] Tests pass\n- [ ] No linting errors\n\n## Parent Issue\nSee #${issueNumber} for context" \
    --label "copilot-ready,generated" \
    --assignee copilot`;
  
  try {
    const output = execSync(command).toString();
    console.log(`✅ Created Copilot issue: ${taskDescription}`);
    console.log(output);
  } catch (error) {
    console.error(`❌ Failed to create issue: ${taskDescription}`);
  }
});

console.log('\n✨ Copilot tasks have been created and assigned!');