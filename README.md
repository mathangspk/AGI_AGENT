# DevMate - Discord AI Coding Assistant

DevMate is an AI agent that runs on Docker, integrated with Discord to support programming. Just @mention the bot on Discord to:

- Read/write/edit files in your projects
- Run tests and build commands
- Create and manage skills
- Have persistent memory between sessions

## Features

- AI Models: DeepSeek V3.1 (NVIDIA), Groq (Llama 3.3 70B)
- Discord Integration: Responds when @mentioned
- File Management: Read, write, create files in projects
- Command Execution: Run test, build commands safely
- Docker Deployment: Runs on container, easy backup/restore
- **Long-term Memory**: identity.md, goals.md, memory/, MEMORY.md
- **Skill System**: Create skills via chat

## Quick Start

### 1. Clone and Setup

[?2004h[?1049h[22;0;0t[1;24r(B[m[4l[?7h[39;49m[?1h=[?1h=[?25l[39;49m(B[m[H[2J[22;34H(B[0;1m[37m[42m[ Reading... ][39;49m(B[m[22;19H(B[0;1m[37m[42m[ Read 4 lines (converted from DOS format) ][39;49m(B[m[?12l[?25h[24;1H[?1049l[23;0;0t[?1l>[?2004l

Add your keys:
ProgramFiles(x86)=C:\Program Files (x86)
CommonProgramFiles(x86)=C:\Program Files (x86)\Common Files
NUMBER_OF_PROCESSORS=8
FPS_BROWSER_USER_PROFILE_STRING=Default
PROCESSOR_LEVEL=6
OPENCODE_EXPERIMENTAL_FILEWATCHER=true
USERDOMAIN_ROAMINGPROFILE=DESKTOP-DO3FFIR
PROGRAMFILES=C:\Program Files
MSYSTEM=MINGW64
ChocolateyInstall=C:\ProgramData\chocolatey
PATHEXT=.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC
JAVA_HOME=C:\Program Files\Java\jdk-17
OS=Windows_NT
AGENT=1
HOMEDRIVE=C:
USERDOMAIN=DESKTOP-DO3FFIR
PWD=/c/local/Agent_code
GIT_LFS_PATH=C:\Program Files\Git LFS
USERPROFILE=C:\Users\mango
OneDriveConsumer=C:\Users\mango\OneDrive
ALLUSERSPROFILE=C:\ProgramData
CommonProgramW6432=C:\Program Files\Common Files
OPENCODE_PID=20300
HOME=/c/Users/mango
USERNAME=mango
OPENCODE=1
EFC_9264_1592913036=1
PLINK_PROTOCOL=ssh
OneDrive=C:\Users\mango\OneDrive
COMSPEC=C:\WINDOWS\system32\cmd.exe
APPDATA=C:\Users\mango\AppData\Roaming
SYSTEMROOT=C:\WINDOWS
LOCALAPPDATA=C:\Users\mango\AppData\Local
OPENCODE_EXPERIMENTAL_ICON_DISCOVERY=true
__COMPAT_LAYER=DetectorsAppHealth
OPENCODE_SERVER_USERNAME=opencode
COMPUTERNAME=DESKTOP-DO3FFIR
TERM=xterm-256color
LOGONSERVER=\\DESKTOP-DO3FFIR
NO_PROXY=127.0.0.1,localhost,::1
PSModulePath=C:\Program Files\WindowsPowerShell\Modules;C:\WINDOWS\system32\WindowsPowerShell\v1.0\Modules
TEMP=/tmp
SHLVL=1
OPENCODE_CLIENT=desktop
PROCESSOR_REVISION=9a03
DriverData=C:\Windows\System32\Drivers\DriverData
COMMONPROGRAMFILES=C:\Program Files\Common Files
XDG_STATE_HOME=C:\Users\mango\AppData\Local\ai.opencode.desktop\
EXEPATH=C:\Program Files\Git\bin
PROCESSOR_IDENTIFIER=Intel64 Family 6 Model 154 Stepping 3, GenuineIntel
SESSIONNAME=Console
OPENCODE_SERVER_PASSWORD=e553d4e1-e7b2-4dca-a228-fae8a896d04f
HOMEPATH=\Users\mango
TMP=/tmp
PATH=/mingw64/bin:/usr/bin:/c/Users/mango/bin:/c/Program Files/Common Files/Oracle/Java/javapath:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/Program Files/dotnet:/c/Program Files/Git LFS:/cmd:/c/ProgramData/chocolatey/bin:/c/Program Files/bazel:/c/msys64/usr/bin:/c/Users/mango/AppData/Local/Programs/Python/Python312:/c/Users/mango/AppData/Local/Programs/Python/Python312/Scripts:/c/Program Files (x86)/CODESYS/APInstaller:/c/Program Files (x86)/Bitvise SSH Client:/c/Program Files/Tailscale:/c/Program Files/Common Files/Oracle/Java/javapath:/c/WINDOWS/system32:/c/WINDOWS:/c/WINDOWS/System32/Wbem:/c/WINDOWS/System32/WindowsPowerShell/v1.0:/c/WINDOWS/System32/OpenSSH:/c/Program Files/dotnet:/c/Program Files/Git LFS:/cmd:/c/ProgramData/chocolatey/bin:/c/Program Files/bazel:/c/msys64/usr/bin:/c/Users/mango/AppData/Local/Programs/Python/Python312:/c/Users/mango/AppData/Local/Programs/Python/Python312/Scripts:/c/Program Files (x86)/CODESYS/APInstaller:/c/Program Files (x86)/Bitvise SSH Client:/c/Program Files/Tailscale:/c/Program Files/bazel":/c/Users/mango/AppData/Local/Programs/Microsoft VS Code/bin:/c/Users/mango/AppData/Local/Programs/cursor/resources/app/bin
ProgramW6432=C:\Program Files
WINDIR=C:\WINDOWS
FPS_BROWSER_APP_PROFILE_STRING=Internet Explorer
PROCESSOR_ARCHITECTURE=AMD64
PUBLIC=C:\Users\Public
SYSTEMDRIVE=C:
ProgramData=C:\ProgramData
ChocolateyLastPathUpdate=134043814089319674
_=/usr/bin/env

### 2. Create Discord Bot

1. Go to https://discord.com/developers/applications
2. Create new Application
3. Go to Bot - Reset Token - Copy token
4. Go to Privileged Intents - Enable Message Content Intent
5. Go to OAuth2 - URL Generator - Select bot scope - Copy invite URL

### 3. Run



## Workspace Structure



## Commands

On Discord, @mention the bot:



## Backup & Restore



## Update



## Files in Workspace

| File | Purpose |
|------|---------|
| identity.md | Defines who the bot is |
| goals.md | Bot's mission and objectives |
| USER.md | Information about the user |
| AGENTS.md | Workspace rules |
| MEMORY.md | Long-term memory |
| memory/YYYY-MM-DD.md | Daily conversation logs |
| skills/*.md | Bot skills |

## Security Notes

- API keys are stored in .env - never commit to git
- The projects/ folder contains your code - backup regularly
- The workspace/ folder contains AI memory and skills
