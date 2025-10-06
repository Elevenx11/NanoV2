@echo off
chcp 65001 > nul
echo ==============================================
echo     🤖 نانو الجديد - المساعد الذكي المطوّر
echo ==============================================
echo.
echo 📋 اختر طريقة التشغيل:
echo.
echo [1] 💬 وضع المحادثة المباشرة (Console)
echo [2] 🌐 وضع الويب (Web Interface) 
echo [3] 🎓 نظام التدريب المتطور
echo [4] ⚙️  تشغيل تفاعلي (اختيار تلقائي)
echo [5] ❌ خروج
echo.
set /p choice="اختيارك (1-5): "

if "%choice%"=="1" (
    echo.
    echo 🚀 تشغيل نانو في وضع المحادثة المباشرة...
    echo 💡 استخدم الأوامر: حالة، حفظ، إعادة، خروج
    echo.
    python nano_main.py console
    pause
) else if "%choice%"=="2" (
    echo.
    echo 🌐 تشغيل نانو في وضع الويب...
    echo 🔗 سيفتح على: http://127.0.0.1:5000
    echo.
    start http://127.0.0.1:5000
    python nano_main.py web
    pause
) else if "%choice%"=="3" (
    echo.
    echo 🎓 تشغيل نظام التدريب المتطور...
    echo 🎯 سيتم تدريب نانو ليصبح أكثر طبيعية وذكاءً
    echo.
    cd training
    python advanced_trainer.py
    cd ..
    pause
) else if "%choice%"=="4" (
    echo.
    echo ⚙️ تشغيل نانو في الوضع التفاعلي...
    echo.
    python nano_main.py
    pause
) else if "%choice%"=="5" (
    echo.
    echo 👋 شكراً لاستخدامك نانو!
    timeout /t 2 >nul
    exit
) else (
    echo.
    echo ❌ اختيار غير صحيح! الرجاء اختيار رقم من 1-5
    timeout /t 2 >nul
    goto start
)

:start
start_nano_new.bat