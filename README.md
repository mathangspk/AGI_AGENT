# DevMate - Discord AI Coding Agent

DevMate is an AI agent that runs on Docker, integrated with Discord. It can read/write files, run commands, manage SSH connections, set reminders, and handle webhooks.

## Features

### AI Models
- NVIDIA DeepSeek V3.1 - High accuracy
- Groq (Llama 3.3 70B) - Fast responses

### Core Capabilities
- Read/write files in projects
- Run test/build commands
- Persistent memory (identity, goals, memory)
- Skill system with per-skill model selection

### SSH Management
- Generate SSH keys
- Connect to any server
- Run remote commands
- Password encryption

### Reminders
- Natural language time parsing
- Scheduled notifications
- Per-channel or DM delivery

### Webhooks
- Discord webhooks
- Git auto-deploy triggers
- Monitoring alerts
- Custom triggers

## Quick Start

### 1. Clone and Setup
git clone https://github.com/mathangspk/AGI_AGENT.git devmate
cd devmate
cp .env.example .env
nano .env

### 2. Configure .env
DISCORD_BOT_TOKEN=your_token
GROQ_API_KEY=your_groq_key
MOONSHOT_API_KEY=your_nvidia_key
DEFAULT_PROJECT=myproject

### 3. Create Discord Bot
1. Go to https://discord.com/developers/applications
2. Create Application - Bot
3. Enable Message Content Intent
4. Copy invite URL and add bot to server

### 4. Run
docker-compose up -d

## Project Structure

devmate/
├── bot/
│   ├── main.py                    # Entry point
│   ├── discord_client.py          # Discord handler
│   ├── llm/
│   │   └── router.py             # LLM routing + memory
│   ├── tools/
│   │   ├── ssh_manager.py        # SSH connections
│   │   ├── reminder_manager.py   # Cron/schedules
│   │   ├── webhook_manager.py    # Webhooks
│   │   ├── project_manager.py   # Project management
│   │   ├── command_exec.py      # Command execution
│   │   └── file_manager.py      # File operations
│   └── providers/
│       └── registry.py           # Provider config
├── workspace/devmate/            # Mounted from host
│   ├── identity.md              # Who the bot is
│   ├── goals.md                # Bots mission
│   ├── USER.md                 # User info
│   ├── AGENTS.md               # Workspace rules
│   ├── MEMORY.md               # Long-term memory
│   ├── memory/                 # Daily logs
│   ├── skills/                 # Bot skills
│   ├── config/                 # SSH, reminders, webhooks
│   └── keys/                   # SSH keys
├── projects/                    # Your code projects
├── config.json                   # Provider config
├── docker-compose.yml
├── Dockerfile
└── README.md

## Configuration

### config.json - Providers
{
  providers: {
    groq: {
      name: Groq,
      api_key_env: GROQ_API_KEY,
      models: [llama-3.3-70b-versatile],
      default_model: llama-3.3-70b-versatile
    },
    nvidia: {
      name: NVIDIA DeepSeek,
      api_key_env: MOONSHOT_API_KEY,
      models: [deepseek-ai/deepseek-v3.1],
      default_model: deepseek-ai/deepseek-v3.1,
      endpoint: https://integrate.api.nvidia.com/v1
    }
  },
  default_provider: groq
}

### Adding New Provider
anthropic: {
  name: Anthropic Claude,
  api_key_env: ANTHROPIC_API_KEY,
  models: [claude-3-opus-20240229],
  default_model: claude-3-opus-20240229,
  endpoint: https://api.anthropic.com/v1
}

## Commands

### Model Selection
@DevMate use groq - Switch to Groq for this session
@DevMate use nvidia - Switch to NVIDIA for this session
@DevMate use default - Use default provider
@DevMate which model - Show current model
@DevMate show providers - List available providers

### Skills
@DevMate create skill <name> - Create new skill (asks for model)
@DevMate list skills - List all skills
@DevMate set skill <name> model <provider> - Change skills model

### SSH
@DevMate ssh key generate - Generate SSH key
@DevMate ssh connect user@host -p 22 - Connect to server
@DevMate ssh connect user@host -password XYZ - Connect with password
@DevMate ssh run <command> - Run command on server
@DevMate ssh disconnect - Disconnect
@DevMate ssh status - Show connection status

### Reminders
@DevMate remind me in 20 minutes to check email - Set reminder
@DevMate remind me at 9:00 AM to standup - Set daily reminder
@DevMate list reminders - List all reminders
@DevMate delete reminder <id> - Delete reminder

### Webhooks
@DevMate webhook add <name> <url> - Add webhook
@DevMate webhook list - List webhooks
@DevMate webhook test <name> - Test webhook
@DevMate webhook delete <name> - Delete webhook
@DevMate webhook add-trigger <name> <trigger> - Add trigger (git, alert, monitor)

### General
@DevMate Who are you? - Show identity
@DevMate What is your mission? - Show goals

## Skill Format

Skills are stored in workspace/devmate/skills/ as markdown files with YAML frontmatter:

---
model: groq
description: Simple reminder skill
---
# Skill: reminder

## Description
Nhắc nhở người dùng về các task

## Usage
Khi user yêu cầu nhắc nhở...

## Backup and Restore

### Backup
Backup workspace (identity, memory, skills, configs):
tar -czvf workspace-backup.tar.gz workspace/

Backup projects:
tar -czvf projects-backup.tar.gz projects/

Git backup:
git add . && git commit -m Update && git push

### Restore
Clone repo:
git clone https://github.com/mathangspk/AGI_AGENT.git

Restore environment:
cp .env.example .env && nano .env

Restore backups:
tar -xzvf workspace-backup.tar.gz
tar -xzvf projects-backup.tar.gz

Rebuild and run:
docker-compose down
docker-compose build --no-cache
docker-compose up -d

## Development

### Adding New Features
1. New Tool: Add to bot/tools/
2. New Provider: Add to config.json and update bot/providers/registry.py
3. New Command: Add handler in bot/discord_client.py

### Testing
Build and run:
docker-compose up -d

View logs:
docker logs devmate

Restart:
docker-compose restart

## Files Description

File - Purpose
identity.md - Bots personality and values
goals.md - Bots mission and objectives
USER.md - User information
AGENTS.md - Workspace rules
MEMORY.md - Long-term memory (curated)
memory/YYYY-MM-DD.md - Daily conversation logs
skills/*.md - Bot skills
config/ssh.json - SSH connections
config/reminders.json - Scheduled reminders
config/webhooks.json - Webhook configurations
keys/id_rsa_* - SSH private keys

## Security Notes
- API keys stored in .env - never commit to git
- SSH passwords are encrypted with Fernet
- SSH keys stored in workspace/devmate/keys/
- Backup .env and workspace/ regularly

## Dependencies
discord.py>=2.0.0
groq>=0.4.0
openai>=1.0.0
python-dotenv>=1.0.0
aiofiles>=23.0.0
PyYAML>=6.0
paramiko>=2.12.0
cryptography>=41.0.0
aiohttp>=3.9.0
apscheduler>=3.10.0

## License
MIT
