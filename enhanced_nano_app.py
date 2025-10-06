"""
تطبيق ويب نانو المحسّن
========================

تطبيق ويب متكامل يستخدم النظام المحسّن لنانو مع:
- محرك لاما للهجة السعودية
- نظام المشاعر الذكي
- إنشاء الحسابات الفعلي
- تخصيص الشخصية الديناميكي
"""

from flask import Flask, render_template, request, jsonify, flash
import asyncio
import json
import time
from datetime import datetime
import logging
from pathlib import Path

# استيراد النظام المحسّن
try:
    from core.enhanced_nano_core import EnhancedNanoCore, NanoResponse
    ENHANCED_MODE = True
    print("✅ تم تحميل النظام المحسّن لنانو بنجاح!")
except ImportError as e:
    print(f"❌ فشل في تحميل النظام المحسّن: {e}")
    print("📌 سيتم استخدام النظام الأساسي...")
    ENHANCED_MODE = False

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "nano_enhanced_2024_secret"

# تهيئة نانو
if ENHANCED_MODE:
    nano_core = EnhancedNanoCore()
    logger.info("🚀 تم تهيئة نانو المحسّن بنجاح!")
else:
    nano_core = None
    logger.error("⚠️ النظام المحسّن غير متوفر!")

# ======== الصفحات الرئيسية ========

@app.route('/')
def dashboard():
    """لوحة التحكم الرئيسية"""
    try:
        if not ENHANCED_MODE or not nano_core:
            return render_template_string(ERROR_TEMPLATE, 
                error="النظام المحسّن غير متوفر")
        
        # جمع بيانات الحالة
        status = nano_core.get_nano_status()
        
        dashboard_data = {
            "core_version": status["core_version"],
            "personality_traits": status["active_personality_traits"],
            "emotion_insights": status["emotion_insights"], 
            "user_relationship": status["user_relationship"],
            "accounts_status": status["accounts_status"],
            "stats": status["performance_stats"],
            "settings": status["settings"],
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return render_template_string(DASHBOARD_TEMPLATE, data=dashboard_data)
        
    except Exception as e:
        logger.error(f"خطأ في لوحة التحكم: {str(e)}")
        return f"خطأ في تحميل لوحة التحكم: {str(e)}", 500

@app.route('/personality')
def personality_settings():
    """صفحة إعدادات الشخصية"""
    try:
        if not ENHANCED_MODE:
            return "النظام المحسّن غير متوفر", 503
            
        status = nano_core.get_nano_status()
        return render_template_string(
            PERSONALITY_TEMPLATE, 
            current_traits=status["active_personality_traits"],
            settings=status["settings"]
        )
        
    except Exception as e:
        logger.error(f"خطأ في صفحة الشخصية: {str(e)}")
        return f"خطأ: {str(e)}", 500

@app.route('/accounts')
def accounts_manager():
    """صفحة إدارة الحسابات"""
    try:
        if not ENHANCED_MODE:
            return "النظام المحسّن غير متوفر", 503
            
        accounts_status = nano_core.account_creator.get_creation_status()
        return render_template_string(
            ACCOUNTS_TEMPLATE, 
            accounts=accounts_status
        )
        
    except Exception as e:
        logger.error(f"خطأ في صفحة الحسابات: {str(e)}")
        return f"خطأ: {str(e)}", 500

# ======== واجهات API ========

@app.route('/api/chat', methods=['POST'])
async def chat_with_nano():
    """المحادثة مع نانو المحسّن"""
    try:
        if not ENHANCED_MODE or not nano_core:
            return jsonify({
                "status": "error", 
                "message": "النظام المحسّن غير متوفر"
            })
        
        data = request.json
        message = data.get('message', '').strip()
        user_context = data.get('context', {})
        
        if not message:
            return jsonify({
                "status": "error", 
                "message": "الرسالة فارغة"
            })
        
        # معالجة الرسالة عبر النانوكور المحسّن
        response = await nano_core.process_message(message, user_context)
        
        return jsonify({
            "status": "success",
            "response": response.text,
            "emotion": response.emotion,
            "confidence": response.confidence,
            "personality_traits": response.personality_traits,
            "context_understanding": response.context_understanding,
            "response_time": response.response_time,
            "metadata": response.metadata,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"خطأ في المحادثة: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": f"خطأ: {str(e)}"
        })

@app.route('/api/personality_command', methods=['POST'])
async def execute_personality_command():
    """تنفيذ أمر تخصيص الشخصية"""
    try:
        if not ENHANCED_MODE:
            return jsonify({
                "status": "error", 
                "message": "النظام المحسّن غير متوفر"
            })
        
        command = request.json.get('command', '').strip()
        
        if not command:
            return jsonify({
                "status": "error", 
                "message": "الأمر فارغ"
            })
        
        # تنفيذ الأمر عبر النانوكور
        response = await nano_core.process_message(command)
        
        return jsonify({
            "status": "success",
            "message": "تم تطبيق الأمر",
            "response": response.text,
            "personality_changed": response.metadata.get("personality_changed", False),
            "new_traits": response.personality_traits
        })
        
    except Exception as e:
        logger.error(f"خطأ في تنفيذ أمر الشخصية: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": str(e)
        })

