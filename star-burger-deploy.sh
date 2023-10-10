#!/usr/bin/env bash
set -e
cd /opt/star-burger
git pull star-burger master
echo -e "\e[1;32m Files updated.\e[0m"
eval "$(pyenv init -)"
pyenv activate venv
pip3 install -r requirements.txt
echo -e "\e[1;32m Requirements updated.\e[0m"
echo $(npm install --dev)
echo $(.node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./")
echo $(python3 manage.py collectstatic --noinput)
echo -e "\e[1;32m Frontend updated.\e[0m"
python3 manage.py migrate --noinput
pyenv deactivate
echo -e "\e[1;32m Migrations applied.\e[0m"
systemctl daemon-reload
echo -e "\e[1;32m Systemd reloaded.\e[0m"
systemctl restart star-burger.service
echo -e "\e[1;32m Starburger restarted.\e[0m"
systemctl reload nginx.service
echo -e "\e[1;32m Nginx reloaded.\e[0m"
echo -e "\e[1;32m Success!\e[0m"
