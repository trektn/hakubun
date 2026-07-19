Hakubun (博聞)
==============

![Hakubun](assets/header.png)

Hakubun aims to be a lightweight and simple but feature-rich program for Unix based systems
for fetching, updating and using data from personal lists hosted in several media tracking websites.

The name Hakubun comes from a Japanese 4-character idiom 博聞強記, meaning "being widely read and having a highly retentive memory"

Hakubun is an independent fork of [Trackma](https://github.com/z411/trackma), extended with
additional features. See [Relationship to upstream](#relationship-to-upstream) below.

See [Hakubun+](https://github.com/trektn/hakubun-plus) for even more features, there's another repo because I thought Hakubun was already out of scope for an anime tracker.

Features
--------

- Manage local list and synchronize when necessary, useful when offline
- Manage multiple accounts on different media tracking sites
- Support for several media types (as supported by the site)
- Multiple user interfaces (Qt, GTK, command-line)
- Detection of running media player, updates list if necessary
- Ability to launch media player for a requested media in the list and update list if necessary
- Highly scalable, easy to code new interfaces and support for other sites
- Secure, uses HTTPS wherever possible
- Optional Kitsu GraphQL backend for faster, batched list downloads
- Undo and redo for progress, score, status, and tag changes (GTK and Qt)
- GTK list filtering, drag-and-drop status moves, and additional list columns (Season, Type, Platform Score)
- Qt toolbar actions, "Move to status" menu, and improved show-detail layout

Which tracker should I use?
--------
There isn't a single "best" tracker. Each has different goals and strengths.

| Project | Choose it if... |
|---------|-----------------|
| [**Taiga**](https://github.com/erengy/taiga) | You primarily use **Windows**, and/or **torrent anime**, or prefer its built-in search. |
| [**Hakubun**](https://github.com/trektn/hakubun) | You use ***nix** and wanted **Trackma** with a more opinionated UI/UX, or you use **Kitsu** and want GraphQL support. |
| [**Trackma**](https://github.com/z411/trackma) | You prefer a **CLI-first** workflow, are building wrappers or automation around it, or simply want to support the original project and its maintainers. |
| [**Hakubun+**](https://github.com/trektn/hakubun-plus) | The same as Hakubun but you also want features not available elsewhere, such as the **airing schedule** or **MAL score** additions. It should work across platforms, including Windows, but Windows is not tested. Expect it to be less stable than all of these other options on *nix or Windows. |

### Quick recommendations

- **Windows user?** → **Taiga**
- **Linux or want a more modern Trackma experience?** → **Hakubun**
- **Need a CLI or scripting interface?** → **Trackma**
- **Want experimental or extra features?** → **Hakubun+**

Currently supported websites
----------------------------

- [Anilist](https://anilist.co/) (Anime, Manga)
- [Kitsu](https://kitsu.app/) (Anime, Manga)
- [MyAnimeList](https://myanimelist.net/) (Anime, Manga)
- [Shikimori](https://shikimori.io/) (Anime, Manga)
- [VNDB](https://vndb.org/) (VNs)

Dependencies
------------

The only required dependencies to run Hakubun are:

- Python 3.9+
- For installation: `python-pip` (to install through `pip`) *or* `python-uv` (to install through `uv`)

But only basic features will work (only CLI interface and no tracker). Everything else is optional.

The following user interfaces are available and their requirements are as follows:

| UI | Dependencies |
| --- | --- |
| Qt | PyQt6 (`python-pyqt6`) |
| GTK 3 | PyGI (`python-gi` and `python-cairo`) |
| CLI | None |

The following media recognition trackers are available and their requirements are as follows:

| Tracker | Description | Dependencies |
| --- | --- | --- |
| inotify | Instant, but only supported in Linux. Uses it whenever possible. | `inotify` *or* `pyinotify` |
| Polling | Slow, but supported in every POSIX platform. Fallback. | `lsof` |
| Plex | Connects to Plex server. Enabled manually. | None |
| Kodi | Connects to Kodi server. Enabled manually. | None |
| Jellyfin | Connects to Jellyfin server. Enabled manually. | None |
| MPRIS | Connects to running MPRIS capable media players. | `python-jeepney` |
| Win32 | Recognition for Windows platforms. | None |

Additional optional Python dependencies:

- PIL (`python-pil`) - for showing preview images in the Qt/GTK interfaces.
- pypresence (???) - for announcing activity on Discord.
- anitopy (-) - for the anitopy title parser

Installation
------------

An AUR package is planned but not yet available. Until then, install from source:

```sh
$ git clone https://github.com/trektn/hakubun.git
$ cd hakubun
$ uv build
$ pip3 install dist/hakubun-*-py3-none-any.whl
```

Or install the git version directly:

```sh
$ pip3 install -U git+https://github.com/trektn/hakubun.git
```

### Extras (User Interfaces)

All user interfaces except for the default CLI mode require additional dependencies to function.
You may specify these as "extras" to be installed by the Python package manager.

The following extras are available:

| Extra | Description |
| --- | --- |
| `gtk` | The GTK interface. |
| `qt` | The Qt interface. |
| `ui` | All user interfaces. |
| `trackers` | All tracker libraries. |
| `discord_rpc` | Set your watching activity in Discord. |

If you want to install any of the extras be sure to specify them during installation:

#### pip

```sh
# With pip
$ pip3 install hakubun[gtk,trackers]
$ pip3 install hakubun[ui,discord_rpc]
```

Note that pip does not have a way to install all available extras,
so you'll have to provide them all manually if desired.

Then you can run the program with the interface you like.

```sh
$ hakubun
$ hakubun-gtk
$ hakubun-qt
```

#### uv

When using uv on the cloned repository (see above),
you can install your desired extras as follows:

```sh
$ uv sync --extra gtk --extra trackers
$ uv sync --extra ui --extra discord_rpc
$ uv sync --all-extras
```

Then you can run the interface you like in your virtual environment managed by uv:

```sh
$ uv run hakubun
$ uv run hakubun-gtk
$ uv run hakubun-qt
```

Configuration
-------------

A configuration file will be created in `~/.config/hakubun/config.json`, make sure to fill in the
directory where you store your video files and other settings.

Alternatively, the GTK and Qt interfaces provide a visual Settings panel.

If you are migrating from Trackma, you can transfer all your settings in `~/.config/trackma/` to `~/.config/hakubun/` and this usually shouldn't be a problem. However I recommend only transferring your account logins in `~/.config/trackma/accounts.dict`

Development
-----------

The code is hosted as a git repository on [GitHub](https://github.com/trektn/hakubun).

Clone the repo and create the virtual environment using `uv`:

```sh
$ git clone https://github.com/trektn/hakubun.git
$ cd hakubun
$ uv sync --all-extras
```

Use the above commands from the [uv](#uv) section for how to run your desired interface.

Relationship to upstream
-------------------------

This is an independent fork of [Trackma](https://github.com/z411/trackma) and is not affiliated
with or endorsed by the original project.

This fork was developed using AI assistance. Upstream Trackma does not accept AI-assisted
contributions on their own. Please respect upstream's contribution policy and do not submit
patches from this fork upstream unless they have been independently reviewed and comply with
that policy.

Branding
--------

Hakubun uses a hanko (Japanese seal) as its primary visual identity. The `assets/` directory
contains logos and headers. The hanko serves as the desktop application icon.

Maintenance expectations
-------------------------

This fork is provided as-is. I may make occasional updates, but I do not plan to provide
long-term maintenance or guaranteed support.

License
-------

Hakubun is licensed under the GPLv3 license, please see [LICENSE](../COPYING) for details.

Authors
-------

Hakubun is a fork of Trackma, originally written by z411 <z411@omaera.org>. For other upstream
contributors see the AUTHORS file.
