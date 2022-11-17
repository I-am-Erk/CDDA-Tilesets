@echo off
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: This script sets the environmental variable CDDA_TILESET to either:
:: - the first positional argument or
:: - a path entered by the user upon prompt
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
set tileset_arg=

set is_temp=NO
set allow_clear=YES
set silent=NO

:next_arg
if not "%1"=="" (
    if /i [%1] EQU [/t] (
        set is_temp=YES
    ) else if /i [%1] EQU [/c] (
        set allow_clear=NO
    ) else if /i [%1] EQU [/s] (
        set silent=YES
    ) else (
        set tileset_arg=%1
    )
    shift
    goto :next_arg
)

if /i [%is_temp%] NEQ [YES] (
    setlocal EnableDelayedExpansion
)

if /i [%tileset_arg%] NEQ [] (
    goto :skip_interactive
)

set count=0

:: Read in files
for /d %%x in (..\gfx\*.*) do (
    set /a count=count+1
    set choice[!count!]=%%~nx
)

if /i [%allow_clear%] EQU [YES] (
    set /a count=count+1
    set choice[!count!]=Clear-tileset-settings
)

echo.
echo Select one:
echo.

:: Print list of files
for /l %%x in (1,1,!count!) do (
    echo %%x] !choice[%%x]!
)
echo.

:: Retrieve User input
set /p select=?
echo.
set tileset_arg=!choice[%select%]!

:skip_interactive
if /i [%tileset_arg%] EQU [Clear-tileset-settings] (
    if /i [%is_temp%] EQU [YES] (
        echo Clearing temporary tileset settings
        SET CDDA_TILESET=
    ) else (
        echo Clearing permanent tileset settings, reboot required
        SETX CDDA_TILESET ""
        REG delete HKCU\Environment /F /V CDDA_TILESET || echo Error removing env var CDDA_TILESET && goto stop
    )
) else (
    if /i [%tileset_arg%] EQU [] (
        echo ERROR: Invalid tileset selection! && goto stop
    )
    :: Check for correct tileset name
    if not exist "..\gfx\%tileset_arg%" (
        echo ERROR: Tileset "%tileset_arg%" does not exist! && goto stop
    )
    echo Selected tileset %tileset_arg%

    if /i [%is_temp%] EQU [YES] (
        echo Setting tileset to %tileset_arg% temporarily
        SET CDDA_TILESET=%tileset_arg%
    ) else (
        echo Setting tileset to %tileset_arg% permanently
        echo Reboot required
        SETX CDDA_TILESET %tileset_arg%
    )
)

if /i [%silent%] NEQ [YES] (
    echo (press any key to close this window^)
    pause >nul
)

exit /b 0

:stop
echo.

if /i [%silent%] NEQ [YES] (
    echo (press any key to close this window^)
    pause >nul
)

exit /b 1
