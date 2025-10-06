@echo off
chcp 65001 > nul
cls
title نانو المحسّن - تشغيل آمن

echo.
echo    ╔══════════════════════════════╗
echo    ║      🤖 نانو المحسّن 🤖      ║
echo    ║       النسخة الآمنة         ║
echo    ╚══════════════════════════════╝
echo.

echo 🔧 بدء تحضير النظام...
echo.

echo 📍 المجلد الحالي: %CD%
echo 🐍 فحص Python...

python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت! 
    echo 💡 يرجى تثبيت Python من: https://python.org
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo.

echo 🚀 تشغيل نانو المحسّن...
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

python run_nano_simple.py

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo 👋 تم إيقاف نانو
echo 💡 اضغط أي مفتاح للإغلاق...
pause > nul