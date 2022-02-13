# 1. install nginx
# 2. install mongodb

# commands to install and start mongodb ubuntu 20.04
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
sudo apt-get install gnupg
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list
sudo apt-get update
sudo apt-get install -y mongodb

sudo systemctl start mongodb
sudo systemctl daemon-reload
sudo systemctl enable mongodb

# commands to install and start nginx ubuntu 20.04
sudo apt-get install nginx
sudo systemctl start nginx
sudo systemctl enable nginx