@app.route('/api/create_account', methods=['POST'])
async def create_social_account():
    """إنشاء حساب على منصة اجتماعية"""
    try:
        if not ENHANCED_MODE:
            return jsonify({
                "status": "error", 
                "message": "النظام المحسّن غير متوفر"
            })
        
        platform = request.json.get('platform', '').strip()
        
        if not platform:
            return jsonify({
                "status": "error", 
                "message": "المنصة غير محددة"
            })
        
        # استخدام الأمر الطبيعي لإنشاء الحساب
        command = f"سوي حساب {platform} وعطني يوزرك"
        response = await nano_core.process_message(command)
        
        return jsonify({
            "status": "success" if response.metadata.get("success", False) else "error",
            "message": response.text,
            "account_created": response.metadata.get("account_creation", False),
            "platform": response.metadata.get("platform", platform)
        })
        
    except Exception as e:
        logger.error(f"خطأ في إنشاء الحساب: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": str(e)
        })

@app.route('/api/get_status', methods=['GET'])
def get_nano_status():
    """الحصول على حالة نانو الحالية"""
    try:
        if not ENHANCED_MODE:
            return jsonify({
                "status": "error", 
                "message": "النظام المحسّن غير متوفر"
            })
        
        status = nano_core.get_nano_status()
        
        return jsonify({
            "status": "success",
            "data": status,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"خطأ في جلب الحالة: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": str(e)
        })

@app.route('/api/reset_conversation', methods=['POST'])
def reset_chat():
    """إعادة تعيين المحادثة"""
    try:
        if not ENHANCED_MODE:
            return jsonify({
                "status": "error", 
                "message": "النظام المحسّن غير متوفر"
            })
        
        nano_core.reset_conversation()
        
        return jsonify({
            "status": "success",
            "message": "تم إعادة تعيين المحادثة"
        })
        
    except Exception as e:
        logger.error(f"خطأ في إعادة التعيين: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": str(e)
        })

# ======== القوالب ========

def render_template_string(template_content, **context):
    """عرض قالب من نص"""
    from jinja2 import Template
    template = Template(template_content)
    return template.render(**context)

