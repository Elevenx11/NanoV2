"""
لوحة التحكم الرئيسية لنانو
==========================

واجهة ويب شاملة للتحكم في:
- شخصية نانو والأوامر العليا
- إنشاء وإدارة الحسابات
- مراقبة النشاط والحالة
- إدارة المحتوى والنشر
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import json
import asyncio
import threading
from datetime import datetime, timedelta
from pathlib import Path
import logging

# استيراد الأنظمة المحلية
import sys
sys.path.append('core')

from core.admin_commands import NanoAdminCommands
from core.auto_account_creator import NanoAutoAccountCreator
from core.nano_chat_engine import NanoChatEngine

# إعداد التسجيل
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# إنشاء التطبيق
app = Flask(__name__)
app.secret_key = "nano_control_panel_secret_key_2024"

# تهيئة الأنظمة
admin_commands = NanoAdminCommands()
account_creator = NanoAutoAccountCreator()
chat_engine = NanoChatEngine()

# ======== الصفحات الرئيسية ========

@app.route('/')
def dashboard():
    """لوحة التحكم الرئيسية"""
    try:
        # جمع بيانات الحالة العامة
        admin_settings = admin_commands.get_current_settings()
        account_status = account_creator.get_account_status()
        command_history = admin_commands.get_command_history(5)
        chat_history = chat_engine.get_recent_chat(5)
        
        dashboard_data = {
            "current_personality": admin_settings["personality"]["name"],
            "humor_level": admin_settings["personality"]["humor_level"],
            "stubbornness_level": admin_settings["personality"]["stubbornness_level"],
            "total_accounts": account_status["total_accounts"],
            "pending_accounts": account_status["pending_queue"],
            "recent_commands": command_history,
            "platform_accounts": account_status["platforms"],
            "chat_messages_count": len(chat_history),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return render_template('dashboard.html', data=dashboard_data)
    
    except Exception as e:
        logger.error(f"خطأ في لوحة التحكم: {str(e)}")
        return f"خطأ في تحميل لوحة التحكم: {str(e)}", 500

@app.route('/personality')
def personality_control():
    """صفحة التحكم في الشخصية"""
    try:
        settings = admin_commands.get_current_settings()
        personalities = admin_commands.personality_config["personalities"]
        
        return render_template('personality.html', 
                             current=settings["personality"],
                             personalities=personalities)
    
    except Exception as e:
        logger.error(f"خطأ في صفحة الشخصية: {str(e)}")
        return f"خطأ: {str(e)}", 500

@app.route('/accounts')
def accounts_management():
    """صفحة إدارة الحسابات"""
    try:
        account_status = account_creator.get_account_status()
        creation_queue = account_creator.get_creation_queue()
        
        return render_template('accounts.html',
                             status=account_status,
                             queue=creation_queue)
    
    except Exception as e:
        logger.error(f"خطأ في صفحة الحسابات: {str(e)}")
        return f"خطأ: {str(e)}", 500

@app.route('/commands')
def command_center():
    """مركز الأوامر العليا"""
    try:
        command_history = admin_commands.get_command_history(20)
        
        return render_template('commands.html',
                             history=command_history)
    
    except Exception as e:
        logger.error(f"خطأ في مركز الأوامر: {str(e)}")
        return f"خطأ: {str(e)}", 500

# ======== APIs للتفاعل ========

@app.route('/api/execute_command', methods=['POST'])
def execute_command():
    """تنفيذ أمر عليا"""
    try:
        command_text = request.json.get('command', '').strip()
        
        if not command_text:
            return jsonify({"status": "error", "message": "الأمر فارغ"})
        
        result = admin_commands.execute_command(command_text)
        
        return jsonify({
            "status": "success",
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"خطأ في تنفيذ الأمر: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/change_personality', methods=['POST'])
def change_personality():
    """تغيير شخصية نانو"""
    try:
        personality_name = request.json.get('personality')
        
        if not personality_name:
            return jsonify({"status": "error", "message": "اسم الشخصية مطلوب"})
        
        result = admin_commands.change_personality(personality_name)
        
        return jsonify({
            "status": "success",
            "message": result,
            "new_personality": personality_name
        })
    
    except Exception as e:
        logger.error(f"خطأ في تغيير الشخصية: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/adjust_trait', methods=['POST'])
def adjust_trait():
    """تعديل صفة في الشخصية"""
    try:
        trait = request.json.get('trait')
        level = int(request.json.get('level', 5))
        
        if not trait:
            return jsonify({"status": "error", "message": "اسم الصفة مطلوب"})
        
        result = admin_commands.adjust_trait(trait, level)
        
        return jsonify({
            "status": "success",
            "message": result,
            "trait": trait,
            "new_level": level
        })
    
    except Exception as e:
        logger.error(f"خطأ في تعديل الصفة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/queue_account', methods=['POST'])
def queue_account_creation():
    """إضافة حساب لقائمة الإنشاء"""
    try:
        platform = request.json.get('platform')
        preferences = request.json.get('preferences', {})
        
        if not platform:
            return jsonify({"status": "error", "message": "المنصة مطلوبة"})
        
        result = admin_commands.queue_account_creation(platform, preferences)
        
        return jsonify({
            "status": "success",
            "message": result,
            "platform": platform
        })
    
    except Exception as e:
        logger.error(f"خطأ في إضافة الحساب للقائمة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/create_account_now', methods=['POST'])
def create_account_immediately():
    """إنشاء حساب فوراً"""
    try:
        platform = request.json.get('platform')
        preferences = request.json.get('preferences', {})
        
        if not platform:
            return jsonify({"status": "error", "message": "المنصة مطلوبة"})
        
        # تشغيل إنشاء الحساب في خيط منفصل
        def create_account_async():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            result = loop.run_until_complete(
                account_creator.create_account_auto(platform, preferences)
            )
            loop.close()
            return result
        
        # تنفيذ في الخلفية
        thread = threading.Thread(target=create_account_async)
        thread.start()
        
        return jsonify({
            "status": "started",
            "message": f"بدأ إنشاء حساب {platform}... يرجى المتابعة في صفحة الحسابات",
            "platform": platform
        })
    
    except Exception as e:
        logger.error(f"خطأ في إنشاء الحساب: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/get_status', methods=['GET'])
def get_current_status():
    """الحصول على الحالة الحالية"""
    try:
        admin_settings = admin_commands.get_current_settings()
        account_status = account_creator.get_account_status()
        
        return jsonify({
            "personality": admin_settings["personality"],
            "accounts": account_status,
            "behavior": admin_settings["behavior"],
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"خطأ في جلب الحالة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/update_bio', methods=['POST'])
def update_bio():
    """تحديث البايو"""
    try:
        new_bio = request.json.get('bio', '').strip()
        
        if not new_bio:
            return jsonify({"status": "error", "message": "البايو فارغ"})
        
        result = admin_commands.update_bio(new_bio)
        
        return jsonify({
            "status": "success",
            "message": result,
            "new_bio": new_bio
        })
    
    except Exception as e:
        logger.error(f"خطأ في تحديث البايو: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/add_interest', methods=['POST'])
def add_interest():
    """إضافة اهتمام جديد"""
    try:
        interest = request.json.get('interest', '').strip()
        
        if not interest:
            return jsonify({"status": "error", "message": "الاهتمام فارغ"})
        
        result = admin_commands.add_interest(interest)
        
        return jsonify({
            "status": "success",
            "message": result,
            "interest": interest
        })
    
    except Exception as e:
        logger.error(f"خطأ في إضافة الاهتمام: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/chat', methods=['POST'])
def chat_with_nano():
    """المحادثة مع نانو"""
    try:
        message = request.json.get('message', '').strip()
        user_name = request.json.get('user_name', 'صديق')
        
        if not message:
            return jsonify({"status": "error", "message": "الرسالة فارغة"})
        
        # الحصول على رد نانو
        response = chat_engine.chat(message, user_name)
        
        # الحصول على معلومات الشخصية الحالية
        personality_info = chat_engine.get_personality_info()
        
        return jsonify({
            "status": "success",
            "response": response,
            "personality": chat_engine.get_current_personality(),
            "personality_name": personality_info.get("name", "نانو"),
            "timestamp": datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f"خطأ في المحادثة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/chat_history', methods=['GET'])
def get_chat_history():
    """الحصول على تاريخ المحادثة"""
    try:
        limit = int(request.args.get('limit', 10))
        history = chat_engine.get_recent_chat(limit)
        
        return jsonify({
            "status": "success",
            "history": history,
            "count": len(history)
        })
    
    except Exception as e:
        logger.error(f"خطأ في جلب تاريخ المحادثة: {str(e)}")
        return jsonify({"status": "error", "message": str(e)})

# ======== المهام التلقائية ========

def background_account_processor():
    """معالج الحسابات في الخلفية"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    while True:
        try:
            logger.info("🔄 فحص قائمة إنشاء الحسابات...")
            loop.run_until_complete(account_creator.process_creation_queue())
            
            # انتظار 5 دقائق قبل الفحص التالي
            import time
            time.sleep(300)
            
        except Exception as e:
            logger.error(f"خطأ في معالج الحسابات: {str(e)}")
            import time
            time.sleep(60)  # انتظار دقيقة في حالة الخطأ

