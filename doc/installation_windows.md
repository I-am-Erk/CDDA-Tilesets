# Windows guide

Guide for Windows users, without touching the Command Line.

## First steps

1. [Register](https://github.com/join) on GitHub
2. [Get](https://docs.github.com/en/enterprise-cloud@latest/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop#downloading-and-installing-github-desktop) `Github Desktop` [^1]
3. [Fork](https://docs.github.com/en/get-started/quickstart/fork-a-repo) Tileset repository
4. [Clone](https://docs.github.com/en/desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop) forked repository.

> [!NOTE]
> It is a good practice to create new branch at the start. Name it "playground" for example.
> Your repo is your own private space. You can do whatever you want in it without affecting the original project. However, if you want to contribute to the project, you need to follow some guidelines. One of them is to keep your master branch clean and empty, and do your work in a separate branch. This will make it easier for you to sync your changes with the upstream repo and create pull requests.

Now you have source files on your drive and some tools as well.
These tools will help you managing multitile objects, setting up the environment and composing tilesets.

## The Game

The easiest way to get the game is to use the [CDDA Game Launcher](https://github.com/Fris0uman/CDDA-Game-Launcher/releases).
With the launcher, install the latest **experimental** release.

Tools need to know where to put composed tileset. So you have three options:
- copy `set_game_path.cmd` to your game dir and double-click it.
- drag and drop game folder over `set_game_path.cmd` script.
- or just double-click it and type path to the game folder.

> [!NOTE]
> if you change your game folder later, you can repeat this step and provide new path.

## Tilesets and Windows

Some tilesets reuse assets from other tilesets. This can be done by using symlinks, which are shortcuts that point to another file or folder. However, symlinks are disabled by default in Windows systems. If you want to compose tilesets that use symlinks (such as Altica or Ultica-ISO), you need to enable them.

To enable symlinks, go to the `tools` folder in your local repository and double-click on `git_symlinks.cmd`. This will run a script that will configure your Git settings to allow symlinks. [^2]

## Python and Windows

If you dont have Python istalled yet you need to disable app execution alias.
<details>
   <summary>Go to -> "start" and type "Manage App Execution Aliases". Go to it and turn off "Python"</summary>

![img](https://i.stack.imgur.com/7C78e.png)

</details>

Make sure you are not using the Python version from the Microsoft Store. This version is incompatible with the tileset composing tools. You can uninstall this version safely from your system. The tools from the repo will install Python 3.12 for you, which you can use for any purpose.

Open the `tools` folder in your local repository and double-click `updtset.cmd`
Select any common tileset (like MShockXotto+) for the first runs until it finally compose.
At the first run script will try to install Python using `winget`. In case of successful install it would stop and ask you to relaunch it again.

> [!WARNING]
> If script failed to install Python you should do it manually from [python.org](https://www.python.org/downloads/windows/).
> During installation, check "Add Python to PATH".

## Python and components

The script will first check if Python is installed on your system. It will print the Python version and verify that the pyvips module and the libvips library are available.

- If pyvips is missing, the script will try to install it automatically. This step should not cause any errors, only informational messages.
- Next, the script will check if there are any libvips binaries in the system. If not, the script will attempt to download the 8.15 version and unzip it using VBS into the user’s home folder. Then, the script will call set_vips_path.cmd with this path.

If the script successfully adds libvips, it will stop and ask the user to run it again.

> [!WARNING]
> If script failed to install libvips you should do it manually.
> Download the latest libvips distribution from [libvips.github.io](https://libvips.github.io/libvips/install.html)
> get vips-dev-w64-web-#.#.#.zip NOT vips-dev-w64-all-#.#.#.zip
> extract files somewhere and drag and drop this folder on `set_vips_path.cmd`

## Final

Maximum at third run script should compose tileset and propose you to check it in game.
If something goes wrong, read the script's output carefully!

> [!TIP]
> You may ask for help at tileset Discord server.

> [!TIP]
> To set a tileset to compose permanently, double-click `set_tileset.cmd` and select the desired tileset.
> If not set permanently, the update script will allow for interactive selection of a tileset.
> Note: This sets the environmental variable `CDDA_TILESET`. Delete it if you want to select tileset again.

> [!TIP]
> When scripts ask you to restart your computer it may be necessary on some systems. But you can try and skip reboots.

[^1]: Some tasks can be done much faster and easier with command line actually. So you can try to run ```winget install Github.GitHubDesktop```

[^2]: That tool will guide you how to [enable symlinks](https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/) in your system and turn them on for your local repository.
