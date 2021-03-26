@echo off

rem IDENTIFICA EL EQUIPO
if exist D:\Devel\ (
    set DEVEL=D:\Devel
) else (
    set DEVEL=%USERPROFILE%\Devel
)


@cmd /K %DEVEL%\consola_config_g3.9.2