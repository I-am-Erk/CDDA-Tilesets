@echo off
setlocal EnableDelayedExpansion
setlocal EnableExtensions
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::ver 1.13 / 2022-06-29::::
:: This script does the following:
:: - compose tilesets from source
:: - put composed tileset into some folder for future use
:: - copy said composed tileset from the folder into the game so you can try in on the fly
:: - copy layering json file from tileset source into the game
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: 1. Set path to your local copy of the tileset repository

set tileset_fork=".."

::
:: 2. Set correct tileset folder name (e.g. UltimateCataclysm)

set def_tileset=""

::
:: 3. Set path to compose.py file

set script_dir="."
:: For use of compose.py script from the game directory:
:: set script_dir="CDDA_PATH\tools\gfx_tools"

::
:: 4. Set path to CDDA game folder

set the_game_dir=""

::
:: 5. OPTIONAL, Set path to the folder where to put the composed tileset (for future examination)

set composed_dir="compiled_tilesets\"

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
set direct_update=YES
set separate_composed=NO
set tileset_arg=

:next_arg
set curarg=%1
set curarg1=!curarg:~0,1!

if /i [!curarg1!] EQU [/] (
    if /i [!curarg!] EQU [/q] (
        set verbose=NO
    ) else if /i [!curarg!] EQU [/d] (
        set direct_update=NO
    ) else if /i [!curarg!] EQU [/s] (
        set separate_composed=YES
    ) else (
        :usage
        echo Compose tileset and update game with it
        echo.
        echo %0 [/q] [/d] [/s] [tileset]
        echo.
        echo   /q         Quiet mode - do not print additional info. Just main steps
        echo   /d         inDirect update - will use "composed_dir" variable path and just then update the game.
        echo   /s         Separate forder for composed tilesets - in case of using "composed_dir" variable
        echo              will create separate folder with corresponding name for composed tileset,
        echo              then update the game.
        echo   tileset    Should be the same as foldername in tileset repository.
        echo.
        echo   When used without any key will use variables set in the top part of the %0 script.
        echo   Alternatively, use an environmental variable: set CDDA_PATH="C:\Program Files\Cataclysm-DDA"
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
if /i [!verbose!] EQU [YES] (echo    WARNING^^^! Tileset cant be composed with Python installed from Microsoft Store! )
if /i [!verbose!] EQU [YES] (echo.)

:overwrite_with_env_var
if /i [!CDDA_PATH!] NEQ [] (
    SET the_game_dir=%CDDA_PATH:"=%
)
if /i [!CDDA_TILESET!] NEQ [] (
    SET def_tileset=%CDDA_TILESET:"=%
)

:interactive_game_path
if /i [!the_game_dir!] EQU [] (
    echo No game directory specified
    echo To set the game directory permanently, run set_game_path.cmd
    echo Setting the game directory temporarily...
    CALL set_game_path.cmd /t /s || echo Error setting game directory && goto stop
    SET the_game_dir=!CDDA_PATH:"=!
)

:interactive_tileset
if /i [!tileset_arg!] EQU [] (
    if /i [!def_tileset!] EQU [] (
        echo No tileset specified
        echo To set the tileset permanently, run set_tileset.cmd
        echo Alternatively, run this script with the tileset name as argument
        echo Setting the tileset temporarily...
        CALL set_tileset.cmd /t /c /s || echo Error setting tileset && goto stop
        SET tileset_arg=!CDDA_TILESET:"=!
    )
)

echo 1. Check if folders are correct.
if /i [!tileset_arg!] EQU [] (
    set tileset_name=!def_tileset!
) else (
    set tileset_name=!tileset_arg!
)
if /i [!verbose!] EQU [YES] (echo    - Will use [!tileset_name!] as tileset name.)

if not exist "%tileset_fork%\gfx\" (
    echo ERROR: Check tileset source dir! && goto stop
) else (
    if not exist "%tileset_fork%\gfx\%tileset_name%\tile_info.json" (echo ERROR: Check tileset name. Must be one of these:&& dir "%tileset_fork%\gfx\" /AD /B && goto stop)
)
if /i [!verbose!] EQU [YES] (echo    - CDDA-Tileset fork with source tiles found.)

set script_path=%script_dir:CDDA_PATH=!the_game_dir!%\compose.py

if not exist "%script_path%" (echo ERROR: Cannot find compose.py file! && goto stop)
if /i [!verbose!] EQU [YES] (echo    - Python 'compose.py' script found under !script_path! folder.)

if /i [!direct_update!] EQU [YES] (
    set path_to_compose=!the_game_dir!\gfx\!tileset_name!
) else (
    if /i [!separate_composed!] EQU [YES] (
        set path_to_compose=%composed_dir%\%tileset_name%
        if not exist "!path_to_compose!" ( mkdir "!path_to_compose!" )
    ) else (
        set path_to_compose=%composed_dir%
    )
)
if not exist "%path_to_compose%" (echo ERROR: Check folder "%path_to_compose%" for composed tileset! && goto stop)
if /i [!verbose!] EQU [YES] (echo    - Composed tileset will be put to [!path_to_compose!])
if /i [!verbose!] EQU [YES] (
    if /i [!direct_update!] EQU [NO] (
        if /i [!separate_composed!] EQU [NO] (
            echo    - No separate folder will be created!
        )
    )
)

if not exist "%the_game_dir%\cataclysm-tiles.exe" (echo ERROR: Cannot find the game! && goto stop)
if /i [!verbose!] EQU [YES] (echo    - Cataclysm game executable found.)
if /i [!verbose!] EQU [YES] (echo.)


echo 2. Check if python available.
if /i [!verbose!] EQU [YES] (echo    - IMPORTANT: If any error apears at this stage please refer following page first.)
if /i [!verbose!] EQU [YES] (echo      https://github.com/CleverRaven/Cataclysm-DDA/blob/master/doc/TILESET.md#pyvips )
where py.exe /q
if errorlevel 1 (
    where python3.exe /q
    if errorlevel 1 (
        where python.exe /q
        if errorlevel 1 (
            echo ERROR: No Python found!
            echo If you are sure that Python is installed - please check 'path' environment variable.
            echo Script will try to install Python 3.10, try to run this script again after this.
            echo.
            winget install Python.Python.3.10 --disable-interactivity
            goto stop
        ) else (
            set APP=python
        )
    ) else (
        set APP=python3
    )
) else (
    set APP=py
)

if /i [!verbose!] EQU [YES] (echo    - %APP% found.)
%APP% --version

pip install --upgrade pip --no-color 1>nul

pip show pyvips --no-color 1>nul
if errorlevel 1 (
    if /i [!verbose!] EQU [YES] (echo    - NO python 'pyvips' module found. Will try to install it.)
    %APP% -m pip install --user pyvips --no-color >nul
    if errorlevel 1 (
        echo    - Python 'pyvips' failed to install. && goto stop
    )
    if /i [!verbose!] EQU [YES] (echo    - Python 'pyvips' installed.)
) else (
    if /i [!verbose!] EQU [YES] (echo    - Python 'pyvips' module found.)
)

pip show numpy --no-color 1>nul
if errorlevel 1 (
    if /i [!verbose!] EQU [YES] (echo    - NO python 'numpy' module found. Will try to install it.)
    %APP% -m pip install numpy --no-color >nul
    if errorlevel 1 (
        echo    - Python 'numpy' failed to install. && goto stop
    )
    if /i [!verbose!] EQU [YES] (echo    - Python 'numpy' installed.)
) else (
    if /i [!verbose!] EQU [YES] (echo    - Python 'numpy' module found.)
)

where /q %LIBVIPS_PATH%\bin:vips.exe
if errorlevel 1 (
    echo ERROR^^^! No 'libvips' library found. Please refer installation manual:
    echo https://libvips.github.io/libvips/install.html
    echo If you are sure that library was installed - please check library version and 'path' environment variable.
    echo Script will try to download libvips 8.15 into your home directory, try to run this script again after this.
    echo.
    curl https://github.com/libvips/build-win64-mxe/releases/download/v8.15.0/vips-dev-w64-web-8.15.0.zip -L -o %HOMEDRIVE%%HOMEPATH%\vips-dev-w64-web-8.15.0.zip

    call :UnZipFile "%HOMEDRIVE%%HOMEPATH%\vips" "%HOMEDRIVE%%HOMEPATH%\vips-dev-w64-web-8.15.0.zip"
    call set_vips_path.cmd %HOMEDRIVE%%HOMEPATH%\vips\vips-dev-8.15\
    goto stop
) else (
    if /i [!verbose!] EQU [YES] (echo    - Library 'libvips' found.)
)
if /i [!verbose!] EQU [YES] (echo.)

echo 3. Lets compose %tileset_name%. Be patient it takes some time.
pushd "!path_to_compose!" || goto :deleted
rd /q /s . 2> NUL
popd
:deleted
%APP% "%script_path%" --use-all "%tileset_fork%\gfx\%tileset_name%" "!path_to_compose!"
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
        xcopy "%tileset_fork%\gfx\%tileset_name%\fallback*.*" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
        xcopy "%tileset_fork%\gfx\%tileset_name%\tileset.txt" "%the_game_dir%\gfx\%tileset_name%" /Y /Q 1>nul
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

echo.
echo (press any key to close this window^)
pause >nul
exit /b 1

:UnZipFile <ExtractTo> <newzipfile>
set vbs="%temp%\_.vbs"
if exist %vbs% del /f /q %vbs%
>%vbs%  echo Set fso = CreateObject("Scripting.FileSystemObject")
>>%vbs% echo If NOT fso.FolderExists(%1) Then
>>%vbs% echo fso.CreateFolder(%1)
>>%vbs% echo End If
>>%vbs% echo set objShell = CreateObject("Shell.Application")
>>%vbs% echo set FilesInZip=objShell.NameSpace(%2).items
>>%vbs% echo objShell.NameSpace(%1).CopyHere(FilesInZip)
>>%vbs% echo Set fso = Nothing
>>%vbs% echo Set objShell = Nothing
cscript //nologo %vbs%
if exist %vbs% del /f /q %vbs%
