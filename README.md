# DevMate - Discord AI Coding Assistant

DevMate la mot AI agent chay tren Docker, tich hop voi Discord de ho tro lap trinh. Ban chi can @mention bot tren Discord la co the:
- Doc/ghi/sua file trong du an
- Chay test va build commands
- Thuc hien cac tac vu lap trinh khac

## Tinh nang
- AI Models: DeepSeek V3.1 (NVIDIA), Groq (Llama 3.3 70B)
- Discord Integration: Phan hoi khi duoc @mention
- File Management: Doc, ghi, tao file trong project
- Command Execution: Chay test, build commands an toan
- Docker Deployment: Chay tren container, de dang backup/restore

## Cau hinh
1. Tao .env tu .env.example
2. Dien Discord Bot Token va API Keys
3. Chay: docker-compose up -d

## Backup & Restore
# Backup
cd devmate && git add . && git commit -m "Update" && tar -czvf projects-backup.tar.gz projects/

# Restore
git clone <repo> && tar -xzvf projects-backup.tar.gz && docker-compose up -d

## Su dung
@DevMate Doc file main.py
@DevMate Tao file test.py voi noi dung Hello World
@DevMate Chay pytest
