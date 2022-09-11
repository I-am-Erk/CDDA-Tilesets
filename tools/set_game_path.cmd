@echo off
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: This script sets the environmental variable CDDA_PATH to either:
:: - the first positional argument or
::   (also supports drag & drop ofthe game folder ontothe script file)
:: - the current working directory it it is a valid CDDA game directory or
:: - a path entered by the user upon prompt
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set path_arg=
set is_temp=NO
set silent=NO

:next_arg
if not "%1"=="" (
    if /i [%1] EQU [/t] (
        set is_temp=YES
    ) else if /i [%1] EQU [/s] (
        set silent=YES
    ) else (
        set path_arg=%1
    )
    shift
    goto :next_arg
)

if /i [%is_temp%] NEQ [YES] (
    setlocal EnableDelayedExpansion
)

if /i [%path_arg%] NEQ [] (
    goto :skip_interactive
)

if exist "%CD%\gfx" (
    if exist "%CD%\cataclysm-tiles.exe" (
        echo Detected CDDA game directory at %CD%
        set path_arg=%CD%&& goto :skip_interactive
    )
)

:: Retrieve User input
set /p path_arg="Game directory: "

:skip_interactive

:: Make path absolute
for %%x in ("%path_arg%") do (
    set path_arg=%%~fx
)

if not exist "%path_arg%" (
    echo ERROR: Directory "%path_arg%" does not exist! && goto stop
)

if not exist "%path_arg%\gfx" (
    echo ERROR: Directory "%path_arg%" is not a valid CDDA game directory! && goto stop
)
if not exist "%path_arg%\cataclysm-tiles.exe" (
    echo ERROR: Directory "%path_arg%" is not a valid CDDA game directory! && goto stop
)

if /i [%is_temp%] EQU [YES] (
    echo Setting cdda path to "%path_arg%", temporarily
    SET CDDA_PATH=%path_arg%
) else (
    echo Setting cdda path "%path_arg%", permanently
    echo Reboot required
    SETX CDDA_PATH %path_arg%
)

exit /b 0
:stop
echo.

if /i [%silent%] NEQ [YES] (
    echo (press any key to close this window^)
    pause >nul
)

exit /b 1
