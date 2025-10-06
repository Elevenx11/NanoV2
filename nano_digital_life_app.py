# nano_digital_life_app.py - واجهة تطبيق حياة نانو الرقمية
import os
import sys
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import threading
import time
import json
from pathlib import Path

# إضافة مجلد core للمسار
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

try:
    from core.nano_digital_life import NanoDigitalLife
    print("✅ تم تحميل نظام حياة نانو بنجاح")
except ImportError as e:
    print(f"❌ خطأ في تحميل نظام نانو: {e}")
    sys.exit(1)

# إنشاء تطبيق Flask
app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

# إعدادات التطبيق
app.secret_key = 'nano_digital_life_2024_secret'

# إنشاء حياة نانو الرقمية
nano_life = None
nano_active = False

def initialize_nano():
    """تهيئة نانو وبدء حياته الرقمية"""
    global nano_life, nano_active
    try:
        print("🚀 تهيئة نانو...")
        nano_life = NanoDigitalLife(data_path="data/nano_life")
        nano_life.start_nano_life()
        nano_active = True
        print("✅ نانو جاهز!")
        
        # بدء الروتين التلقائي لنانو
        start_nano_background_routine()
        
    except Exception as e:
        print(f"❌ خطأ في تهيئة نانو: {e}")
        nano_active = False

def start_nano_background_routine():
    """يشغل روتين نانو في الخلفية"""
    def background_routine():
        while nano_active and nano_life:
            try:
                time.sleep(300)  # كل 5 دقائق
                if nano_life:
                    nano_life.daily_routine()
            except Exception as e:
                print(f"خطأ في الروتين التلقائي: {e}")
                time.sleep(60)
    
    thread = threading.Thread(target=background_routine, daemon=True)
    thread.start()
    print("🔄 بدأ الروتين التلقائي لنانو")

# الصفحات الرئيسية
@app.route('/')
def home():
    """الصفحة الرئيسية لنانو"""
    if not nano_active or not nano_life:
        return render_template('error.html', 
                             message="نانو غير متاح حالياً",
                             error="يرجى المحاولة لاحقاً")
    
    status = nano_life.get_nano_status()
    recent_memories = nano_life.memories[-5:] if nano_life.memories else []
    
    return render_template('nano_home.html', 
                         status=status,
                         recent_memories=recent_memories,
                         current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

@app.route('/chat')
def chat_page():
    """صفحة المحادثة مع نانو"""
    if not nano_active or not nano_life:
        return redirect(url_for('home'))
    
    return render_template('nano_chat.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API للمحادثة مع نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح حالياً"
        })
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                "success": False,
                "error": "الرجاء كتابة رسالة"
            })
        
        # نانو يرد على الرسالة
        nano_response = nano_life.chat_with_friend(user_message)
        
        # معلومات إضافية عن حالة نانو
        current_status = nano_life.get_nano_status()
        
        return jsonify({
            "success": True,
            "nano_response": nano_response,
            "nano_mood": current_status['mood']['current'],
            "nano_energy": f"{current_status['mood']['energy']:.1%}",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في المحادثة: {str(e)}"
        })

@app.route('/status')
def status_page():
    """صفحة حالة نانو المفصلة"""
    if not nano_active or not nano_life:
        return redirect(url_for('home'))
    
    status = nano_life.get_nano_status()
    
    return render_template('nano_status.html', 
                         status=status,
                         memories=nano_life.memories[-10:],
                         projects=nano_life.current_projects)

