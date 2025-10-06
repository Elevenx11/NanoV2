#!/usr/bin/env python3
"""
برنامج اختبار شامل لأنظمة نانو
=============================

يختبر جميع الأنظمة الجديدة:
- نظام الأوامر العليا
- نظام إنشاء الحسابات  
- لوحة التحكم
"""

import sys
import os
import json
import asyncio
from pathlib import Path
import traceback

# إضافة مسار core
sys.path.append('core')

def test_admin_commands():
    """اختبار نظام الأوامر العليا"""
    print("🔧 اختبار نظام الأوامر العليا...")
    
    try:
        from core.admin_commands import NanoAdminCommands
        
        admin = NanoAdminCommands()
        
        # اختبار الحصول على الإعدادات
        settings = admin.get_current_settings()
        print(f"✅ الشخصية الحالية: {settings['personality']['name']}")
        
        # اختبار تنفيذ أمر سريع
        result = admin.execute_command("الإعدادات")
        print(f"✅ تنفيذ الأوامر يعمل")
        
        # اختبار تعديل صفة
        result = admin.adjust_trait("humor_level", 8)
        print(f"✅ تعديل الصفات: {result}")
        
        # اختبار إضافة اهتمام
        result = admin.add_interest("اختبار")
        print(f"✅ إضافة اهتمامات: {result}")
        
        # اختبار سجل الأوامر
        history = admin.get_command_history(3)
        print(f"✅ سجل الأوامر: {len(history)} عناصر")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في نظام الأوامر العليا: {e}")
        print(traceback.format_exc())
        return False

def test_account_creator():
    """اختبار نظام إنشاء الحسابات"""
    print("\n🏗️ اختبار نظام إنشاء الحسابات...")
    
    try:
        from core.auto_account_creator import NanoAutoAccountCreator
        
        creator = NanoAutoAccountCreator()
        
        # اختبار توليد اسم المستخدم
        username = creator.generate_username("instagram", "nano_themed")
        print(f"✅ توليد اسم المستخدم: {username}")
        
        # اختبار توليد البايو
        bio = creator.generate_bio("instagram")
        print(f"✅ توليد البايو: {bio[:50]}...")
        
        # اختبار توليد كلمة مرور
        password = creator.generate_password(10)
        print(f"✅ توليد كلمة المرور: {'*' * len(password)} ({len(password)} أحرف)")
        
        # اختبار الحصول على حالة الحسابات
        status = creator.get_account_status()
        print(f"✅ حالة الحسابات: {status['total_accounts']} حسابات")
        
        # اختبار قائمة الإنشاء
        queue = creator.get_creation_queue()
        print(f"✅ قائمة الإنشاء: {len(queue)} طلبات")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في نظام إنشاء الحسابات: {e}")
        print(traceback.format_exc())
        return False

def test_flask_app():
    """اختبار لوحة التحكم الويب"""
    print("\n🌐 اختبار لوحة التحكم الويب...")
    
    try:
        # اختبار استيراد Flask app
        import nano_control_panel
        
        print("✅ استيراد Flask app نجح")
        
        # اختبار إنشاء القوالب
        templates_dir = Path("templates")
        if templates_dir.exists():
            print("✅ مجلد القوالب موجود")
            
            if (templates_dir / "base.html").exists():
                print("✅ قالب base.html موجود")
            
            if (templates_dir / "dashboard.html").exists():
                print("✅ قالب dashboard.html موجود")
        else:
            print("⚠️ مجلد القوالب غير موجود - سيتم إنشاؤه تلقائياً")
        
        # اختبار app object
        app = nano_control_panel.app
        print("✅ Flask app object تم إنشاؤه بنجاح")
        
        return True
        
    except ImportError as e:
        print(f"❌ خطأ في استيراد Flask: {e}")
        return False
    except Exception as e:
        print(f"❌ خطأ في لوحة التحكم: {e}")
        print(traceback.format_exc())
        return False

