@echo off
setlocal EnableDelayedExpansion
setlocal EnableExtensions
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::ver 1.13 / 2022-06-29::::
:: this script does the following:
:: - compose tilesets from source
:: - put composed tileset into some folder for future use
:: - copy said composed tileset from the folder into the game so you can try in on the fly
:: - copy layering json file from tileset source into the game
::
:: PLEASE setup 5 variables below, put correct text between quotes
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: 1. Set path to your local copy of the tileset repository

set tileset_fork="T:\cdda-tilesets"

::
:: 2. Set correct tileset folder name (e.g. UltimateCataclysm)

set def_tileset="UltimateCataclysm"

::
:: 3. Set path to compose.py file 

set script_dir="T:\workshop"

::
:: 4. Set path to the folder where to put the composed tileset (for future examination)

set composed_dir="T:\workshop\compiled"

::
:: 5. Set path to CDDA game folder

set the_game_dir="T:\cataclysm"

::
:: all set, you're done! just doubleclick on this file.
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:removing_quotes
SET tileset_fork=%tileset_fork:"=%
SET def_tileset=%def_tileset:"=%
SET script_dir=%script_dir:"=%
SET composed_dir=%composed_dir:"=%
SET the_game_dir=%the_game_dir:"=%

:parse_command_line
set verbose=YES
set direct_update=NO
set separate_composed=NO
set tileset_arg=

:next_arg
set curarg=%1
set curarg1=!curarg:~0,1!

if /i [!curarg1!] EQU [/] (
	if /i [!curarg!] EQU [/q] (
		set verbose=NO
	) else if /i [!curarg!] EQU [/d] (
		set direct_update=YES
	) else if /i [!curarg!] EQU [/s] (
		set separate_composed=YES
	) else (
		:usage
		echo Compose tileset and update game with it
		echo.
		echo %0 [/q] [/d] [/s] [tileset]
		echo.
		echo   /q         Quiet mode - do not print additional info. Just main steps
		echo   /d         Direct update - will put composed tileset direclty into the game.
		echo              Without this key will use "composed_dir" variable path and just then update the game.
		echo   /s         Separate forder for composed tilesets - in case of using "composed_dir" variable 
		echo              will create separate folder with corresponding name for composed tileset,
		echo              then update the game.
		echo   tileset    Should be the same as foldername in tileset repository.
		echo.
		echo   When used without any key will use variables set in the top part of the %0 script.
		exit /b 255
	)
	shift /1
	goto next_arg
) else (
	if /i [!curarg!] EQU [] ( goto continue ) else ( set tileset_arg=!curarg!&& shift /1 && goto next_arg )
)
:continue
if /i [!verbose!] EQU [YES] (echo.)
if /i [!verbose!] EQU [YES] (echo    For advanced use please run %0 /?)
if /i [!verbose!] EQU [YES] (echo.)

