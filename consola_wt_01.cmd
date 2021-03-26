@echo off

set CURDIR=%CD%

start	wt -p "Pwsh 7.1 (conda 3.9.2)" -d %CURDIR%; split-pane -p "Pwsh 7.1 (conda 3.9.2)" -d %CURDIR%