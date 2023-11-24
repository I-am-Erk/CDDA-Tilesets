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

## Python and Windows

If you dont have Python istalled yet you need to disable app execution alias.  
<details>
   <summary>Go to -> "start" and type "Manage App Execution Aliases". Go to it and turn off "Python"</summary>

![img](https://i.stack.imgur.com/7C78e.png)
   
</details>

Make sure you are not using the Python version from the Microsoft Store. This version is incompatible with the tileset composing tools. You can uninstall this version safely from your system. The tools from the repo will install Python 3.12 for you, which you can use for any purpose.

## Tilesets and Windows

Some tilesets reuse assets from other tilesets. This can be done by using symlinks, which are shortcuts that point to another file or folder. However, symlinks are disabled by default in Windows systems. If you want to compose tilesets that use symlinks (such as Altica or Ultica-ISO), you need to enable them.

To enable symlinks, go to the `tools` folder in your local repository and double-click on `git_symlinks.cmd`. This will run a script that will configure your Git settings to allow symlinks. [^2]

<!--
## Install requirements

**Python**

Install Python 3 from [python.org](https://www.python.org/downloads/windows/).

During installation, check "Add Python to PATH".

**libvips**

Download the latest libvips distribution from [libvips.github.io](https://libvips.github.io/libvips/install.html)
(get vips-dev-w64-web-#.#.#.zip NOT vips-dev-w64-all-#.#.#.zip).

Extract the files somewhere.

## Setting up paths

For composing tilesets, some path must be known to the respective scripts.
This section describes the most easy drag & drop approach.

In `CDDA-Tilesets`, go into folder `tools`.

1. Copy `set_game_path.cmd` into the game's folder, and double-click it.  
OR: Drag & drop the game folder onto `set_game_path.cmd`.
   > Note: This sets the environmental variable `CDDA_PATH`.

2. Copy `set_vips_path.cmd` into the vips folder (e.g. `C:\vips-dev-x.xx`), and double-click it.  
OR: Drag & drop the vips folder onto `set_vips_path.cmd`.
   > Note: This sets the environmental variable `LIBVIPS_PATH`.

3. Optional: To set a tileset to compose permanently, double-click `set_tileset.cmd` and select the desired tileset.  
If not set permanently, the update script will allow for interactive selection of a tileset.
   > Note: This sets the environmental variable `CDDA_TILESET`.

After these steps, it might be necessary to restart the computer.

## Compose and update tileset

In `tools`, double-click `updtset.cmd`.

You will be prompted to select a tileset (unless it was set permanently).
At the first run, `pyvips` will be installed automatically.
-->

If something goes wrong, read the script's output carefully!
[^1]: Some tasks can be done much faster and easier with command line actually. So you can try to run ```winget install Github.GitHubDesktop```
[^2]: That tool will guide you how to [enable symlinks](https://blogs.windows.com/windowsdeveloper/2016/12/02/symlinks-windows-10/) in your system and turn them on for your local repository.
