@echo off

SET Dir=%~dp0

regsvr32.exe "%Dir%SKCOM.dll"
regsvr32.exe "%Dir%PolarisB2BAPI.dll"