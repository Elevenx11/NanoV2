@echo off
chcp 65001
title نانو المحسّن - النظام الذكي

echo.
echo ================================
echo    🤖 نانو المحسّن v2.0 🤖
echo ================================
echo.
echo يتم تشغيل النظام المطور الجديد...
echo.

echo 📦 فحص المتطلبات...
python -c "import flask, requests, selenium" 2>nul
if errorlevel 1 (
    echo ⚠️  بعض المتطلبات غير مثبتة!
    echo 💡 تثبيت المتطلبات الآن...
    pip install -r requirements_enhanced.txt
    echo.
)

echo ✅ المتطلبات جاهزة!
echo.

echo 🚀 بدء تشغيل نانو المحسّن...
echo.
echo 🌐 الواجهة ستكون متاحة على: http://localhost:5000
echo 💬 جرب الأوامر الجديدة مثل:
echo    - "قول ميو نهاية كل جملة"
echo    - "كن واثق مع الرجال وخفيف مع البنات"
echo    - "سوي حساب انستقرام"
echo.

python enhanced_nano_app.py

echo.
echo 👋 تم إيقاف نانو المحسّن
pause