# تشغيل معالج الحسابات في خيط منفصل
background_thread = threading.Thread(target=background_account_processor, daemon=True)
background_thread.start()

# ======== إنشاء القوالب ========

def create_templates():
    """إنشاء قوالب HTML"""
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)
    
    # القالب الأساسي
    base_template = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}لوحة تحكم نانو{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .navbar { background: rgba(255,255,255,0.95) !important; backdrop-filter: blur(10px); }
        .card { border: none; border-radius: 15px; box-shadow: 0 8px 25px rgba(0,0,0,0.1); }
        .btn-primary { background: linear-gradient(45deg, #667eea, #764ba2); border: none; }
        .sidebar { min-height: 100vh; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); }
        .personality-card { background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #fecfef 100%); }
        .account-card { background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); }
        .command-card { background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); }
        .status-indicator { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
        .status-online { background-color: #28a745; }
        .status-offline { background-color: #dc3545; }
        .status-pending { background-color: #ffc107; }
    </style>
</head>
<body>
    <!-- شريط التنقل -->
    <nav class="navbar navbar-expand-lg navbar-light fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-robot text-primary"></i> نانو - لوحة التحكم
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto">
                    <li class="nav-item"><a class="nav-link" href="/"><i class="fas fa-tachometer-alt"></i> الرئيسية</a></li>
                    <li class="nav-item"><a class="nav-link" href="/personality"><i class="fas fa-user-cog"></i> الشخصية</a></li>
                    <li class="nav-item"><a class="nav-link" href="/accounts"><i class="fas fa-users"></i> الحسابات</a></li>
                    <li class="nav-item"><a class="nav-link" href="/commands"><i class="fas fa-terminal"></i> الأوامر</a></li>
                </ul>
                <span class="navbar-text">
                    <i class="fas fa-clock"></i> آخر تحديث: <span id="lastUpdate">{{ data.last_updated if data else 'الآن' }}</span>
                </span>
            </div>
        </div>
    </nav>

    <!-- المحتوى الرئيسي -->
    <div class="container-fluid" style="margin-top: 80px;">
        {% block content %}{% endblock %}
    </div>

    <!-- إشعارات -->
    <div id="notifications" class="position-fixed bottom-0 end-0 p-3" style="z-index: 1050;"></div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // وظائف JavaScript مساعدة
        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `alert alert-${type} alert-dismissible fade show`;
            notification.innerHTML = `
                <strong>${type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️'}</strong> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            document.getElementById('notifications').appendChild(notification);
            
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }

        function executeCommand(command) {
            fetch('/api/execute_command', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({command: command})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    showNotification(data.result, 'success');
                } else {
                    showNotification(data.message, 'error');
                }
            })
            .catch(error => {
                showNotification('حدث خطأ في الاتصال', 'error');
            });
        }

        // تحديث الوقت كل دقيقة
        setInterval(() => {
            document.getElementById('lastUpdate').textContent = new Date().toLocaleString('ar-SA');
        }, 60000);
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
    """
    
    # صفحة لوحة التحكم الرئيسية
    dashboard_template = """
{% extends "base.html" %}

{% block title %}لوحة التحكم الرئيسية - نانو{% endblock %}

{% block content %}
<div class="row">
    <!-- بطاقات الحالة السريعة -->
    <div class="col-md-3 mb-4">
        <div class="card personality-card text-white h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">الشخصية الحالية</h6>
                        <h4>{{ data.current_personality }}</h4>
                        <small>مزح: {{ data.humor_level }}/10 | عناد: {{ data.stubbornness_level }}/10</small>
                    </div>
                    <i class="fas fa-user-circle fa-3x opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-4">
        <div class="card account-card text-white h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">الحسابات</h6>
                        <h4>{{ data.total_accounts }}</h4>
                        <small>معلقة: {{ data.pending_accounts }}</small>
                    </div>
                    <i class="fas fa-users fa-3x opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-4">
        <div class="card command-card text-white h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">المحادثات</h6>
                        <h4>{{ data.chat_messages_count }}</h4>
                        <small>رسالة أخيرة</small>
                    </div>
                    <i class="fas fa-comments fa-3x opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-md-3 mb-4">
        <div class="card bg-success text-white h-100">
            <div class="card-body">
                <div class="d-flex justify-content-between">
                    <div>
                        <h6 class="card-title">الحالة</h6>
                        <h4><span class="status-indicator status-online"></span> متصل</h4>
                        <small>يعمل بشكل طبيعي</small>
                    </div>
                    <i class="fas fa-heart fa-3x opacity-75"></i>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="row">
    <!-- أوامر سريعة -->
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-lightning-bolt"></i> أوامر سريعة</h5>
            </div>
            <div class="card-body">
                <div class="row g-2">
                    <div class="col-6">
                        <button class="btn btn-outline-primary btn-sm w-100" onclick="executeCommand('عنيد')">
                            😤 وضع العناد
                        </button>
                    </div>
                    <div class="col-6">
                        <button class="btn btn-outline-success btn-sm w-100" onclick="executeCommand('ساخر')">
                            😏 وضع السخرية
                        </button>
                    </div>
                    <div class="col-6">
                        <button class="btn btn-outline-warning btn-sm w-100" onclick="executeCommand('نكات')">
                            😂 وضع النكات
                        </button>
                    </div>
                    <div class="col-6">
                        <button class="btn btn-outline-info btn-sm w-100" onclick="executeCommand('جدي')">
                            🤔 وضع جدي
                        </button>
                    </div>
                </div>
                
                <hr>
                
                <div class="input-group">
                    <input type="text" class="form-control" id="customCommand" placeholder="أدخل أمر مخصص...">
                    <button class="btn btn-primary" onclick="executeCommand(document.getElementById('customCommand').value)">
                        تنفيذ
                    </button>
                </div>
            </div>
        </div>
    </div>
    
    <!-- إحصائيات الحسابات -->
    <div class="col-md-6 mb-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-chart-pie"></i> إحصائيات الحسابات</h5>
            </div>
            <div class="card-body">
                {% for platform, count in data.platform_accounts.items() %}
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>
                        {% if platform == 'instagram' %}
                            <i class="fab fa-instagram text-danger"></i> انستقرام
                        {% elif platform == 'twitter' %}
                            <i class="fab fa-twitter text-info"></i> تويتر
                        {% elif platform == 'tiktok' %}
                            <i class="fab fa-tiktok text-dark"></i> تيكتوك
                        {% endif %}
                    </span>
                    <span class="badge bg-secondary">{{ count }}</span>
                </div>
                {% endfor %}
                
                <hr>
                
                <div class="d-grid">
                    <a href="/accounts" class="btn btn-outline-primary">إدارة الحسابات</a>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- نافذة المحادثة مع نانو -->
<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                    <i class="fas fa-comments text-primary"></i> 
                    محادثة مع نانو
                    <small class="text-muted" id="nano-personality">{{ data.current_personality }}</small>
                </h5>
                <div class="btn-group" role="group">
                    <button class="btn btn-outline-secondary btn-sm" onclick="clearChat()">
                        <i class="fas fa-eraser"></i> مسح
                    </button>
                    <button class="btn btn-outline-info btn-sm" onclick="loadChatHistory()">
                        <i class="fas fa-history"></i> التاريخ
                    </button>
                </div>
            </div>
            <div class="card-body">
                <!-- منطقة المحادثة -->
                <div id="chat-container" class="border rounded p-3 mb-3" style="height: 300px; overflow-y: auto; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
                    <div class="text-center text-muted py-5">
                        <i class="fas fa-robot fa-3x mb-3"></i>
                        <p>مرحباً! أنا نانو، صديقك الذكي 🤖</p>
                        <p>اكتب أي شيء وسأرد عليك حسب شخصيتي الحالية</p>
                    </div>
                </div>
                
                <!-- أزرار الرسائل السريعة -->
                <div class="mb-3">
                    <small class="text-muted">رسائل سريعة:</small>
                    <div class="mt-1">
                        <button class="btn btn-outline-primary btn-sm me-2 mb-1" onclick="sendQuickMessage('مرحبا نانو')">
                            👋 مرحبا
                        </button>
                        <button class="btn btn-outline-success btn-sm me-2 mb-1" onclick="sendQuickMessage('كيف حالك؟')">
                            🤔 كيف حالك؟
                        </button>
                        <button class="btn btn-outline-warning btn-sm me-2 mb-1" onclick="sendQuickMessage('احكيلي نكتة')">
                            😂 نكتة
                        </button>
                        <button class="btn btn-outline-info btn-sm me-2 mb-1" onclick="sendQuickMessage('وش رأيك بالطقس؟')">
                            ☁️ الطقس
                        </button>
                        <button class="btn btn-outline-secondary btn-sm me-2 mb-1" onclick="sendQuickMessage('شايف إيش نسوي؟')">
                            🎯 أنشطة
                        </button>
                    </div>
                </div>
                
                <!-- مربع الإدخال -->
                <div class="input-group">
                    <input type="text" class="form-control" id="chat-input" 
                           placeholder="اكتب رسالتك هنا..." 
                           onkeypress="if(event.key==='Enter') sendMessage()">
                    <button class="btn btn-primary" onclick="sendMessage()">
                        <i class="fas fa-paper-plane"></i> إرسال
                    </button>
                </div>
                
                <!-- مؤشر الكتابة -->
                <div id="typing-indicator" class="mt-2" style="display: none;">
                    <small class="text-muted">
                        <i class="fas fa-circle-notch fa-spin"></i> نانو يكتب...
                    </small>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- آخر الأوامر -->
{% if data.recent_commands %}
<div class="row">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-history"></i> آخر الأوامر المنفذة</h5>
            </div>
            <div class="card-body">
                <div class="table-responsive">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>الوقت</th>
                                <th>الأمر</th>
                                <th>النتيجة</th>
                                <th>الحالة</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for cmd in data.recent_commands %}
                            <tr>
                                <td>{{ cmd.timestamp.split('T')[1][:5] if 'T' in cmd.timestamp else cmd.timestamp }}</td>
                                <td><code>{{ cmd.command }}</code></td>
                                <td>{{ cmd.result[:50] }}{{ '...' if cmd.result|length > 50 else '' }}</td>
                                <td>
                                    {% if cmd.success %}
                                        <span class="badge bg-success">نجح</span>
                                    {% else %}
                                        <span class="badge bg-danger">فشل</span>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</div>
{% endif %}

<script>
// متغيرات المحادثة
let chatMessages = [];
let userName = 'صديق';

// إرسال رسالة لنانو
function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (!message) {
        showNotification('اكتب رسالة أولاً!', 'warning');
        return;
    }
    
    // إضافة رسالة المستخدم
    addChatMessage(message, 'user');
    
    // مسح مربع الإدخال وإظهار مؤشر الكتابة
    chatInput.value = '';
    showTypingIndicator();
    
    // إرسال للخادم
    fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            message: message,
            user_name: userName
        })
    })
    .then(response => response.json())
    .then(data => {
        hideTypingIndicator();
        
        if (data.status === 'success') {
            // إضافة رد نانو
            addChatMessage(data.response, 'nano', data.personality_name);
            
            // تحديث اسم الشخصية
            document.getElementById('nano-personality').textContent = data.personality_name;
        } else {
            showNotification('خطأ في الرد: ' + data.message, 'error');
        }
    })
    .catch(error => {
        hideTypingIndicator();
        showNotification('خطأ في الاتصال', 'error');
        addChatMessage('آسف، حصل خطأ تقني! 😅 جرب مرة ثانية', 'nano');
    });
}

// إضافة رسالة للمحادثة
function addChatMessage(message, sender, senderName = null) {
    const container = document.getElementById('chat-container');
    
    // إزالة رسالة الترحيب إذا كانت موجودة
    const welcomeMessage = container.querySelector('.text-center.text-muted');
    if (welcomeMessage) {
        welcomeMessage.remove();
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `mb-3 ${sender === 'user' ? 'text-end' : 'text-start'}`;
    
    const time = new Date().toLocaleTimeString('ar-SA', {hour: '2-digit', minute: '2-digit'});
    
    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="d-inline-block px-3 py-2 rounded-pill bg-primary text-white" style="max-width: 70%;">
                ${message}
                <br><small class="opacity-75">${time}</small>
            </div>
        `;
    } else {
        const displayName = senderName || 'نانو';
        messageDiv.innerHTML = `
            <div class="d-inline-block px-3 py-2 rounded-3 bg-light border" style="max-width: 70%;">
                <strong class="text-primary">
                    <i class="fas fa-robot"></i> ${displayName}
                </strong>
                <br>${message}
                <br><small class="text-muted">${time}</small>
            </div>
        `;
    }
    
    container.appendChild(messageDiv);
    
    // التمرير لأسفل
    container.scrollTop = container.scrollHeight;
    
    // حفظ الرسالة محلياً
    chatMessages.push({
        message,
        sender,
        senderName,
        timestamp: new Date().toISOString()
    });
}

// إظهار مؤشر الكتابة
function showTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'block';
}

// إخفاء مؤشر الكتابة
function hideTypingIndicator() {
    document.getElementById('typing-indicator').style.display = 'none';
}

// مسح المحادثة
function clearChat() {
    const container = document.getElementById('chat-container');
    container.innerHTML = `
        <div class="text-center text-muted py-5">
            <i class="fas fa-robot fa-3x mb-3"></i>
            <p>مرحباً! أنا نانو، صديقك الذكي 🤖</p>
            <p>اكتب أي شيء وسأرد عليك حسب شخصيتي الحالية</p>
        </div>
    `;
    chatMessages = [];
    showNotification('تم مسح المحادثة', 'info');
}

// تحميل تاريخ المحادثة
function loadChatHistory() {
    fetch('/api/chat_history?limit=20')
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success' && data.history.length > 0) {
            const container = document.getElementById('chat-container');
            
            // مسح المحادثة الحالية
            container.innerHTML = '';
            
            // إضافة الرسائل السابقة
            data.history.forEach(chat => {
                addChatMessage(chat.user_message, 'user');
                addChatMessage(chat.nano_response, 'nano');
            });
            
            showNotification(`تم تحميل ${data.count} رسائل من التاريخ`, 'success');
        } else {
            showNotification('لا يوجد تاريخ محادثة', 'info');
        }
    })
    .catch(error => {
        showNotification('خطأ في تحميل التاريخ', 'error');
    });
}

