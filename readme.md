sudo nano /etc/systemd/system/main.service


[Unit]
Description=Main Python Script Service
After=network.target

[Service]
ExecStart=/bin/bash /path/to/start.sh
WorkingDirectory=~/
Environment="RUN_RPI=1"
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload