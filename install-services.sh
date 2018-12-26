#/bin/bash

# installs the systemctl services

chmod 664 lights.service
chmod 664 lights-api.service
cp lights.service /etc/systemd/system/lights.service
cp lights-api.service /etc/systemd/system/lights-api.service


