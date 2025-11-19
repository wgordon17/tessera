# Autonomy - Multi-Agent AI Framework

A sophisticated multi-agent AI framework implementing **Supervisor** and **Interviewer** personas with panel-based evaluation systems. Built on LangChain with support for multiple LLM providers (OpenAI, Anthropic, Azure).

## Features

### 🎯 Supervisor Agent
- **Task Decomposition**: Breaks complex objectives into actionable subtasks
- **Agent Coordination**: Assigns tasks to appropriate agents based on capabilities
- **Progress Monitoring**: Tracks task completion and identifies blockers
- **Quality Control**: Reviews outputs for coherence and completeness
- **Conflict Resolution**: Mediates disagreements and makes final decisions

### 🎤 Interviewer Agent
- **Candidate Evaluation**: Structured interviews to assess agent/model suitability
- **Comparative Analysis**: Ranks multiple candidates using weighted scoring
- **Tie-Breaking**: Resolves tied votes with additional evaluation rounds
- **Performance Documentation**: Maintains evaluation records with detailed justifications

### 👥 Panel Interview System
- **Round-Robin Voting**: Multiple panelists with diverse perspectives
- **5 Specialized Roles**: Technical, Creative, Efficiency, User-Centric, Risk evaluators
- **Scoring Rubrics**: 6 weighted metrics (Accuracy, Relevance, Completeness, etc.)
- **Democratic Process**: Majority vote with automatic tie-breaking

### 💬 Slack Approval Workflows (NEW!)
- **LangGraph Integration**: Native integration with LangGraph's interrupt() for approval gates
- **Socket Mode**: Self-hosted, no webhooks required - uses Slack SDK Socket Mode
- **Interactive Buttons**: Approve/Deny actions directly from Slack Block Kit UI
- **Async Workflows**: Non-blocking execution that pauses for human decisions
- **Multi-Channel**: Route different approval types to different Slack channels
- **Local State**: SQLite-based checkpointing for resumable workflows

## Quick Start

```bash
git clone <repository-url> && cd autonomy
# Optional: Install direnv for automatic .env loading
brew install direnv && echo 'eval "$(direnv hook zsh)"' >> ~/.zshrc && direnv allow .
uv sync
```

**Option 1: GitHub Copilot (Free)**
```bash
# Generate Copilot token (NOT a GitHub PAT!)
npx copilot-api@latest auth
# Follow prompts, then save the ghu_* token to .env or 1Password
export GITHUB_TOKEN=ghu_your_copilot_token_here
```
```python
from autonomy import start_proxy, SupervisorAgent
start_proxy(rate_limit=30, use_wait=True)
supervisor = SupervisorAgent()
```

**Option 2: OpenAI**
```bash
cp .env.example .env  # Add: OPENAI_API_KEY=sk-your-key
```
```python
from autonomy import SupervisorAgent
supervisor = SupervisorAgent()
```

**Option 3: Anthropic**
```python
from autonomy import SupervisorAgent
from autonomy.config import LLMConfig
supervisor = SupervisorAgent(config=LLMConfig.from_env(provider='anthropic'))
# Requires: ANTHROPIC_API_KEY=sk-ant-your-key in .env
```


## Configuration

### Environment Variables

