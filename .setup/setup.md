## Discord Tradingview Image 🤖 Setup

### Requirements

- Linux VPS Server (I use Linode)
  - [My VPS Provider](https://www.linode.com/lp/refer/?r=3eabea16dddc74fdc11ae5d0a73cd919c1ed1ae0)
- Discord Server
- Discord Bot

### 1. Clone Git Repo

```bash
git clone https://github.com/theprogrammergary/Discord-Antispam-Bot

cd Discord-Antispam-Bot
```

### 2. Run Server Setup Script

```bash
sudo ./.setup/setup.sh
```

### 3. Setup .env

```bash
# Create .env file (.envSample file is provided in /.setup)
sudo nano ./.setup/.env

# Configure your specific vars
Example:
BOT_TOKEN=123456789101112
```

### 5. Reboot

```bash
sudo reboot
```

### 6. Check Status of Bot

```bash
sudo supervisorctl status all
```
