@echo off
title FTL Laporan - Public Online Tunnel (localhost.run)
echo ========================================================
echo       FOR THE LITTLE INDONESIA - ONLINE TUNNEL
echo ========================================================
echo.
echo  Menghubungkan ke localhost.run...
echo  Link publik (https://xxxxxx.app.lhr.life) akan muncul di bawah:
echo.
echo ========================================================
ssh -o StrictHostKeyChecking=no -R 80:localhost:80 nokey@localhost.run
pause
