@echo off

SET Dir=%~dp0

regsvr32.exe /u "%Dir%SKCOM.dll"
regsvr32.exe /u "%Dir%PolarisB2BAPI.dll"