@app.route('/api/status')
def status_api():
    """API لحالة نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        status = nano_life.get_nano_status()
        
        return jsonify({
            "success": True,
            "status": status,
            "active": nano_active,
            "last_updated": datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })

@app.route('/create')
def create_page():
    """صفحة إبداعات نانو"""
    if not nano_active or not nano_life:
        return redirect(url_for('home'))
    
    return render_template('nano_create.html')

@app.route('/api/create/<content_type>')
def create_content_api(content_type):
    """API لطلب إبداع معين من نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        creative_engine = nano_life.creative_engine
        content = ""
        caption = ""
        
        if content_type == "ascii_art":
            subject = request.args.get('subject', 'جمل عربي')
            content = creative_engine.create_ascii_art(subject)
            caption = f"🎨 رسمت {subject} بفن ASCII!"
            
        elif content_type == "poem":
            theme = request.args.get('theme', 'الصداقة الرقمية')
            content = creative_engine.write_poem(theme)
            caption = f"✍️ قصيدة عن {theme}"
            
        elif content_type == "story":
            theme = request.args.get('theme', 'مغامرة')
            content = creative_engine.write_short_story(theme)
            caption = "📚 قصة قصيرة جديدة"
            
        elif content_type == "manga":
            concept = creative_engine.create_manga_concept()
            content = json.dumps(concept, ensure_ascii=False, indent=2)
            caption = f"🎌 مفهوم مانجا: {concept['title']}"
            
        else:
            return jsonify({
                "success": False,
                "error": "نوع المحتوى غير مدعوم"
            })
        
        # نانو ينشر المحتوى (محاكاة)
        if nano_life.instagram.is_logged_in:
            nano_life.instagram.post_content("text", "", caption)
        
        return jsonify({
            "success": True,
            "content": content,
            "caption": caption,
            "type": content_type,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في الإبداع: {str(e)}"
        })

@app.route('/instagram')
def instagram_page():
    """صفحة حساب انستقرام نانو"""
    if not nano_active or not nano_life:
        return redirect(url_for('home'))
    
    instagram_stats = nano_life.instagram.activity_stats
    
    return render_template('nano_instagram.html', 
                         instagram=nano_life.instagram,
                         stats=instagram_stats)

@app.route('/api/instagram/post', methods=['POST'])
def instagram_post_api():
    """API لنشر محتوى على انستقرام نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        data = request.get_json()
        caption = data.get('caption', '')
        content_type = data.get('type', 'text')
        
        if not caption:
            return jsonify({
                "success": False,
                "error": "الرجاء كتابة تسمية للمنشور"
            })
        
        # نانو ينشر المحتوى
        success = nano_life.instagram.post_content(content_type, "", caption)
        
        if success:
            return jsonify({
                "success": True,
                "message": "تم النشر بنجاح!",
                "posts_count": nano_life.instagram.activity_stats["posts_created"]
            })
        else:
            return jsonify({
                "success": False,
                "error": "فشل في النشر"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في النشر: {str(e)}"
        })

@app.route('/api/instagram/dm', methods=['POST'])
def instagram_dm_api():
    """API لإرسال رسالة خاصة من نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 'you')  # افتراضياً أنت
        
        if not message:
            return jsonify({
                "success": False,
                "error": "الرجاء كتابة رسالة"
            })
        
        # نانو يرسل رسالة خاصة
        success = nano_life.instagram.send_dm(user_id, message)
        
        if success:
            return jsonify({
                "success": True,
                "message": "تم إرسال الرسالة!",
                "messages_count": nano_life.instagram.activity_stats["messages_sent"]
            })
        else:
            return jsonify({
                "success": False,
                "error": "فشل في الإرسال"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في الإرسال: {str(e)}"
        })

@app.route('/admin')
def admin_page():
    """صفحة إدارة نانو"""
    if not nano_active or not nano_life:
        return redirect(url_for('home'))
    
    return render_template('nano_admin.html', 
                         nano_life=nano_life)

