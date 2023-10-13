#!/usr/bin/env bash
set -e
cd /opt/star-burger
git stash
git pull star-burger master
echo -e "\e[1;32m Files updated.\e[0m"
eval "$(pyenv init -)"
pyenv activate venv
pip3 install -r requirements.txt
echo -e "\e[1;32m Requirements updated.\e[0m"
npm install --dev
.node_modules/.bin/parcel build bundles-src/index.js --dist-dir bundles --public-url="./"
python3 manage.py collectstatic --noinput
echo -e "\e[1;32m Frontend updated.\e[0m"
python3 manage.py migrate --noinput
echo -e "\e[1;32m Migrations applied.\e[0m"
systemctl restart star-burger.service
echo -e "\e[1;32m Star-burger restarted.\e[0m"
systemctl reload nginx.service
echo -e "\e[1;32m Nginx reloaded.\e[0m"
if [ "${ROLLBAR_TOKEN}" ] && [ "${ROLLBAR_ENV}" ];
then
  curl -X POST https://api.rollbar.com/api/1/deploy \
        -H "X-Rollbar-Access-Token: $ROLLBAR_TOKEN" \
        -d "environment=$ROLLBAR_ENV&revision=$(git rev-parse HEAD)"
fi
echo -e "\e[1;32m Success!\e[0m"
