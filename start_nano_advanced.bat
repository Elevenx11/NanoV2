@echo off
chcp 65001 >nul
color 0A

echo.
echo ================================================================
echo          🤖 نانو المتقدم - Nano Advanced AI System 🤖
echo          مع نظام المشاعر والوحدات المتكاملة
echo ================================================================
echo.
echo 🇸🇦 مطور بالهجة السعودية الرياضية الأصيلة
echo 💡 يحتوي على 1292+ جملة وعبارة 
echo 🧠 نظام ذكاء متقدم مع 10 أنواع مشاعر
echo ⚙️  4 وحدات نشطة (عربي، إنجليزي، رسم، شخصية)
echo.
echo ================================================================
echo                    خيارات التشغيل
echo ================================================================
echo.
echo 1. تشغيل نانو المتقدم (الواجهة الكاملة)
echo 2. تدريب متقدم جديد 
echo 3. جمع محادثات جديدة
echo 4. اختبار سريع للنظام
echo 5. عرض إحصائيات نانو
echo.
set /p choice="اختر الرقم المناسب (1-5): "

if "%choice%"=="1" goto start_advanced
if "%choice%"=="2" goto advanced_training  
if "%choice%"=="3" goto collect_conversations
if "%choice%"=="4" goto quick_test
if "%choice%"=="5" goto show_stats
goto invalid_choice

:start_advanced
echo.
echo 🚀 بدء تشغيل نانو المتقدم...
echo ⚡ تحميل نظام المشاعر والوحدات...
echo 🌐 الواجهة ستكون متاحة على: http://127.0.0.1:5000
echo.
echo ⏰ انتظر قليلاً حتى يكتمل التحميل...
echo.
python app_v2.py
goto end

:advanced_training
echo.
echo 🎓 بدء التدريب المتقدم لنانو...
echo 📚 سيتم تحسين الذكاء والمنطقية...
echo.
python advanced_training_system.py
goto end

:collect_conversations  
echo.
echo 📱 جمع محادثات جديدة من وسائل التواصل...
echo 🔄 معالجة وتنظيف النصوص...
echo.
python social_media_collector.py
goto end

:quick_test
echo.
echo ⚡ اختبار سريع لنظام نانو المتكامل...
echo 🧪 فحص المشاعر والوحدات...
echo.
python nano_core.py
goto end

:show_stats
echo.
echo 📊 إحصائيات نانو المتقدم
echo ===============================
python -c "
import json
try:
    with open('corpus.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        count = len(data['sentences'])
    print(f'📝 إجمالي الجمل: {count}')
    print(f'🧠 مستوى الذكاء: متقدم')  
    print(f'💖 نظام المشاعر: نشط (10 أنواع)')
    print(f'⚙️  الوحدات النشطة: 4')
    print(f'🇸🇦 اللهجة: رياضية أصيلة')
    print(f'⭐ الجودة: عالية الذكاء')
except:
    print('❌ خطأ في قراءة الإحصائيات')
"
echo.
pause
goto menu

:invalid_choice
echo.
echo ❌ اختيار غير صحيح، حاول مرة أخرى
timeout /t 2 >nul
goto menu

:end
echo.
echo ================================================================
echo              🎉 انتهى التشغيل - Nano Completed 🎉  
echo ================================================================
echo.
echo 💡 نصائح:
echo - للتدريب المستمر: شغل الخيار 2 بانتظام
echo - لأفضل أداء: استخدم الواجهة المتقدمة (الخيار 1)
echo - لتحديث النصوص: استخدم الخيار 3
echo.
echo 🙏 شكراً لاستخدام نانو المتقدم!
echo.
pause