@app.route('/api/admin/mood', methods=['POST'])
def update_mood_api():
    """API لتحديث مزاج نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        data = request.get_json()
        new_mood = data.get('mood', '')
        energy_level = float(data.get('energy', 0.5))
        creativity_level = float(data.get('creativity', 0.5))
        
        # تحديث مزاج نانو
        nano_life.current_mood.mood = new_mood
        nano_life.current_mood.energy_level = energy_level
        nano_life.current_mood.creativity_level = creativity_level
        nano_life.current_mood.last_updated = datetime.now()
        
        return jsonify({
            "success": True,
            "message": "تم تحديث مزاج نانو",
            "new_mood": new_mood
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في التحديث: {str(e)}"
        })

@app.route('/api/admin/skill', methods=['POST'])
def update_skill_api():
    """API لتحديث مهارات نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        data = request.get_json()
        skill_name = data.get('skill', '')
        level_increase = float(data.get('increase', 0.1))
        
        if skill_name in nano_life.skills:
            skill = nano_life.skills[skill_name]
            skill.level = min(1.0, skill.level + level_increase)
            skill.experience += int(level_increase * 100)
            skill.last_practiced = datetime.now()
            
            return jsonify({
                "success": True,
                "message": f"تم تطوير مهارة {skill_name}",
                "new_level": f"{skill.level:.1%}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "المهارة غير موجودة"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في التحديث: {str(e)}"
        })

@app.route('/api/admin/save')
def save_data_api():
    """API لحفظ بيانات نانو"""
    if not nano_active or not nano_life:
        return jsonify({
            "success": False,
            "error": "نانو غير متاح"
        })
    
    try:
        nano_life.save_nano_life_data()
        
        return jsonify({
            "success": True,
            "message": "تم حفظ بيانات نانو",
            "saved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"خطأ في الحفظ: {str(e)}"
        })

# إنشاء مجلدات القوالب والملفات الثابتة
def create_app_directories():
    """إنشاء مجلدات التطبيق"""
    directories = ['templates', 'static/css', 'static/js', 'static/images', 'data/nano_life']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("📁 تم إنشاء مجلدات التطبيق")

