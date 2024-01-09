<div align="center" style="display: flex; justify-content: center; align-items: center;">
  <img class="lo" src='.github/images/logo-fill.light.svg' style="height: 4rem">
</div>
<div align="center" style="font-size: 2rem"><b>Swing Music</b></div>

<div align="center"><b><sub><code>v1.4.6</code></sub></b></div>
 
**<div align="center" style="padding-top: 1.25rem">[Download](https://swingmusic.vercel.app/downloads) • <a href="https://swingmusic.vercel.app/support-us.html" target="_blank">Support Development</a> • [Docs](https://swingmusic.vercel.app/guide/introduction.html) • [Screenshots](https://swingmusic.vercel.app) • [r/SwingMusicApp](https://www.reddit.com/r/SwingMusicApp)</div>**

##

[![Image showing the Swing Music artist page](.github/images/artist.webp)](https://raw.githubusercontent.com/swing-opensource/swingmusic/master/.github/images/artist.webp)

##

Swing Music is a beautiful, self-hosted music player for your local audio files. Like a cooler Spotify ... but bring your own music. Just run the app and enjoy your music library in a web browser.

### Installation

Swing Music is available as pre-compiled binaries for Windows and Linux. Just download the latest release from the [downloads page](https://swingmusic.vercel.app/downloads) and launch it.

For Linux, you need to make the file executable first.

```bash
chmod a+x ./swingmusic

./swingmusic
```

The app should start at <http://localhost:1970> by default. Open it in your browser to use Swing Music. You can change the default port by using the `--port` flags.

```sh
swingmusic --port 1980
```

### Options

Options are flags that can be passed when starting the app in the terminal to tweak runtime settings or perform tasks. You can use the `-h` flag to see all supported options. 

> [!TIP]
> You can read more about options in [the docs](https://swingmusic.vercel.app/guide/getting-started.html#options). 

### Docker

Pull the latest Docker image and run it:

```sh
docker pull ghcr.io/swing-opensource/swingmusic:latest
```

```sh
docker run --name swingmusic -p 1970:1970 \
  -v /path/to/music:/music \
  -v /path/to/config:/config \
  --restart unless-stopped \
  ghcr.io/swing-opensource/swingmusic:latest
```

Don't forget to replace `/path/to/music` and `/path/to/config` with the appropriate values. In addition, specify the the `/music` directory as the root directory. Using the `Home Directory` option won't work.

> [!TIP]
> For more info, see the [Docker section](https://swingmusic.vercel.app/guide/getting-started.html#docker) on the docs.

#### Using Docker Compose

Here's a sample Docker compose file:

```yaml
services:
  swingmusic:
    image: swingmusic
    container_name: swingmusic
    volumes:
      - /path/to/music:/music
      - /path/to/config:/config
    ports:
      - "1970:1970"
    restart: unless-stopped
```

### Contributing

See [contributing guidelines](.github/contributing.md).

### License

This software is provided to you with terms stated in the MIT License. Read the full text in the `LICENSE` file located at the root of this repository.

**[MIT License](https://opensource.org/licenses/MIT) | Copyright (c) 2023 Mungai Njoroge**