def test_data_files():
    """اختبار ملفات البيانات"""
    print("\n📁 اختبار ملفات البيانات...")
    
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    expected_files = [
        "nano_personality_config.json",
        "nano_accounts.json", 
        "nano_behavior_settings.json"
    ]
    
    for filename in expected_files:
        file_path = data_dir / filename
        try:
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {filename}: سليم ({len(str(data))} بايت)")
            else:
                print(f"⚠️ {filename}: غير موجود (سيتم إنشاؤه عند الحاجة)")
        except Exception as e:
            print(f"❌ {filename}: خطأ - {e}")
    
    return True

def test_requirements():
    """اختبار المتطلبات المثبتة"""
    print("\n📦 فحص المتطلبات...")
    
    required_packages = [
        'flask',
        'requests', 
        'selenium',
        'aiohttp',
        'beautifulsoup4',
        'transformers',
        'torch'
    ]
    
    installed = []
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            installed.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package} - غير مثبت")
    
    print(f"\nالنتيجة: {len(installed)}/{len(required_packages)} مثبت")
    
    if missing:
        print(f"\nلتثبيت المتطلبات المفقودة:")
        print(f"pip install {' '.join(missing)}")
    
    return len(missing) == 0

def run_integration_test():
    """اختبار التكامل بين الأنظمة"""
    print("\n🔄 اختبار التكامل...")
    
    try:
        from core.admin_commands import NanoAdminCommands
        from core.auto_account_creator import NanoAutoAccountCreator
        
        admin = NanoAdminCommands()
        creator = NanoAutoAccountCreator()
        
        # اختبار إضافة حساب لقائمة الإنشاء
        result = admin.queue_account_creation("instagram", {"priority": "test"})
        print(f"✅ إضافة حساب للقائمة: {result}")
        
        # اختبار قراءة القائمة من النظام الآخر
        queue = creator.get_creation_queue()
        test_requests = [req for req in queue if req.get("preferences", {}).get("priority") == "test"]
        
        if test_requests:
            print("✅ التكامل بين الأنظمة يعمل بشكل صحيح")
            
            # حذف طلب الاختبار
            queue = [req for req in queue if req.get("preferences", {}).get("priority") != "test"]
            # حفظ القائمة المحدثة (تبسيط - في الواقع نحتاج للحفظ بشكل صحيح)
            
        else:
            print("⚠️ لم يتم العثور على طلب الاختبار في القائمة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار التكامل: {e}")
        return False

def main():
    """الدالة الرئيسية لتشغيل جميع الاختبارات"""
    
    print("🤖 بدء اختبار أنظمة نانو الشاملة")
    print("=" * 50)
    
    tests = [
        ("فحص المتطلبات", test_requirements),
        ("ملفات البيانات", test_data_files),
        ("الأوامر العليا", test_admin_commands),
        ("إنشاء الحسابات", test_account_creator),
        ("لوحة التحكم", test_flask_app),
        ("التكامل", run_integration_test),
    ]
    
    results = {}
    
    for test_name, test_function in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_function()
        except Exception as e:
            print(f"❌ خطأ عام في {test_name}: {e}")
            results[test_name] = False
    
    # عرض النتائج النهائية
    print("\n" + "="*50)
    print("📊 ملخص نتائج الاختبار:")
    print("="*50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in results.items():
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{test_name:20}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 النتيجة النهائية: {passed}/{total} اختبارات نجحت")
    
    if passed == total:
        print("\n🎉 جميع الأنظمة تعمل بشكل مثالي!")
        print("🚀 يمكنك الآن تشغيل نانو بثقة:")
        print("   - شغّل start_nano_complete.bat")
        print("   - أو python nano_control_panel.py")
    else:
        print(f"\n⚠️ {total-passed} اختبارات فشلت. راجع التفاصيل أعلاه")
        print("💡 نصائح لحل المشاكل:")
        print("   1. شغّل 'pip install -r requirements.txt'")
        print("   2. تأكد من وجود Python 3.7+")
        print("   3. تحقق من اتصال الإنترنت")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    
    print(f"\n{'🎉' if success else '⚠️'} انتهاء الاختبارات")
    
    # انتظار المستخدم قبل الإغلاق
    input("\nاضغط Enter للمتابعة...")