// رسائل ترحيب سريعة
function sendQuickMessage(message) {
    document.getElementById('chat-input').value = message;
    sendMessage();
}

// تهيئة المحادثة عند تحميل الصفحة
document.addEventListener('DOMContentLoaded', function() {
    // إضافة أزرار الرسائل السريعة
    const chatContainer = document.getElementById('chat-container');
    
    // رسالة ترحيب تلقائية عند بداية الجلسة
    setTimeout(() => {
        if (chatMessages.length === 0) {
            addChatMessage('مرحباً! كيف حالك اليوم؟ 😊', 'nano');
        }
    }, 1000);
});

// أمثلة رسائل سريعة
const quickMessages = [
    'مرحبا نانو',
    'كيف حالك؟', 
    'احكيلي نكتة',
    'وش رأيك بالطقس؟',
    'شايف إيش نسوي اليوم؟'
];
</script>

{% endblock %}
    """
    
    # حفظ القوالب
    with open(templates_dir / "base.html", "w", encoding="utf-8") as f:
        f.write(base_template)
    
    with open(templates_dir / "dashboard.html", "w", encoding="utf-8") as f:
        f.write(dashboard_template)

# إنشاء القوالب عند التشغيل
create_templates()

if __name__ == "__main__":
    print("🤖 بدء تشغيل لوحة التحكم الرئيسية لنانو...")
    print("=" * 50)
    print("📊 لوحة التحكم: http://localhost:5000")
    print("🎭 إدارة الشخصية: http://localhost:5000/personality")
    print("👥 إدارة الحسابات: http://localhost:5000/accounts")
    print("💻 مركز الأوامر: http://localhost:5000/commands")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)