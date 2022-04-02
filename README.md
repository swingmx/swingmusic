### Alice Music

Alice is a web-based music player for playing and managing local music files. It interacts with the files using a Python Rest API which handles all the processing and basically most of the work.

This project is currently under very heavy development, and only a few of the features are functional. Some working features include:

- playing tracks
- playing tracks in queue
- adding tracks to playlists

Most of the features are underway and the user interface is consistently changing. Hopefully to make Alice better.

### Setting up a development Alice locally

Alice currently relies on a locally installed MongoDB for storing tracks data like playlists, Nginx for serving images and Python of course.

> This project is currently only tested on Ubuntu `20.04` running `Python 3.8.10`, Nginx `v1.18.0` and MongoDB server `v5.0.6`. Any other OS are not tested. If you are using a different OS, please help us by opening an issue or creating a pull request to fix what breaks.

Python comes installed on Ubuntu by default. If it's not installed, you need to install it.

```bash
sudo apt install python3.8
```

Then install and start MongoDB.

```bash
# add the necessary repositories
wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

sudo apt-get install gnupg

wget -qO - https://www.mongodb.org/static/pgp/server-5.0.asc | sudo apt-key add -

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/5.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-5.0.list

# install mongodb
sudo apt-get update
sudo apt-get install -y mongodb

# start mondodb services
sudo systemctl start mongodb
sudo systemctl daemon-reload
sudo systemctl enable mongodb
```

Then install and start Nginx.

```bash
sudo apt-get install nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

Alice uses a Vue.js client. You need Node.js `> v14.x` and yarn to work with it. If you don't have Node.js installed, you can install it using the following commands.

```bash
curl -fsSL https://deb.nodesource.com/setup_14.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Then install `yarn`:

```bash
sudo npm install -g yarn
```

With that done, clone this repo on your machine.

```bash
git clone https://github.com/geoffrey45/alice.git
cd ./alice
```

Then install the client dependencies and start the client development server.

```bash
yarn install
yarn dev
```
The development server will be started on <http://127.0.0.1:3000>.

That's pretty all there is to the client. Now we need to set up the actual desktop agent.

The Python server uses the `poetry` package manager. You need to install it first.

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Open a new terminal/tab and navigate to the `alice/server` directory and install the server dependencies.

```bash
cd ./server
poetry install
```
Then start the server.
```bash
./start.sh
```
The server will be started on <http://127.0.0.1:9876>.

Congratulations! You have successfully set up a development Alice instance. You should expect a lot of bugs. Please open an issue or open a pull request if you can help. We really appreciate your contribution.

![](./images/1.png)
