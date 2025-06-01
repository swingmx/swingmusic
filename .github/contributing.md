# Swing Music Contributing Guide

Hi! We're really excited that you are interested in contributing to Swing Music. This project uses Python, [Flask](https://flask.palletsprojects.com/en/2.3.x/), Sqlite, [uv](https://docs.astral.sh/uv), and [Vue](https://vuejs.org/).

If you are interested in making a code contribution take a moment to read through the following guidelines:

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Pull Request Guidelines](#pull-request-guidelines)

## Pull Request Guidelines

- Checkout a topic branch from the relevant branch, e.g. `master`, and merge back against that branch.

- If adding a new feature:

  - Provide a convincing reason to add this feature. Ideally, you should open a suggestion issue first and have it approved before working on it.

- If fixing a bug:

  - Provide a detailed description of the bug in the PR.

## Development Setup

This project is broken down into 2 parts. The server (this repo) and the client (which lives [here](https://github.com/swing-opensource/swingmusic-client)).

To contribute to the server development, you need to install [uv package manager](https://docs.astral.sh/uv).

Fork this repo, git clone and install the dependencies:

```sh
git clone https://github.com/swing-opensource/swingmusic.git

# or with ssh

git clone git@github.com:swing-opensource/swingmusic.git

cd swingmusic
uv sync
```

Finally install the wsgi module for the server. If you are on Windows, simply install `waitress`:

```sh
uv add waitress
```

If you are on Unix, you will need to install `bjoern`. The package requires the `libev` module to be installed on your machine:

```sh
# Arch Linux
pacman -S libev

# Fedora, CentOS
dnf install libev-devel

# MacOS
brew install libev
```

Finally:

```sh
uv add bjoern
```

Finally, run the server for development on port 1980.

```sh
uv run python -m swingmusic --port 1980
```

After that, checkout into a new branch and make your changes.

```sh
git checkout <branch_name>
```

After testing your changes, commit your changes and open a pull request.

## Contributing to the client

You need to have [yarn](https://yarnpkg.com) installed in your machine. Please check out the [install guide](https://yarnpkg.com/getting-started/install).

Fork the repo, git clone and install the dependencies:

```sh
git clone https://github.com/swing-opensource/swingmusic-client.git

# or with ssh

git clone git@github.com:swing-opensource/swingmusic-client.git

cd swingmusic-client
yarn install
```

You can now run the client in development mode.

```sh
yarn dev
```

You can see the client at http://localhost:5173.

> [!TIP]
> The client is configured to hook into the development server running on port `1980` (to allow the another server instance to be running on the default port).

## Where can I go for help?

If you need help, you can find users and contributors on [Swing Music Community](https://t.me/+9n61PFcgKhozZDE0) Telegram chat.

## What does the Code of Conduct mean for me?

Our Code of Conduct means that you are responsible for treating everyone on the project with respect and courtesy regardless of their identity. If you are the victim of any inappropriate behavior or comments as described in our Code of Conduct, we are here for you and will do the best to ensure that the abuser is reprimanded appropriately, per our code.

See you around?