def create_templates():
    """إنشاء قوالب HTML للتطبيق"""
    
    # القالب الأساسي
    base_template = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}نانو - صديقك الإلكتروني{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .nano-card {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        .nano-header {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            color: white;
            border-radius: 15px 15px 0 0;
            padding: 20px;
            text-align: center;
        }
        .mood-indicator {
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            margin: 5px;
        }
        .mood-فضول { background-color: #FFE5B4; color: #8B4513; }
        .mood-متحمس { background-color: #FFB6C1; color: #8B0000; }
        .mood-مبسوط { background-color: #98FB98; color: #006400; }
        .mood-ملل { background-color: #D3D3D3; color: #2F4F4F; }
        .mood-إبداع { background-color: #DDA0DD; color: #4B0082; }
        
        .skill-bar {
            background-color: #e9ecef;
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin-bottom: 10px;
        }
        .skill-progress {
            height: 100%;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            transition: width 0.5s ease;
        }
        
        .chat-container {
            height: 500px;
            overflow-y: auto;
            border: 2px solid #e9ecef;
            border-radius: 10px;
            padding: 15px;
            background-color: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
        }
        .message.user {
            background-color: #007bff;
            color: white;
            margin-left: auto;
            text-align: left;
        }
        .message.nano {
            background-color: #28a745;
            color: white;
            margin-right: auto;
        }
        
        .btn-nano {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            border: none;
            color: white;
            border-radius: 25px;
            padding: 10px 25px;
            transition: all 0.3s ease;
        }
        .btn-nano:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            color: white;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-transparent">
        <div class="container">
            <a class="navbar-brand" href="{{ url_for('home') }}">
                🤖 نانو - صديقك الإلكتروني
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="{{ url_for('home') }}">الرئيسية</a>
                <a class="nav-link" href="{{ url_for('chat_page') }}">المحادثة</a>
                <a class="nav-link" href="{{ url_for('create_page') }}">الإبداع</a>
                <a class="nav-link" href="{{ url_for('status_page') }}">الحالة</a>
                <a class="nav-link" href="{{ url_for('instagram_page') }}">انستقرام</a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.0.min.js"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>"""
    
    # الصفحة الرئيسية
    home_template = """{% extends "base.html" %}

{% block content %}
<div class="row">
    <div class="col-lg-8">
        <div class="nano-card">
            <div class="nano-header">
                <h1><i class="fas fa-robot"></i> مرحباً! أنا نانو</h1>
                <p class="mb-0">صديقك الإلكتروني الذي يحب الإبداع والمرح!</p>
                <div class="mt-2">
                    <span class="mood-indicator mood-{{ status.mood.current }}">
                        💭 {{ status.mood.current }}
                    </span>
                    <span class="mood-indicator" style="background-color: rgba(255,255,255,0.2);">
                        ⚡ {{ (status.mood.energy * 100)|int }}%
                    </span>
                </div>
            </div>
            <div class="card-body p-4">
                <div class="row">
                    <div class="col-md-6">
                        <h5><i class="fas fa-brain"></i> مهاراتي الحالية:</h5>
                        {% for skill_name, skill_data in status.skills.items() %}
                        <div class="mb-2">
                            <small>{{ skill_name }} - {{ (skill_data.level * 100)|int }}%</small>
                            <div class="skill-bar">
                                <div class="skill-progress" style="width: {{ (skill_data.level * 100)|int }}%"></div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                    <div class="col-md-6">
                        <h5><i class="fas fa-heart"></i> اهتماماتي:</h5>
                        {% for interest, level in status.current_interests.items() %}
                        <span class="badge bg-secondary me-1">{{ interest }} {{ (level * 100)|int }}%</span>
                        {% endfor %}
                    </div>
                </div>
                
                <hr>
                
                <div class="text-center">
                    <a href="{{ url_for('chat_page') }}" class="btn btn-nano me-2">
                        <i class="fas fa-comments"></i> تعال نسولف!
                    </a>
                    <a href="{{ url_for('create_page') }}" class="btn btn-nano me-2">
                        <i class="fas fa-palette"></i> شوف إبداعي
                    </a>
                    <a href="{{ url_for('instagram_page') }}" class="btn btn-nano">
                        <i class="fab fa-instagram"></i> انستقرامي
                    </a>
                </div>
            </div>
        </div>
    </div>
    
    <div class="col-lg-4">
        <div class="nano-card">
            <div class="card-header bg-info text-white">
                <h5><i class="fas fa-memory"></i> ذكرياتي الأخيرة</h5>
            </div>
            <div class="card-body">
                {% if recent_memories %}
                {% for memory in recent_memories %}
                <div class="mb-3 p-2 border-start border-primary border-3">
                    <small class="text-muted">{{ memory.event_type }} - {{ memory.timestamp.strftime('%Y-%m-%d %H:%M') }}</small>
                    <p class="mb-1 small">{{ memory.content }}</p>
                    <div>
                        {% for emotion in memory.emotions_felt %}
                        <span class="badge bg-light text-dark">{{ emotion }}</span>
                        {% endfor %}
                    </div>
                </div>
                {% endfor %}
                {% else %}
                <p class="text-muted">لا توجد ذكريات حتى الآن...</p>
                {% endif %}
            </div>
        </div>
        
        <div class="nano-card mt-3">
            <div class="card-header bg-success text-white">
                <h5><i class="fab fa-instagram"></i> نشاطي على انستقرام</h5>
            </div>
            <div class="card-body text-center">
                <div class="row">
                    <div class="col-6">
                        <h4>{{ status.instagram.posts }}</h4>
                        <small>منشور</small>
                    </div>
                    <div class="col-6">
                        <h4>{{ status.instagram.messages }}</h4>
                        <small>رسالة</small>
                    </div>
                </div>
                <div class="mt-2">
                    {% if status.instagram.logged_in %}
                    <span class="badge bg-success">متصل</span>
                    {% else %}
                    <span class="badge bg-warning">غير متصل</span>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</div>

<div class="text-center mt-4">
    <p class="text-white-50">
        <i class="fas fa-clock"></i> آخر تحديث: {{ current_time }}
    </p>
</div>
{% endblock %}"""
    
    # صفحة المحادثة
    chat_template = """{% extends "base.html" %}

{% block title %}محادثة مع نانو{% endblock %}

{% block content %}
<div class="row justify-content-center">
    <div class="col-lg-8">
        <div class="nano-card">
            <div class="nano-header">
                <h2><i class="fas fa-comments"></i> محادثة مع نانو</h2>
                <p class="mb-0">تكلم معي عن أي شي تبغاه! 😊</p>
            </div>
            <div class="card-body">
                <div id="chat-container" class="chat-container">
                    <div class="message nano">
                        <strong>نانو:</strong> هاي! أنا نانو صديقك الإلكتروني! كيفك اليوم؟ 😊
                    </div>
                </div>
                
                <div class="mt-3">
                    <div class="input-group">
                        <input type="text" id="message-input" class="form-control" placeholder="اكتب رسالتك هنا..." maxlength="500">
                        <button id="send-btn" class="btn btn-nano">
                            <i class="fas fa-paper-plane"></i> إرسال
                        </button>
                    </div>
                </div>
                
                <div class="mt-2 text-center">
                    <small class="text-muted">مزاج نانو: <span id="nano-mood">فضول</span> | طاقة: <span id="nano-energy">80%</span></small>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block extra_js %}
<script>
$(document).ready(function() {
    const chatContainer = $('#chat-container');
    const messageInput = $('#message-input');
    const sendBtn = $('#send-btn');
    
    function sendMessage() {
        const message = messageInput.val().trim();
        if (!message) return;
        
        // إضافة رسالة المستخدم
        chatContainer.append(`
            <div class="message user">
                <strong>أنت:</strong> ${message}
            </div>
        `);
        
        // إظهار مؤشر الكتابة
        chatContainer.append(`
            <div class="message nano typing">
                <strong>نانو:</strong> <i class="fas fa-ellipsis-h"></i> يكتب...
            </div>
        `);
        
        messageInput.val('');
        chatContainer.scrollTop(chatContainer[0].scrollHeight);
        
        // إرسال الرسالة لنانو
        $.ajax({
            url: '/api/chat',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({message: message}),
            success: function(response) {
                $('.typing').remove();
                
                if (response.success) {
                    chatContainer.append(`
                        <div class="message nano">
                            <strong>نانو:</strong> ${response.nano_response}
                            <small class="text-muted d-block mt-1">${response.timestamp}</small>
                        </div>
                    `);
                    
                    // تحديث حالة نانو
                    $('#nano-mood').text(response.nano_mood);
                    $('#nano-energy').text(response.nano_energy);
                } else {
                    chatContainer.append(`
                        <div class="message nano">
                            <strong>نانو:</strong> عذراً، واجهت مشكلة: ${response.error}
                        </div>
                    `);
                }
                
                chatContainer.scrollTop(chatContainer[0].scrollHeight);
            },
            error: function() {
                $('.typing').remove();
                chatContainer.append(`
                    <div class="message nano">
                        <strong>نانو:</strong> عذراً، لم أستطع الرد الآن. حاول مرة أخرى!
                    </div>
                `);
                chatContainer.scrollTop(chatContainer[0].scrollHeight);
            }
        });
    }
    
    sendBtn.click(sendMessage);
    messageInput.keypress(function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });
});
</script>
{% endblock %}"""
    
    # حفظ القوالب
    templates = {
        'base.html': base_template,
        'nano_home.html': home_template,
        'nano_chat.html': chat_template
    }
    
    for filename, content in templates.items():
        with open(f'templates/{filename}', 'w', encoding='utf-8') as f:
            f.write(content)
    
    print("📄 تم إنشاء قوالب HTML")

def run_nano_app():
    """تشغيل تطبيق نانو"""
    print("🚀 بدء تطبيق حياة نانو الرقمية...")
    
    # إنشاء المجلدات والقوالب
    create_app_directories()
    create_templates()
    
    # تهيئة نانو
    initialize_nano()
    
    if not nano_active:
        print("❌ فشل في تهيئة نانو")
        return
    
    print("🌐 تشغيل الخادم على http://localhost:5000")
    print("📱 يمكنك الآن تصفح التطبيق والتحدث مع نانو!")
    
    try:
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n👋 وداعاً! نانو ينام الآن...")
        global nano_active
        nano_active = False

if __name__ == '__main__':
    run_nano_app()