# Swing music

Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music. Just run the app and enjoy your music library in a web browser.

<a href="https://swingmusic-git-v130-swingmusic.vercel.app/support-us.html" target="_blank"><img src="screenshots/supportus.png" alt="Buy Me A Coffee" style="height: 60px !important;width: auto !important;" ></a>

| ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/artist.webp)  | ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/album.webp)  |
| ------------------------------------------------------------ | ----------------------------------------------------------- |
| ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/artist2.webp) | ![SWING MUSIC PLAYER BANNER IMAGE](screenshots/album2.webp) |

For full size screenshots, visit the [website](https://swingmusic.vercel.app).

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

| Option               | Short  | Description                                                                   |
| -------------------- | ------ | ----------------------------------------------------------------------------- |
| `--help`             | `-h`   | Show help message                                                             |
| `--version`          | `-v`   | Show the app version                                                          |
| `--host`             |        | Set the host                                                                  |
| `--port`             |        | Set the port                                                                  |
| `--config`           |        | Set the config path                                                           |
| `--no-periodic-scan` | `-nps` | Disable periodic scan                                                         |
| `--scan-interval`    | `-psi` | Set the periodic scan interval in seconds. Default is 300 seconds (5 minutes) |
| `--build`            |        | Build the application (in development)                                        |

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
| :----------: | -------------------------------------------------------------------------------------------- |
|  `-p 1970`   | WebUI                                                                                        |
| `-v /music`  | Recommended directory to store your music collection. You can bind other folder if you wish. |
| `-v /config` | Configuration files.                                                                         |

### Contributing

See [contributing guidelines](.github/contributing.md).

### License

This software is provided to you with terms stated in the MIT License. Read the full text in the `LICENSE` file located at the root of this repository.

**[MIT License](https://opensource.org/licenses/MIT) | Copyright (c) 2023 Mungai Njoroge**