# قالب الخطأ
ERROR_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>خطأ - نانو</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card border-danger">
                    <div class="card-header bg-danger text-white">
                        <h4><i class="fas fa-exclamation-triangle"></i> خطأ في النظام</h4>
                    </div>
                    <div class="card-body">
                        <p class="card-text">{{ error }}</p>
                        <p>يرجى التأكد من تثبيت كافة المتطلبات وإعادة تشغيل النظام.</p>
                        <a href="/" class="btn btn-primary">العودة للرئيسية</a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# قالب لوحة التحكم الرئيسية
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - نانو المحسّن</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .card { 
            border: none; 
            border-radius: 15px; 
            box-shadow: 0 8px 25px rgba(0,0,0,0.1); 
            backdrop-filter: blur(10px);
            background: rgba(255, 255, 255, 0.95);
        }
        .gradient-primary { background: linear-gradient(45deg, #667eea, #764ba2); }
        .gradient-success { background: linear-gradient(45deg, #56ab2f, #a8e6cf); }
        .gradient-info { background: linear-gradient(45deg, #3ca5e2, #a8e6cf); }
        .gradient-warning { background: linear-gradient(45deg, #ffb347, #ffcc5c); }
    </style>
</head>
<body>
    <!-- شريط التنقل -->
    <nav class="navbar navbar-expand-lg navbar-dark gradient-primary">
        <div class="container">
            <a class="navbar-brand fw-bold" href="/">
                <i class="fas fa-robot"></i> نانو المحسّن {{ data.core_version }}
            </a>
            <div class="navbar-nav ms-auto">
                <span class="navbar-text text-white">
                    <i class="fas fa-circle text-success"></i> متصل ونشط
                </span>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        <!-- بطاقات الإحصائيات -->
        <div class="row mb-4">
            <div class="col-md-3 mb-3">
                <div class="card gradient-primary text-white h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>المحادثات</h6>
                                <h3>{{ data.stats.total_conversations }}</h3>
                                <small>نجح منها {{ data.stats.successful_responses }}</small>
                            </div>
                            <i class="fas fa-comments fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="card gradient-success text-white h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>الحسابات</h6>
                                <h3>{{ data.accounts_status.total_created }}</h3>
                                <small>منصات متعددة</small>
                            </div>
                            <i class="fas fa-users fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="card gradient-info text-white h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>الشخصية</h6>
                                <h3>{{ data.stats.personality_changes }}</h3>
                                <small>تغيير في الشخصية</small>
                            </div>
                            <i class="fas fa-user-cog fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-3 mb-3">
                <div class="card gradient-warning text-white h-100">
                    <div class="card-body">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h6>مستوى العلاقة</h6>
                                <h3>{{ data.user_relationship.level }}</h3>
                                <small>{{ data.user_relationship.positive_interactions }} تفاعل إيجابي</small>
                            </div>
                            <i class="fas fa-heart fa-2x opacity-75"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="row">
            <!-- نافذة المحادثة -->
            <div class="col-md-8 mb-4">
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">
                            <i class="fas fa-comments text-primary"></i>
                            محادثة مع نانو المحسّن
                        </h5>
                        <div class="btn-group btn-group-sm">
                            <button class="btn btn-outline-secondary" onclick="clearChat()">
                                <i class="fas fa-eraser"></i> مسح
                            </button>
                            <button class="btn btn-outline-info" onclick="resetNano()">
                                <i class="fas fa-refresh"></i> إعادة تعيين
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <!-- منطقة المحادثة -->
                        <div id="chat-container" class="border rounded p-3 mb-3" 
                             style="height: 400px; overflow-y: auto; background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
                            <div class="text-center text-muted py-5">
                                <i class="fas fa-robot fa-3x mb-3 text-primary"></i>
                                <h5>مرحباً! أنا نانو المحسّن 🤖</h5>
                                <p>أستخدم الآن محرك لاما للهجة السعودية مع نظام مشاعر ذكي</p>
                                <p>يمكنك تخصيص شخصيتي أو طلب إنشاء حسابات اجتماعية!</p>
                            </div>
                        </div>
                        
                        <!-- رسائل سريعة للتجربة -->
                        <div class="mb-3">
                            <small class="text-muted">جرب هذه الأوامر:</small>
                            <div class="mt-2">
                                <button class="btn btn-outline-primary btn-sm me-2 mb-1" onclick="sendQuickMessage('مرحبا نانو')">
                                    👋 مرحبا
                                </button>
                                <button class="btn btn-outline-success btn-sm me-2 mb-1" onclick="sendQuickMessage('قول ميو نهاية كل جملة')">
                                    🐱 قول ميو
                                </button>
                                <button class="btn btn-outline-warning btn-sm me-2 mb-1" onclick="sendQuickMessage('كن واثق مع الرجال وخفيف مع البنات')">
                                    💪 تكيف حسب الجنس
                                </button>
                                <button class="btn btn-outline-info btn-sm me-2 mb-1" onclick="sendQuickMessage('سوي حساب انستقرام')">
                                    📱 إنشاء حساب
                                </button>
                                <button class="btn btn-outline-danger btn-sm me-2 mb-1" onclick="sendQuickMessage('يا أصلع')">
                                    😤 اختبار الإهانة
                                </button>
                            </div>
                        </div>
                        
                        <!-- مربع الإدخال -->
                        <div class="input-group">
                            <input type="text" class="form-control" id="chat-input" 
                                   placeholder="اكتب رسالتك أو أمر تخصيص..." 
                                   onkeypress="if(event.key==='Enter') sendMessage()">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i> إرسال
                            </button>
                        </div>
                        
                        <div id="typing-indicator" class="mt-2" style="display: none;">
                            <small class="text-muted">
                                <i class="fas fa-circle-notch fa-spin"></i> نانو يفكر ويحلل...
                            </small>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- لوحة الحالة والتحكم -->
            <div class="col-md-4 mb-4">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-cog"></i> حالة النظام</h5>
                    </div>
                    <div class="card-body">
                        <div id="system-status">
                            <div class="mb-3">
                                <strong>الشخصية الحالية:</strong>
                                <div id="current-traits" class="mt-1">
                                    <span class="badge bg-secondary">تحميل...</span>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <strong>آخر مشاعر مكتشفة:</strong>
                                <div id="last-emotion" class="mt-1">
                                    <span class="badge bg-info">غير محدد</span>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <strong>زمن الاستجابة:</strong>
                                <div id="response-time" class="mt-1">
                                    <span class="badge bg-success">-- ثانية</span>
                                </div>
                            </div>
                            
                            <div class="mb-3">
                                <strong>درجة الثقة:</strong>
                                <div id="confidence-level" class="mt-1">
                                    <div class="progress">
                                        <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        <hr>
                        
                        <div class="d-grid gap-2">
                            <a href="/personality" class="btn btn-outline-primary btn-sm">
                                <i class="fas fa-user-cog"></i> إعدادات الشخصية
                            </a>
                            <a href="/accounts" class="btn btn-outline-success btn-sm">
                                <i class="fas fa-users"></i> إدارة الحسابات
                            </a>
                            <button class="btn btn-outline-info btn-sm" onclick="getSystemStatus()">
                                <i class="fas fa-sync"></i> تحديث الحالة
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- إشعارات -->
    <div id="notifications" class="position-fixed bottom-0 end-0 p-3" style="z-index: 1050;"></div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // متغيرات المحادثة
        let chatMessages = [];
        
        // إرسال رسالة
        async function sendMessage() {
            const chatInput = document.getElementById('chat-input');
            const message = chatInput.value.trim();
            
            if (!message) {
                showNotification('اكتب رسالة أولاً!', 'warning');
                return;
            }
            
            // إضافة رسالة المستخدم
            addChatMessage(message, 'user');
            chatInput.value = '';
            showTypingIndicator();
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message})
                });
                
                const data = await response.json();
                hideTypingIndicator();
                
                if (data.status === 'success') {
                    // إضافة رد نانو
                    addChatMessage(data.response, 'nano');
                    
                    // تحديث معلومات النظام
                    updateSystemStatus(data);
                } else {
                    showNotification('خطأ: ' + data.message, 'error');
                    addChatMessage('عذراً، واجهت مشكلة تقنية 😅', 'nano');
                }
            } catch (error) {
                hideTypingIndicator();
                showNotification('خطأ في الاتصال', 'error');
                addChatMessage('مشكلة في الاتصال، جرب مرة ثانية 🔄', 'nano');
            }
        }
        
        // إضافة رسالة للمحادثة
        function addChatMessage(message, sender) {
            const container = document.getElementById('chat-container');
            
            // إزالة رسالة الترحيب
            const welcome = container.querySelector('.text-center.text-muted');
            if (welcome) welcome.remove();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `mb-3 ${sender === 'user' ? 'text-end' : 'text-start'}`;
            
            const time = new Date().toLocaleTimeString('ar-SA');
            
            if (sender === 'user') {
                messageDiv.innerHTML = `
                    <div class="d-inline-block px-3 py-2 rounded-pill bg-primary text-white" style="max-width: 80%;">
                        ${message}
                        <br><small class="opacity-75">${time}</small>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="d-inline-block px-3 py-2 rounded-3 bg-light border" style="max-width: 80%;">
                        <strong class="text-primary">
                            <i class="fas fa-robot"></i> نانو
                        </strong>
                        <br>${message}
                        <br><small class="text-muted">${time}</small>
                    </div>
                `;
            }
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
            
            chatMessages.push({message, sender, time});
        }
        
        // تحديث حالة النظام
        function updateSystemStatus(data) {
            // الشخصية
            const traitsContainer = document.getElementById('current-traits');
            const traits = Object.keys(data.personality_traits || {});
            traitsContainer.innerHTML = traits.length > 0 
                ? traits.map(t => `<span class="badge bg-primary me-1">${t}</span>`).join('')
                : '<span class="badge bg-secondary">افتراضي</span>';
            
            // المشاعر
            document.getElementById('last-emotion').innerHTML = 
                `<span class="badge bg-info">${data.emotion}</span>`;
            
            // زمن الاستجابة
            document.getElementById('response-time').innerHTML = 
                `<span class="badge bg-success">${data.response_time.toFixed(2)}s</span>`;
            
            // درجة الثقة
            const confidence = Math.round(data.confidence * 100);
            const progressBar = document.querySelector('#confidence-level .progress-bar');
            progressBar.style.width = confidence + '%';
            progressBar.textContent = confidence + '%';
            progressBar.className = `progress-bar ${confidence > 70 ? 'bg-success' : confidence > 40 ? 'bg-warning' : 'bg-danger'}`;
        }
        
        // رسائل سريعة
        function sendQuickMessage(message) {
            document.getElementById('chat-input').value = message;
            sendMessage();
        }
        
        // وظائف المساعدة
        function showTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'block';
        }
        
        function hideTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'none';
        }
        
        function clearChat() {
            const container = document.getElementById('chat-container');
            container.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-robot fa-3x mb-3 text-primary"></i>
                    <h5>مرحباً! أنا نانو المحسّن 🤖</h5>
                    <p>جاهز للمحادثة مرة أخرى!</p>
                </div>
            `;
            chatMessages = [];
            showNotification('تم مسح المحادثة', 'info');
        }
        
        async function resetNano() {
            try {
                const response = await fetch('/api/reset_conversation', {method: 'POST'});
                const data = await response.json();
                
                if (data.status === 'success') {
                    clearChat();
                    showNotification('تم إعادة تعيين نانو', 'success');
                } else {
                    showNotification('فشل في إعادة التعيين', 'error');
                }
            } catch (error) {
                showNotification('خطأ في الاتصال', 'error');
            }
        }
        
        async function getSystemStatus() {
            try {
                const response = await fetch('/api/get_status');
                const data = await response.json();
                
                if (data.status === 'success') {
                    showNotification('تم تحديث حالة النظام', 'success');
                    // يمكن إضافة تحديثات إضافية هنا
                }
            } catch (error) {
                showNotification('خطأ في جلب الحالة', 'error');
            }
        }
        
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
        
        // رسالة ترحيب تلقائية
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(() => {
                if (chatMessages.length === 0) {
                    addChatMessage('مرحباً! جرب الأوامر الجديدة مثل "قول ميو نهاية كل جملة" أو "سوي حساب انستقرام" 😊', 'nano');
                }
            }, 1500);
        });
    </script>
</body>
</html>
"""

# قالب إعدادات الشخصية
PERSONALITY_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>إعدادات الشخصية - نانو</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h2>إعدادات شخصية نانو</h2>
        <div class="card">
            <div class="card-body">
                <p>الصفات الحالية: {{ current_traits }}</p>
                <p>الإعدادات: {{ settings }}</p>
            </div>
        </div>
        <a href="/" class="btn btn-primary">العودة للرئيسية</a>
    </div>
</body>
</html>
"""

# قالب إدارة الحسابات
ACCOUNTS_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>إدارة الحسابات - نانو</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h2>إدارة حسابات نانو</h2>
        <div class="card">
            <div class="card-body">
                <p>إجمالي الحسابات: {{ accounts.total_created }}</p>
                <p>المنصات: {{ accounts.platforms }}</p>
                <p>آخر حساب: {{ accounts.latest_account }}</p>
            </div>
        </div>
        <a href="/" class="btn btn-primary">العودة للرئيسية</a>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    print("🚀 بدء تشغيل نانو المحسّن...")
    print("=" * 50)
    
    if ENHANCED_MODE:
        print("✅ النظام المحسّن: متاح")
        print("🧠 محرك لاما: نشط")
        print("💝 نظام المشاعر الذكي: نشط") 
        print("👥 إنشاء الحسابات: نشط")
        print("🎭 تخصيص الشخصية: نشط")
    else:
        print("❌ النظام المحسّن: غير متاح")
        print("⚠️  سيتم تشغيل الواجهة الأساسية فقط")
    
    print("=" * 50)
    print("🌐 التطبيق: http://localhost:5000")
    print("🎯 الشخصية: http://localhost:5000/personality") 
    print("👥 الحسابات: http://localhost:5000/accounts")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)