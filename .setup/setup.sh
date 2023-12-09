#!/bin/bash

# Check for root/sudo privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root."
   exit 1
fi

# Set variables
botName="Discord-Tradingview-Image-Bot"
vpsUsername=$SUDO_USER
repoPath=$(pwd)

echo -e "Creating python .venv\n\n"
python3 -m venv .venv
source .venv/bin/activate
pip install -r .setup/requirements.txt


echo - e "\n\nInstalling/Configuring Supervisor\n\n"
sudo apt install supervisor
sudo tee /etc/supervisor/conf.d/${botName}.conf <<EOF
[program:${botName}]
user=${vpsUsername}
directory=$repoPath
command=$repoPath/.venv/bin/python3 $repoPath/src/main.py
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
stderr_logfile=/var/log/${botName}/${botName}.err.log
stderr_logfile_maxbytes=50MB
stderr_logfile_backups=10
stdout_logfile=/var/log/${botName}/${botName}.out.log
stdout_logfile_maxbytes=50MB
stdout_logfile_backups=10
EOF

sudo mkdir -p /var/log/${botName}
sudo touch /var/log/${botName}/${botName}.out.log
sudo touch /var/log/${botName}/${botName}.err.log


echo -e "\n\nServer setup complete. Be sure to setup your .env file for BOT_TOKEN, etc."
