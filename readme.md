sudo nano /etc/systemd/system/main.service


[Unit]
Description=Main Python Script Service
After=network.target

[Service]
ExecStart=/bin/bash /home/pi/tiktok/start.sh
WorkingDirectory=/home/pi/tiktok
Restart=always
User=pi
Group=pi

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload
sudo systemctl enable main.service
sudo systemctl start main.service
sudo systemctl status main.service

journalctl -u main.service
