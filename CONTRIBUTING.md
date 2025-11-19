# Contributing to Tessera

## Commit Message Guidelines

Tessera follows the [Conventional Commits](https://www.conventionalcommits.org/) specification.

### Format

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **chore**: Maintenance tasks (dependencies, configs)
- **refactor**: Code refactoring
- **test**: Test additions or modifications
- **perf**: Performance improvements

### Scopes

Project-specific scopes for Tessera:

- **cli**: Command-line interface
- **config**: Configuration system
- **workflow**: Phase and task execution
- **observability**: Metrics, tracing, cost tracking
- **agents**: Agent implementations
- **tools**: Tool system and plugins
- **slack**: Slack integration
- **api**: HTTP API and sessions
- **repo**: Repository structure changes

### Examples

**Good:**
```
feat(cli): add interactive mode with user prompts

Implements guided workflow for task input with complexity
selection and interview mode option.
```

```
fix(observability): correct token extraction from LiteLLM responses

Token callback now properly captures usage metadata from
LangChain LiteLLM wrapper.
```

```
chore(deps): add google-cloud-aiplatform for Vertex AI support
```

**Bad:**
```
🎉 ADDED COOL NEW FEATURE!!! (with emojis and caps)
```

```
Updated files - Changed 50 files, 200 lines added, files:
src/foo.py, src/bar.py, ... (file listings)
```

### Guidelines

**DO:**
- Use present tense ("add feature" not "added feature")
- Be concise in description (50 chars or less)
- Use body for detailed explanation if needed
- Reference issues: "Closes #123"

**DON'T:**
- Use emojis in commit messages
- Use ALL CAPS
- List changed files (git does this)
- Include detailed statistics (lines changed, etc.)
- Add meta-commentary ("Generated with...", "Co-Authored-By...")

### Breaking Changes

For breaking changes, add `!` after type/scope and explain in footer:

```
feat(api)!: change task queue API structure

BREAKING CHANGE: TaskQueue.get_tasks() now returns QueuedTask objects
instead of plain dicts. Update all callers accordingly.
```

## Development Workflow

1. Create feature branch: `git checkout -b feat/my-feature`
2. Make changes with atomic commits
3. Follow commit guidelines above
4. Test thoroughly
5. Push and create PR to upstream

## Code Style

- Python 3.13+
- Type hints required
- Docstrings for public APIs
- pytest for testing
- ruff for formatting/linting

See `pyproject.toml` for detailed configuration.
