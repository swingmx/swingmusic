# Swing Music Contributing Guide

Hi! We're really excited that you are interested in contributing to Swing Music. This project uses Python, [Flask](https://flask.palletsprojects.com/en/2.3.x/), Sqlite, [Poetry](https://python-poetry.org/), and [Vue](https://vuejs.org/).

If you are interested in making a code contribution take a moment to read through the following guidelines:

- [Code of Conduct](./CODE_OF_CONDUCT.md)
- [Pull Request Guidelines](#pull-request-guidelines)

## Pull Request Guidelines

- Checkout a topic branch from the relevant branch, e.g. `master`, and merge back against that branch.

- If adding a new feature:

  - Provide a convincing reason to add this feature. Ideally, you should open a suggestion issue first and have it approved before working on it.

- If fixing bug:

  - Provide a detailed description of the bug in the PR.

## Development Setup

This project is broken down into 2 parts. The server (this repo) and the client (which lives [here](https://github.com/swing-opensource/swingmusic-client)).

To contribute to the server development, you need to install [Poetry package manager](https://python-poetry.org/docs).

Fork this repo, git clone and install the dependencies:

```sh
git clone https://github.com/swing-opensource/swingmusic.git

# or with ssh

git clone git@github.com:swing-opensource/swingmusic.git

cd swingmusic

poetry install
```

You need a LastFM API key which you can get on the [API accounts page](https://www.last.fm/api/accounts). Then set it as an environment variable under the name: `LASTFM_API_KEY`.

Finally, run the server. You can use a different port if you have another Swing Music instance running on port `1970`.

```sh
poetry run python manage.py --port 1980
```

After that, checkout into a new branch and make your changes.

```sh
git checkout <branch_name>
```

Finally, commit your changes and open a pull request.

## Contributing to the client

You need to have [yarn](https://yarnpkg.com/) installed in your machine. See their [install guide](https://yarnpkg.com/getting-started/install).

Fork the repo, git clone and install the dependencies:

```sh
git clone https://github.com/swing-opensource/swingmusic-client.git

# or with ssh

git clone git@github.com:swing-opensource/swingmusic-client.git

cd swingmusic-client

yarn install
```

You can now run the client.

```sh
yarn dev
```

You can see the client at http://localhost:5173.

> The client is hardcoded to hook into the server on port `1980` (to allow the another server instance to be running on the default port). You can follow the instructions above to set up the server in that port, or you can change the port in `swingmusic-client/config.ts`. Don't forget to change it back when in the PR.

## Where can I go for help?

If you need help, you can email me at: geoffreymungai45@gmail.com

## What does the Code of Conduct mean for me?

Our Code of Conduct means that you are responsible for treating everyone on the project with respect and courtesy regardless of their identity. If you are the victim of any inappropriate behavior or comments as described in our Code of Conduct, we are here for you and will do the best to ensure that the abuser is reprimanded appropriately, per our code.

See you around?