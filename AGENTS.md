# Software Factory

## Overview
Software Factory is a collection of actions for GitHub Actions that accelerate LLM-driven development.

## Project structure
- `.github/` - GitHub workflows, issue templates etc for developing this repo (which is a user of the factory)
- `actions/` - GitHub Actions action definitions, each folder represents a separate action
  - `execute/` - Takes a plan from a GitHub issue comment and creates a pull request to implement the plan
  - `plan/` - Takes a GitHub issue and comments on the issue with a proposed plan for the feature, bug etc
  - `review/` - Reviews an open GitHub pull request
- `factory/` - Python code to interface with LLM agents

## Constraints
- Agents must never edit the following files/directories without explicit confirmation from the user:
  - `.github/`
  - `AGENTS.md`
