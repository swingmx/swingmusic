# Swing music

Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring
your own music. Just run the app and
enjoy your music library in a web browser.

| ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/readme-artist.webp)   | ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/readme-album.webp)    |
|----------------------------------------------------------------------|----------------------------------------------------------------------|
| ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/readme-playlist.webp) | ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/readme-playlist.webp) |

### For more screenshots, see the [screenshots page on the website](https://swingmusic.vercel.app/screenshots.html).


### Setup

Swing Music is available as pre-compiled binaries for Windows and Linux. Just download the latest release from
the [release page](https://github.com/geoffrey45/swingmusic/releases) and launch it.
For Linux, you need to make the file executable first.

```bash
chmod a+x ./swingmusic

./swingmusic
```

The app should start at <http://localhost:1970> by default. You can change the default port or host by using
the `--host` and `--port` flags.

```
Usage: swingmusic [options]
```

### Options

| Flags                    | Description                                                                                                        |
|--------------------------|--------------------------------------------------------------------------------------------------------------------|
| --help, -h               | Show this help message                                                                                             |
| --version, -v            | Show the app version                                                                                               |
| --host                   | Set the host                                                                                                       |
| --port                   | Set the port                                                                                                       |
| --config                 | Set the config path                                                                                                |
| --show-feat, -sf         | Do not extract featured artists from the song  title                                                               |
| --show-prod, -sp         | Do not hide producers in the song title                                                                            |
| --no-clean-albums,  -nca | Don't clean album titles. Cleaning is done by     removing information in parentheses and    showing it separately |
| --no-clean-tracks,-nct   | Don't remove remaster information from track   titles                                                              |
| --no-periodic-scan, -nps | Disable periodic scan                                                                                              |
| --scan-interval,    -psi | Set the periodic scan interval in seconds.       Default is 300 seconds (5 minutes)                                |
|                          |                                                                                                                    |
| --build                  | Build the application (in development)                                                                             |

To stream your music across your local network, use the `--host` flag to run the app in all ports. Like this:

```sh
swingmusic --host 0.0.0.0
```

The link to access the app will be printed on your terminal. Copy it and open it in your browser.

### Docker

You can run Swing Music in a Docker container. To do so, clone the repository and build the image:

```bash
git clone https://github.com/swing-opensource/swingmusic.git --depth 1
cd swingmusic
docker build . -t swingmusic
```

Then create the container. Here are some example snippets to help you get started creating a container.

#### docker-compose

```yaml
---
version: "3.8"
services:
  swing:
    image: swingmusic
    container_name: swingmusic
    volumes:
      - /path/to/music:/music
      - /path/to/config:/config
    ports:
      - "1970:1970"
    restart: unless-stopped
```

#### docker cli

```bash
docker run -d \
  --name=swingmusic \
  -p 1970:1970 \
  -v /path/to/music:/music \
  -v /path/to/config:/config \
  --restart unless-stopped \
  swingmusic
```

#### Parameters

Container images are configured using parameters passed at runtime (such as those above). These parameters are separated
by a colon and indicate `<external>:<internal>` respectively. For example, `-p 8080:80` would expose port `80` from
inside the container to be accessible from the host's IP on port `8080` outside the container.

|  Parameter   | Function                                                                                     |
|:------------:|----------------------------------------------------------------------------------------------|
|  `-p 1970`   | WebUI                                                                                        |
| `-v /music`  | Recommended directory to store your music collection. You can bind other folder if you wish. |
| `-v /config` | Configuration files.                                                                         |

### Development

This project is broken down into 2. The client and the server. The client comprises of the user interface code. This
part is written in Typescript, Vue 3 and SCSS. To setup the client, checkout
the [swing client repo ](https://github.com/geoffrey45/swing-client) on GitHub.

The second part of this project is the server. This is the main part of the app that runs on your machine, interacts
with audio files and send data to the client. It's written in Python 3.

The following instructions will guide you on how to setup the **server**.

---

The project uses [Python poetry](https://python-poetry.org) as the virtual environment manager. Follow the instructions
in [their docs](https://python-poetry.org/docs/) to install it in your machine.

> It is assumed that you have `Python 3.10` or newer installed in your machine. This project uses type hinting features
> so older version of Python will not work. If you don't have Python installed in your machine, get it from
> the [python website](https://www.python.org/downloads/).

Clone this repo locally in your machine. Then install the project dependencies and start the app.

```sh
git clone https://github.com/geoffrey45/swingmusic.git

cd swingmusic

# install dependencies using poetry
poetry install

# start the app
poetry run python manage.py
```

### Contributing

If you want to contribute to this project, feel free to open an issue or a pull request on Github. Your contributions
are highly valued and appreciated. Feature suggestions, bug reports and code contribution are welcome.

### License

This software is provided to you with terms stated in the MIT License. Read the full text in the `LICENSE` file located
at the root of this repository.

**[MIT License](https://opensource.org/licenses/MIT) | Copyright (c) 2023 Mungai Njoroge**
