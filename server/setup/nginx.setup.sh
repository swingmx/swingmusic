# 1. copy sites configs
# 2. create symbolic links for each file in sites-available to sites-enable

sudo cp ./nginx-sites/* /etc/nginx/sites-available
sudo ln -s /etc/nginx/sites-available/* /etc/nginx/sites-enabled -f