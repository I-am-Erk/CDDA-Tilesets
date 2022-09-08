@echo off

set path_arg=

:next_arg
if not "%1"=="" (
    if /i [%1] EQU [/t] (
        set is_temp=YES
    ) else (
        set path_arg=%1
    )
    shift
    goto :next_arg
)

if /i [%path_arg%] EQU [] (
:: Retrieve User input
set /p path_arg="Game directory: "
)

if not exist %path_arg% (
    echo ERROR: Directory "%path_arg%" does not exist! && goto stop
)

if not exist "!path_arg!\gfx" (
    echo ERROR: Directory "%path_arg%" is not a valid CDDA game directory! && goto stop
)

if /i [%is_temp%] EQU [YES] (
    echo Setting cdda path temporarily
    SET CDDA_PATH=%path_arg%
) else (
    echo Setting cdda path permanently, reboot required
    SETX CDDA_PATH %path_arg%
)

exit /b 0
:stop
echo:
echo (press any key to close this window)
pause >nul
exit /b 1