echo 1. Check if folders are correct.
if /i [!tileset_arg!] EQU [] (
	set tileset_name=!def_tileset!
) else (
	set tileset_name=!tileset_arg!
)
if /i [!verbose!] EQU [YES] (echo    - Will use [!tileset_name!] as tileset name.)
if not exist "%tileset_fork%\gfx\" (
	echo ERROR: Check tileset source dir! && goto stop)
) else (
	if not exist "%tileset_fork%\gfx\%tileset_name%\tile_info.json" (echo ERROR: Check tileset name. Must be one of these:&& dir "%tileset_fork%\gfx\" /AD /B && goto stop )
)
if /i [!verbose!] EQU [YES] (echo    - CDDA-Tileset fork with source tiles found.)
if not exist "%script_dir%\compose.py" (echo ERROR: Cannot find compose.py file! && goto stop)
if /i [!verbose!] EQU [YES] (echo    - Python 'compose.py' script found in [!script_dir!] folder.)
if not exist "%composed_dir%" (echo ERROR: Check folder for composed tileset! && goto stop)
if /i [!separate_composed!] EQU [YES] (
	set path_to_compose=%composed_dir%\%tileset_name%
	if not exist "!path_to_compose!" ( mkdir "!path_to_compose!" )
) else (
	set path_to_compose=%composed_dir%
)
if not exist "%the_game_dir%\cataclysm-tiles.exe" (echo ERROR: Cannot find the game! && goto stop)
if /i [!direct_update!] EQU [YES] (
	set path_to_compose=!the_game_dir!\gfx\!tileset_name!
)
if /i [!verbose!] EQU [YES] (echo    - Composed tileset will be put to [!path_to_compose!])
if /i [!verbose!] EQU [YES] (
	if /i [!separate_composed!] EQU [NO] (
		echo    - No separate folder will be created!
	) else (
		if /i [!direct_update!] EQU [YES] (	echo    x No need to provide both /d and /s keys. Direct update always update correct tileset.)
	)
)
if /i [!verbose!] EQU [YES] (echo    - Cataclysm game executable found.)
if /i [!verbose!] EQU [YES] (echo.)


echo 2. Check if python available.
if /i [!verbose!] EQU [YES] (echo    - IMPORTANT: If any error apears at this stage please refer following page first.)
if /i [!verbose!] EQU [YES] (echo      https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/TILESET.md#pyvips )
py --version > nul
if errorlevel 1 (
	echo ERROR: No Python found!
	echo If you are sure that Python is installed - please check 'path' environment variable.
	goto stop
)
if /i [!verbose!] EQU [YES] (echo    - Python found.)
pip show pyvips --no-color 1>nul 
if errorlevel 1 (
	if /i [!verbose!] EQU [YES] (echo    - NO python 'pyvips' module found. Will try to install it.)
	py -m pip install --user pyvips --no-color >nul
	if errorlevel 1 (
		echo    - Python 'pyvips' failed to install. && goto stop
	)
	if /i [!verbose!] EQU [YES] (echo    - Python 'pyvips' installed.)
) else (
	if /i [!verbose!] EQU [YES] (echo    - Python 'pyvips' module found.)
)
vips -v 1>nul
if errorlevel 1 (
	echo ERROR! No 'libvips' library found. Please refer installation manual:
	echo https://libvips.github.io/libvips/install.html 
	echo If you are sure that library was installed - please check library version and 'path' environment variable.
	goto stop
) else (
	if /i [!verbose!] EQU [YES] (echo    - Library 'libvips' found.)
)
if /i [!verbose!] EQU [YES] (echo.)

echo 3. Lets compose %tileset_name%. Be patient it takes some time.
if /i [!direct_update!] EQU [YES] (
	rd /q /s "%temp%\cdda_tset_compose"
	mkdir "%temp%\cdda_tset_compose"
	xcopy "%the_game_dir%\gfx\%tileset_name%\fallback*.*" "%temp%\cdda_tset_compose" /Y /Q 1>nul
	xcopy "%the_game_dir%\gfx\%tileset_name%\tileset.txt" "%temp%\cdda_tset_compose" /Y /Q 1>nul
	if /i [!verbose!] EQU [YES] (echo    - Essential tileset files backed up to [%temp%\cdda_tset_compose].)
)
pushd "!path_to_compose!" || goto :deleted
rd /q /s . 2> NUL
popd
:deleted
py.exe "%script_dir%\compose.py" --use-all "%tileset_fork%\gfx\%tileset_name%" "!path_to_compose!"
if not errorlevel 1 (
	if /i [!verbose!] EQU [YES] (echo.)

	echo 4. Now composed tileset will be copied into the game so you can refresh it.
	if /i [!direct_update!] EQU [NO] (
		xcopy "!path_to_compose!\*.*" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
		if errorlevel 1 goto stop
		if /i [!verbose!] EQU [YES] (echo    - All files are available both in)
		if /i [!verbose!] EQU [YES] (echo      - [!path_to_compose!] and in)
		if /i [!verbose!] EQU [YES] (echo      - [%the_game_dir%\gfx\%tileset_name%])
		if /i [!verbose!] EQU [YES] (echo.)
	) else (
		xcopy "%temp%\cdda_tset_compose\fallback*.*" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
		xcopy "%temp%\cdda_tset_compose\tileset.txt" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
		if /i [!verbose!] EQU [YES] (echo    - Essential tileset files restored.)
		if /i [!verbose!] EQU [YES] (echo.)
	)
	
	echo 5. If there any layering info it'll be copied too.
	if exist "%tileset_fork%\gfx\%tileset_name%\layering.json" (
		xcopy "%tileset_fork%\gfx\%tileset_name%\layering.json" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
		if errorlevel 1 goto stop
		if /i [!verbose!] EQU [YES] (echo    - Additional 'layering.json' file copied)
		if /i [!verbose!] EQU [YES] (echo      - from [%tileset_fork%\gfx\%tileset_name%])
		if /i [!verbose!] EQU [YES] (echo      -   to [%the_game_dir%\gfx\%tileset_name%])
	)
	if /i [!verbose!] EQU [YES] (echo.)
	
	echo.
	echo     All done... Refresh tileset in game. 
) else (
	echo ERROR: Something went wrong! && goto stop
)
timeout /t 10 >nul
exit /b 0
:stop
echo:
echo (press any key to close this window)
pause >nul
exit /b 1
