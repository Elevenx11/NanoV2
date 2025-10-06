@echo off
chcp 65001 >nul
title نانو - النظام المتكامل

echo.
echo ========================================
echo 🤖 مرحباً بك في نانو - النظام المتكامل
echo ========================================
echo.

:menu
echo اختر ما تريد تشغيله:
echo.
echo 1. 🎛️  لوحة التحكم الرئيسية (الواجهة الكاملة)
echo 2. 👤  نظام الأوامر العليا (سطر الأوامر)
echo 3. 🏗️  إنشاء الحسابات التلقائي
echo 4. 💬  تشغيل نانو العادي (للمحادثة)
echo 5. 📊  عرض إحصائيات النظام
echo 6. 🔧  تثبيت المتطلبات
echo 7. 🧹  تنظيف وصيانة النظام
echo 8. ❌  خروج
echo.

set /p choice="أدخل اختيارك (1-8): "

if "%choice%"=="1" goto control_panel
if "%choice%"=="2" goto admin_commands
if "%choice%"=="3" goto account_creator
if "%choice%"=="4" goto normal_nano
if "%choice%"=="5" goto show_stats
if "%choice%"=="6" goto install_requirements
if "%choice%"=="7" goto maintenance
if "%choice%"=="8" goto exit

echo خيار غير صحيح. حاول مرة أخرى.
timeout /t 2 >nul
goto menu

:control_panel
echo.
echo 🎛️ بدء تشغيل لوحة التحكم الرئيسية...
echo ستفتح الواجهة في المتصفح على العنوان: http://localhost:5000
echo.
python nano_control_panel.py
pause
goto menu

:admin_commands
echo.
echo 👤 بدء نظام الأوامر العليا...
echo يمكنك الآن إعطاء أوامر مباشرة لنانو
echo.
python -c "from core.admin_commands import NanoAdminCommands; admin = NanoAdminCommands(); exec(open('core/admin_commands.py').read().split('if __name__ == \"__main__\":')[1])"
pause
goto menu

:account_creator
echo.
echo 🏗️ بدء نظام إنشاء الحسابات...
echo سيقوم نانو بفحص قائمة الحسابات وإنشاؤها تلقائياً
echo.
python -c "import asyncio; from core.auto_account_creator import main; asyncio.run(main())"
pause
goto menu

:normal_nano
echo.
echo 💬 بدء تشغيل نانو العادي للمحادثة...
echo.
if exist "nano_main.py" (
    python nano_main.py
) else if exist "nano_digital_life_app.py" (
    python nano_digital_life_app.py
) else (
    echo ❌ لم يتم العثور على ملف نانو الأساسي
    echo تأكد من وجود nano_main.py أو nano_digital_life_app.py
)
pause
goto menu

:show_stats
echo.
echo 📊 عرض إحصائيات النظام...
echo.
python -c "
from core.admin_commands import NanoAdminCommands
from core.auto_account_creator import NanoAutoAccountCreator
import json

print('🤖 إحصائيات نانو')
print('=' * 40)

admin = NanoAdminCommands()
creator = NanoAutoAccountCreator()

settings = admin.get_current_settings()
status = creator.get_account_status()

print(f'الشخصية الحالية: {settings[\"personality\"][\"name\"]}')
print(f'مستوى الفكاهة: {settings[\"personality\"][\"humor_level\"]}/10')
print(f'مستوى العناد: {settings[\"personality\"][\"stubbornness_level\"]}/10')
print()
print(f'إجمالي الحسابات: {status[\"total_accounts\"]}')
print(f'الحسابات المعلقة: {status[\"pending_queue\"]}')
print()
print('الحسابات حسب المنصة:')
for platform, count in status['platforms'].items():
    print(f'  {platform}: {count}')
print()

history = admin.get_command_history(5)
if history:
    print('آخر الأوامر:')
    for cmd in history[-3:]:
        print(f'  {cmd[\"command\"]}: {cmd[\"result\"][:30]}...')
"
echo.
pause
goto menu

:install_requirements
echo.
echo 🔧 تثبيت المتطلبات...
echo.

echo تحديث pip...
python -m pip install --upgrade pip

echo تثبيت المتطلبات الأساسية...
pip install flask
pip install selenium
pip install aiohttp
pip install requests
pip install pathlib

echo تثبيت المتطلبات الإضافية...
if exist "requirements.txt" (
    pip install -r requirements.txt
) else (
    echo إنشاء ملف requirements.txt...
    echo flask > requirements.txt
    echo selenium >> requirements.txt
    echo aiohttp >> requirements.txt
    echo requests >> requirements.txt
    echo pathlib >> requirements.txt
    echo beautifulsoup4 >> requirements.txt
    echo lxml >> requirements.txt
    pip install -r requirements.txt
)

echo.
echo ✅ تم تثبيت المتطلبات بنجاح!
echo.
pause
goto menu

:maintenance
echo.
echo 🧹 بدء تنظيف وصيانة النظام...
echo.

echo تنظيف الملفات المؤقتة...
if exist "__pycache__" rmdir /s /q "__pycache__"
if exist "core\__pycache__" rmdir /s /q "core\__pycache__"

echo فحص سلامة ملفات البيانات...
python -c "
import json
from pathlib import Path

data_files = [
    'data/nano_personality_config.json',
    'data/nano_accounts.json', 
    'data/nano_behavior_settings.json'
]

for file_path in data_files:
    try:
        if Path(file_path).exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            print(f'✅ {file_path} سليم')
        else:
            print(f'⚠️ {file_path} غير موجود (سيتم إنشاؤه عند الحاجة)')
    except Exception as e:
        print(f'❌ خطأ في {file_path}: {str(e)}')
"

echo إنشاء نسخة احتياطية من البيانات...
set backup_date=%date:~-4,4%-%date:~-10,2%-%date:~-7,2%
if not exist "backups" mkdir backups
if exist "data" (
    xcopy "data" "backups\backup_%backup_date%" /E /I /Y >nul
    echo ✅ تم إنشاء نسخة احتياطية في: backups\backup_%backup_date%
)

echo.
echo ✅ تم تنظيف النظام بنجاح!
echo.
pause
goto menu

:exit
echo.
echo 👋 شكراً لاستخدام نانو!
echo المطور: فريق نانو
echo.
timeout /t 2 >nul
exit

REM إضافة معالج الأخطاء
:error
echo.
echo ❌ حدث خطأ أثناء التنفيذ!
echo تأكد من:
echo 1. تثبيت Python بشكل صحيح
echo 2. تثبيت جميع المتطلبات
echo 3. وجود الملفات الضرورية
echo.
pause
goto menu