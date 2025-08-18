<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <img class="lo" src='.github/images/logo-fill.light.svg' style="height: 4rem">
</div>
<div align="center" style="font-size: 2rem"><b>Swing Music</b></div>

<div align="center"><b><sub><code>v2.0.9</code></sub></b></div>
 
**<div align="center" style="padding-top: 1.25rem">[Download](https://swingmx.com/downloads) • [Get Android Client](https://github.com/swingmx/android) •  <a href="https://github.com/sponsors/swingmx" target="_blank">Support Development</a> • [Docs](https://swingmx.com/guide/introduction.html) • [Screenshots](https://swingmx.com) • [r/SwingMusicApp](https://www.reddit.com/r/SwingMusicApp)</div>**

##

[![Image showing the Swing Music artist page](.github/images/artist.webp)](https://raw.githubusercontent.com/swing-opensource/swingmusic/master/.github/images/artist.webp)

##

Swing Music is a fast and beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music. Just run the app and enjoy your music library in a web browser.

## Features

- **Daily Mixes** - curated everyday based on your listening activity
- **Metadata normalization** - a clean and consistent library
- **Album versioning** - normalized albums and association with version labels (eg. Deluxe, Remaster, etc)
- **Related artist and albums**
- **Folder view** - Browse your music library by folders
- **Playlist management**
- **Beautiful browser based UI**
- **Silence detection** - Combine cross-fade with silence detection to create a seamless listening experience
- **Collections** - Group albums and artists based on your preferences
- **Statistics** - Get insights into your listening activity
- **Lyrics view**
- **Android client**
- **Last.fm scrobbling**
- **Multi-user support**
- **Cross-platform** - Windows, Linux, MacOS (coming soon), arm64, x86
- **Blazingly fast**
- **Pure awesomeness**

### Installation

Swing Music is available as pre-compiled binaries for Windows and Linux. Just download the latest release from the [downloads page](https://swingmusic.vercel.app/downloads) and launch it.

[FFmpeg](https://ffmpeg.org/) is needed for the audio silence skip feature, so you need to install it first. On windows, you can follows [this tutorial](https://phoenixnap.com/kb/ffmpeg-windows) to install FFmpeg.

On Linux, you can install FFmpeg using:

```sh
sudo apt-get install ffmpeg libev-dev libavcodec-extra -y
```

The `libev` package is needed on Linux and MacOS. You can install it on other system as shown:

```sh
# Arch Linux
pacman -S libev

# Fedora, CentOS
dnf install libev-devel

# MacOS
brew install libev
```

Then make the file executable first.

```bash
chmod a+x ./swingmusic

./swingmusic
```

The app should start at <http://localhost:1970> by default. Open it in your browser to configure and use Swing Music. You can change the default port by using the `--port` flag.

```sh
./swingmusic --port 1980
```

> [!IMPORTANT]
> The default password for user `admin` is "admin". Please change the password via the settings after first login.

To stream your music from your Android device, you can download the [Android mobile client](https://github.com/swingmx/android).

### Options

Options flags can be passed when starting the app in the terminal to tweak runtime settings or perform tasks. You can use the `-h` flag to see all supported options.

> [!TIP]
> You can read more about options in [the docs](https://swingmusic.vercel.app/guide/getting-started.html#options).

### Docker

Pull the latest Docker image and run it:

```sh
docker pull ghcr.io/swingmx/swingmusic:latest
```

```sh
docker run --name swingmusic -p 1970:1970 \
  -v /path/to/music:/music \
  -v /path/to/config:/config \
  --restart unless-stopped \
  ghcr.io/swingmx/swingmusic:latest
```

Don't forget to replace `/path/to/music` and `/path/to/config` with the appropriate values. In addition, specify the the `/music` directory as the root directory. Using the `Home Directory` option won't work.

> [!TIP]
> For more info, see the [Docker section](https://swingmusic.vercel.app/guide/getting-started.html#docker) on the docs.

#### Using Docker Compose

Here's a sample Docker compose file:

```yaml
services:
  swingmusic:
    image: ghcr.io/swingmx/swingmusic:latest
    container_name: swingmusic
    volumes:
      - /path/to/music:/music
      - /path/to/config:/config
    ports:
      - "1970:1970"
    restart: unless-stopped
```

### Contributing and Development

Swing Music is looking for contributors. If you're interested, please join us at the [Swing Music Community](https://t.me/+9n61PFcgKhozZDE0) group on Telegram. For more information, take a look at https://github.com/swing-opensource/swingmusic/issues/186.

[**CONTRIBUTING GUIDELINES**](.github/contributing.md).

> [!TIP]
> This project runs on Python 3.11 or newer and uses [uv](https://docs.astral.sh/uv) to manage dependencies. Please [install uv](https://docs.astral.sh/uv/getting-started/installation/) before continuing for an easy setup.

To set up this project on your computer follow the following steps:

```sh
# 1. Fork the project

git clone https://github.com/swingmx/swingmusic.git

# or via SSH

git clone git@github.com:swingmx/swingmusic.git
```

```sh
# 2. Install dependencies

uv sync
```

> [!TIP]
> The `libev` package is needed on Linux and MacOS. You can install it on other system as shown:
> 
> ```sh
> # Arch Linux
> pacman -S libev
> 
> # Fedora, CentOS
> dnf install libev-devel
> 
> # MacOS
> brew install libev
> ```

```sh
# 4. Run the program

uv run python run.py
```

### License

This software is provided to you with terms stated in the [AGPLv3 License](https://github.com/swingmx/swingmusic/blob/master/LICENSE) or any later version. Read the full text in the `LICENSE` file located at the root of this repository.

### Contributors

Shout out to the following code contributors who have helped maintain and improve Swing Music:

<div align="left">
  <table>
    <tr>
      <td align="center">
        <a href="https://github.com/cwilvx">
          <img src="https://github.com/cwilvx.png" width="80px;"/>
          <br />
          <sub><b>@cwilvx</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Ericgacoki">
          <img src="https://github.com/Ericgacoki.png" width="80px;" alt=""/>
          <br />
          <sub><b>@Ericgacoki</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Simonh2o">
          <img src="https://github.com/Simonh2o.png" width="80px;"/>
          <br />
          <sub><b>@Simonh2o</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/tcsenpai">
          <img src="https://github.com/tcsenpai.png" width="80px;"/>
          <br />
          <sub><b>@tcsenpai</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/jensgrunzer1">
          <img src="https://github.com/jensgrunzer1.png" width="80px;"/>
          <br />
          <sub><b>@jensgrunzer1</b></sub>
        </a>
      </td>
      <td align="center">
        <a href="https://github.com/Type-Delta">
          <img src="https://github.com/Type-Delta.png" width="80px;" alt=""/>
          <br />
          <sub><b>@Type-Delta</b></sub>
        </a>
      </td>
     <td align="center">
        <a href="https://github.com/MarcOrfilaCarreras">
          <img src="https://github.com/MarcOrfilaCarreras.png" width="80px;" alt=""/>
          <br />
          <sub><b>@MarcOrfilaCarreras</b></sub>
        </a>
      </td>
    </tr>
    <tr>
    <td align="center">
      <a href="https://github.com/tralph3">
        <img src="https://github.com/tralph3.png" width="80px;" alt=""/>
        <br />
          <sub><b>@tralph3</b></sub>
        </a>
      </td>
    </tr>
  </table>
</div>
