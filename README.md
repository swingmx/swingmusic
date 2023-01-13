![SWING MUSIC PLAYER BANNER IMAGE](./rd-me-banner.png)

---

### Make listening to your local music fun again.

`Swing` is a music player for local audio files that is built with both visual coolness and functionality in mind. Just run the app and enjoy your music library in a web browser.

> Note: This project is in the early stages of development. Many features are missing but will be added with time.

The app is currently only available on linux. (I don't have access to a Windows machine for building and testing purposes and my machine is not strong enough to support Windows in VM).

### Setup

Download the latest release from the [release page](#) and extract it in your machine. Then execute the extracted file in a terminal.

```bash
./swing
```

The file will start the app at <http://localhost:1970> by default. See the setup option section on how to change the host and port.

### Setup options

```
Usage: swing [options]

Options:
    --host: Set the host
    --port: Set the port
    --help, -h: Show this help message
    --version, -v: Show the version
```

### Development

This project is broken down into 2. The client and the server. The client comprises of the user interface code. This part is written in Typescript, Vue 3 and SCSS. To setup the client, checkout the [swing client repo ](#) on GitHub.

The second part of this project is the server. This is the main part of the app that runs on your machine, interacts with audio files and send data to the client. It's written in Python 3.

The following instructions will guide you on how to setup the **server**.

---

The project uses [Python poetry](https://python-poetry.org) as the dependency manager. Follow the instructions in [their docs](https://python-poetry.org/docs/) to install it in your machine.

> It is assumed that you have `Python 3.10` or newer installed in your machine. This project uses duck typing features so older version of Python will not work. If you don't have Python installed in your machine, get it from the [python website](https://www.python.org/downloads/).

Clone this repo locally in your machine. Then install the project dependencies and start the app.

```sh
git clone <$>

cd swing-core

# install dependencies using poetry
poetry install

# start the app
poetry run python manage.py
```

### Contributing

If you want to contribute to this project, feel free to open an issue or a pull request on Github. Your contributions are highly valued and appreciated. Feature suggestions, bug reports and code contribution are welcome.

### License

This software is provided to you with terms stated in the MIT License. Read the full text in the `LICENSE` file located at the root of this repository.

### A brain dump ...

I started working on this project on dec 2021. Why? I like listening and exploring music and I like it more when I can enjoy it (like really really). I'd been searching for cute music players for linux that allow me to manage my ever growing music library. Some of the main features I was looking for were:

- A simple, lively and beautiful user interface (main reason)
- Creating automated daily mixes based on my listening activity.
- Ability to move files around without breaking my playlists and mixes.
- Something that can bring together all the audio files scattered all over my disks into a single place.
- Browsing related artists and albums.
- Reading artists and albums biographies.
- Web browser based user interface.
- a lot more ... but I can't remember them at the moment

I've been working to make sure that most (if not all) of the features listed above are built. Some of them are done, but most are not even touched yet. A lot of work is needed and I know that it will take a lot of time to build and perfect them.

I've been keeping a small 🤥 list of a few cool features that I'd like to see implemented in the project. You can check it out in [this notion page](https://rhetorical-othnielia-565.notion.site/Cool-features-1a0cd5b797904da687bec441e7c7aa19). https://rhetorical-othnielia-565.notion.site/Cool-features-1a0cd5b797904da687bec441e7c7aa19

I have been working on this project solo, so it’s very hard to push things fast. The app is written in Python for the backend and Vue3 for the client. If you have knowledge in any or both of this areas, feel free to contribute to the project. We’ll be excited to have you. Your help is highly appreciated.

_The backend is basically a bunch of Python classes and functions. The client just sends API request and displays it._

---

**[MIT License](https://opensource.org/licenses/MIT) | Copyright (c) 2023 Mungai Njoroge**