Configure in `.env` file (or use [1Password](#security-1password-integration) for secure secret management):

```bash
# Option 1: GitHub Copilot Proxy (FREE with Copilot subscription)
# First run: npx copilot-api@latest auth
OPENAI_BASE_URL=http://localhost:4141/v1
GITHUB_TOKEN=ghu_your_copilot_token_here  # Must start with ghu_ (NOT ghp_!)

# Option 2: Direct OpenAI API
OPENAI_API_KEY=your_openai_api_key_here  # Or use 1Password CLI
OPENAI_MODEL=gpt-4-turbo-preview

# Option 3: Anthropic Claude
ANTHROPIC_API_KEY=your_anthropic_api_key_here  # Or use 1Password CLI
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Option 4: Azure OpenAI
AZURE_OPENAI_API_KEY=your_azure_key_here
AZURE_OPENAI_ENDPOINT=your_azure_endpoint_here
AZURE_OPENAI_DEPLOYMENT=your_deployment_name_here

# Optional settings
DEFAULT_TEMPERATURE=0.7
MAX_ITERATIONS=10
ENABLE_LOGGING=true
```

**Secure Secret Management**: Use [1Password](#security-1password-integration) for encrypted storage instead of plaintext `.env`.

## Examples

```bash
python tests/examples/basic_supervisor.py           # Task decomposition
python tests/examples/interviewer_evaluation.py     # Candidate evaluation
python tests/examples/panel_interview.py            # Panel voting
python tests/examples/retry_and_rate_limiting_example.py  # Rate limiting
python tests/examples/test_slack_approval.py        # Slack approval workflows (NEW!)
```

## Architecture

### Core Components

```
autonomy/
├── models.py          # Data models (Task, Score, Ballot, etc.)
├── config.py          # Configuration and prompts
├── llm.py            # LLM provider abstraction
├── supervisor.py     # Supervisor agent implementation
├── interviewer.py    # Interviewer agent implementation
├── panel.py          # Panel interview system
└── secrets.py        # Secure secret management (1Password CLI)
```

### Key Concepts

**Task Decomposition Flow:**
```
Objective → Supervisor → Subtasks → Agents → Review → Synthesis
```

**Interview Flow:**
```
Task → Questions → Candidates → Scoring → Ranking → Selection
```

**Panel Flow:**
```
Task → Panel Setup → Round-Robin Q&A → Scoring → Voting → Decision
```

## Scoring System

### Metrics (0-5 scale each)

| Metric | Weight | Description |
|--------|--------|-------------|
| Accuracy | 30% | Correctness and precision |
| Relevance | 20% | Alignment with requirements |
| Completeness | 15% | Thoroughness of solution |
| Explainability | 10% | Clarity and understandability |
| Efficiency | 10% | Resource and cost awareness |
| Safety | 15% | Risk mitigation and ethics |

### Weighted Score Calculation

```
Overall Score = 100 × Σ(weight_i × metric_i / 5)
```

## Configuration

### Custom LLM Provider

```python
from autonomy.config import LLMConfig
from autonomy import SupervisorAgent

# Use Anthropic
config = LLMConfig.from_env(provider="anthropic")
supervisor = SupervisorAgent(config=config)

# Use Azure
config = LLMConfig.from_env(provider="azure")
supervisor = SupervisorAgent(config=config)
```

### Custom Scoring Weights

```python
from autonomy.config import ScoringWeights, FrameworkConfig

weights = ScoringWeights(
    accuracy=0.4,
    relevance=0.2,
    completeness=0.1,
    explainability=0.1,
    efficiency=0.1,
    safety=0.1
)

config = FrameworkConfig(scoring_weights=weights)
interviewer = InterviewerAgent(config=config)
```

### Custom Prompts

```python
from autonomy import SupervisorAgent

CUSTOM_SUPERVISOR_PROMPT = """
You are a specialized supervisor for data science projects...
"""

supervisor = SupervisorAgent(system_prompt=CUSTOM_SUPERVISOR_PROMPT)
```

## API Integration Notes

### GitHub Copilot Proxy

GitHub Copilot does **not** provide an official public API, but we've integrated a **reverse-engineered proxy** that makes it work:

✅ **Copilot Proxy** - Use your Copilot subscription via proxy (see [Copilot Proxy Details](#copilot-proxy-details))
✅ **OpenAI** - Official API, direct integration
✅ **Anthropic** - Official API, Claude models
✅ **Azure OpenAI** - Enterprise deployment

**Why use the Copilot proxy?**
- 💰 **Free** if you already have Copilot subscription
- 🚀 **GPT-4 access** included with Copilot
- 🔄 **OpenAI-compatible** endpoints (no code changes)
- 🔧 **Subprocess management** (no Docker required)

See [Copilot Proxy Details](#copilot-proxy-details) for complete setup instructions.

### Supported Providers Comparison

| Provider | Cost | Setup Complexity | Models | Best For |
|----------|------|------------------|--------|----------|
| **Copilot Proxy** | Free (with subscription) | Medium (requires Node.js) | GPT-4, GPT-3.5 | Development, cost savings |
| **OpenAI Direct** | Pay-per-use | Easy | All OpenAI models | Production, latest models |
| **Anthropic** | Pay-per-use | Easy | Claude models | Production, Claude preference |
| **Azure OpenAI** | Pay-per-use | Medium | OpenAI models | Enterprise, compliance |

## Development

```bash
pytest               # Run tests (93 passing)
ruff format src/     # Format code
ruff check src/      # Lint code
mypy src/            # Type check
```

All caches in `.cache/` directory. See [tests/README.md](tests/README.md) for details.

## Project Structure

```
autonomy/
├── src/autonomy/           # Main package
│   ├── __init__.py
│   ├── models.py          # Pydantic models
│   ├── config.py          # Configuration
│   ├── llm.py             # LLM providers
│   ├── supervisor.py      # Supervisor agent
│   ├── interviewer.py     # Interviewer agent
│   ├── panel.py           # Panel system
│   └── secrets.py         # Secure secret management
├── tests/                 # Test suite (93 tests passing)
│   ├── examples/          # Usage examples
│   │   ├── basic_supervisor.py
│   │   ├── interviewer_evaluation.py
│   │   ├── panel_interview.py
│   │   ├── copilot_proxy_example.py
│   │   ├── 1password_example.py
│   │   └── retry_and_rate_limiting_example.py
│   └── README.md         # Testing guide
├── pyproject.toml        # Dependencies & tool configs
├── .env.example          # Environment template
├── .envrc                # direnv config (auto-loads .env)
├── .gitignore            # Git ignore rules
├── .python-version       # Python 3.13
├── uv.lock               # Dependency lock file
└── README.md             # This file (self-contained docs)
```

## Security: 1Password Integration

Store API keys in 1Password instead of plaintext `.env` files:

### Setup

```bash
# 1. Install 1Password CLI
brew install 1password-cli

# 2. Sign in to 1Password
eval $(op signin)
```

### Get Secret References

1. Open 1Password app
2. Navigate to your secret (e.g., "GitHub Copilot" item)
3. Click the field you want to use (e.g., "copilot-token")
4. Click **"Copy Secret Reference"** (shows as `op://...`)
5. Paste into your `.env` file

### Configure .env

```bash
# Use op:// secret references instead of plaintext
OP_GITHUB_ITEM=op://Private/GitHub-Copilot/copilot-token
OP_OPENAI_ITEM=op://Private/OpenAI-API/credential
OP_ANTHROPIC_ITEM=op://Private/Anthropic-API/credential
```

**Format:** `op://VaultName/ItemName/FieldName`

Framework automatically reads from 1Password (fallback: env var → 1Password → None).

**GitHub Copilot Token:** Generate via `npx copilot-api@latest auth` (NOT a GitHub PAT! Must start with `ghu_`)

## Premium Model Protection

**Automatic protection against accidental premium model usage!**

The framework automatically fetches the latest premium model list from GitHub's documentation and **blocks premium models** unless you explicitly opt-in. This prevents accidental consumption of your limited monthly quota (300 premium requests/month on Copilot Individual).

### How It Works

1. **Automatic Detection**: Parses https://docs.github.com/en/copilot/concepts/billing/copilot-requests on startup
2. **24-Hour Cache**: Results cached in `.cache/premium_models.json` for performance
3. **Explicit Opt-In Required**: Premium models blocked by default

### Usage

```python
# ❌ This will FAIL - premium model without opt-in
config = LLMConfig(
    models=["claude-3.5-sonnet"],  # Premium model!
    base_url="http://localhost:4141/v1"
)

# ✅ This works - explicit opt-in
config = LLMConfig(
    models=["claude-3.5-sonnet"],
    base_url="http://localhost:4141/v1",
    allow_premium_models=True  # Explicit permission
)

# ✅ Free models work without opt-in
config = LLMConfig(
    models=["gpt-4o", "gpt-5-mini"],  # Free unlimited models
    base_url="http://localhost:4141/v1"
)
```

### Environment Variable

```bash
# In .env file
ALLOW_PREMIUM_MODELS=true  # Enable premium models globally
```

### Premium Models & Multipliers

| Model | Multiplier | Monthly Cost (300 quota) |
|-------|-----------|--------------------------|
| **Free Models** (Unlimited) | | |
| gpt-5-mini | 0× | Free |
| gpt-4.1 | 0× | Free |
| gpt-4o | 0× | Free |
| **Discounted Premium** | | |
| claude-haiku-4.5 | 0.33× | 909 requests/month |
| grok-code-fast-1 | 0.25× | 1200 requests/month |
| **Standard Premium** | | |
| claude-3.5-sonnet | 1× | 300 requests/month |
| claude-sonnet-4 | 1× | 300 requests/month |
| claude-sonnet-4.5 | 1× | 300 requests/month |
| gemini-2.5-pro | 1× | 300 requests/month |
| gpt-5 | 1× | 300 requests/month |
| gpt-5-codex | 1× | 300 requests/month |
| **Expensive Premium** | | |
| claude-opus-4.1 | 10× | 30 requests/month |

**Source**: https://docs.github.com/en/copilot/concepts/billing/copilot-requests

## Slack Approval Workflows

Add Slack-based approval gates to your LangGraph workflows using native Slack SDK Socket Mode. Completely self-hosted - no external services or webhooks required.

### Quick Setup (20 minutes)

1. **Create Slack App** (10 min):
   - Go to https://api.slack.com/apps → Create New App
   - Enable **Socket Mode** in settings
   - Create app-level token with `connections:write` scope → save as `SLACK_APP_TOKEN`
   - Add bot token scopes: `chat:write`, `chat:write.public`
   - Install to workspace and copy Bot Token → save as `SLACK_BOT_TOKEN`

2. **Configure Environment** (5 min):
   ```bash
   # Add to .env
   SLACK_APP_TOKEN=xapp-your-app-token
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APPROVAL_CHANNEL=C123456789  # Your Slack channel ID
   ```

3. **Test Integration** (5 min):
   ```bash
   export UV_PROJECT_ENVIRONMENT=.cache/.venv
   # Terminal 1: Start Socket Mode listener
   uv run python examples/slack_approval_demo.py

   # Terminal 2: Invoke graph with approval
   uv run python examples/slack_approval_invoke.py
   ```

**See [docs/SLACK_SETUP_GUIDE.md](docs/SLACK_SETUP_GUIDE.md) for complete setup instructions.**

### Usage Example

```python
from autonomy.slack_approval import SlackApprovalCoordinator, create_slack_client
from autonomy.supervisor_graph import SupervisorGraph

# Initialize Slack Socket Mode client
slack_client = create_slack_client()

# Initialize graph and coordinator
supervisor = SupervisorGraph()
coordinator = SlackApprovalCoordinator(
    graph=supervisor,
    slack_client=slack_client
)

# Register event handler for button clicks
slack_client.socket_mode_request_listeners.append(
    coordinator.create_event_handler()
)

# Connect to Slack (blocks until interrupted)
slack_client.connect()

# In another process, invoke with approval
result = coordinator.invoke_with_slack_approval(
    input_data={"objective": "Deploy to production"},
    thread_id="deploy-123",
    slack_channel="C123456789"
)
```

### How It Works

1. **LangGraph Interrupt**: Graph calls `interrupt()` when approval needed
2. **Slack Message**: Coordinator sends message with Approve/Reject buttons
3. **User Response**: Human clicks button in Slack
4. **Resume Graph**: Coordinator resumes execution with user's decision
5. **Local State**: SQLite checkpoint preserves state between pause/resume

### Resources

- **Setup Guide**: [docs/SLACK_SETUP_GUIDE.md](docs/SLACK_SETUP_GUIDE.md)
- **Demo Script**: `examples/slack_approval_demo.py`
- **Invoke Script**: `examples/slack_approval_invoke.py`
- **Tests**: `tests/test_slack_approval.py`

## Copilot Proxy Details

### Authentication

**IMPORTANT:** The Copilot proxy requires a special token generated via `npx copilot-api@latest auth`, **NOT** a GitHub Personal Access Token (PAT)!

```bash
# Generate Copilot authentication token
npx copilot-api@latest auth

# Follow the prompts to authenticate with GitHub
# This will generate a token starting with ghu_ (NOT ghp_!)

# Save the token to your .env file or 1Password
# GITHUB_TOKEN=ghu_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Token Format Validation:**
- ✅ Valid: `ghu_*` (Copilot-specific token from `npx copilot-api@latest auth`)
- ❌ Invalid: `ghp_*` (GitHub PAT - will be rejected!)
- ❌ Invalid: `gho_*` (GitHub OAuth token - not supported)

### Usage

**Subprocess mode** (no Docker):
```python
from autonomy import start_proxy, stop_proxy
start_proxy(rate_limit=30, use_wait=True)  # Manages npx process
supervisor = SupervisorAgent()
stop_proxy()
```

**Context manager** (auto-cleanup):
```python
from autonomy.copilot_proxy import CopilotProxyManager
with CopilotProxyManager(rate_limit=30, use_wait=True) as proxy:
    supervisor = SupervisorAgent()
```

**Prerequisites**: `brew install node` • Run `npx copilot-api@latest auth` • Proxy source: [ericc-ch/copilot-api](https://github.com/ericc-ch/copilot-api)

## Rate Limiting

Client retries (`.env`):
```bash
MAX_RETRIES=3              # Exponential backoff on errors
REQUEST_TIMEOUT=90.0       # Per-request timeout
```

Proxy rate limiting (avoid GitHub bans):
- `rate_limit=30`: Minimum 30s between requests
- `use_wait=True`: Queue instead of rejecting

**Troubleshooting**: Auth error → check token scope • Rate limited → increase interval • Timeout → increase `REQUEST_TIMEOUT`

## License

MIT License

---

Built with [LangChain](https://github.com/langchain-ai/langchain), [Pydantic](https://github.com/pydantic/pydantic), and [Rich](https://github.com/Textualize/rich)
