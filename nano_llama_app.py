# nano_llama_app.py - التطبيق الرئيسي الجديد لنانو مع Llama
import os
import sys
import json
import time
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

# إضافة مجلد core لمسار Python
sys.path.append(str(Path(__file__).parent / "core"))

try:
    from flask import Flask, request, jsonify, render_template, redirect, url_for, session
    from flask import send_from_directory, flash
    from werkzeug.serving import make_server
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("تحذير: Flask غير متوفر. سيتم استخدام واجهة المحطة الطرفية فقط.")

# استيراد محرك نانو الجديد
try:
    from core.nano_llama_brain import NanoLlamaBrain, NanoLlamaResponse
    from core.llama_engine import LlamaEngine
    from core.saudi_fine_tuner import SaudiFinetuner
except ImportError as e:
    print(f"خطأ في استيراد محرك نانو: {e}")
    print("تأكد من وجود جميع الملفات في مجلد core")
    sys.exit(1)

class NanoLlamaApp:
    """التطبيق الرئيسي لنانو مع Llama"""
    
    def __init__(self, data_path: str = "data"):
        self.data_path = Path(data_path)
        self.data_path.mkdir(exist_ok=True)
        
        # إعداد السجلات
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.data_path / 'nano_llama.log', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        # محرك نانو الرئيسي
        self.nano_brain = None
        self.web_server = None
        self.is_running = False
        
        # إحصائيات التطبيق
        self.app_stats = {
            "start_time": datetime.now(),
            "total_requests": 0,
            "successful_responses": 0,
            "failed_responses": 0,
            "web_requests": 0,
            "terminal_requests": 0
        }
        
        # إعدادات التطبيق
        self.app_config = {
            "web_interface": True,
            "terminal_interface": True,
            "auto_save": True,
            "auto_backup": True,
            "port": 5000,
            "debug": False,
            "max_response_time": 10.0
        }
        
        # تحميل الإعدادات
        self.load_app_config()
        
        self.logger.info("🚀 بدء تشغيل تطبيق نانو Llama...")

    def initialize_nano_brain(self):
        """تهيئة محرك نانو"""
        
        try:
            self.logger.info("⚡ تحميل محرك نانو Llama...")
            self.nano_brain = NanoLlamaBrain(str(self.data_path))
            self.logger.info("✅ تم تحميل محرك نانو بنجاح!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في تحميل محرك نانو: {e}")
            return False

    def create_web_app(self):
        """إنشاء تطبيق Flask للواجهة الويب"""
        
        if not HAS_FLASK:
            self.logger.warning("Flask غير متوفر - تعطيل الواجهة الويب")
            return None
        
        app = Flask(__name__)
        app.secret_key = 'nano_llama_secret_key_2024'
        
        @app.route('/')
        def home():
            """الصفحة الرئيسية"""
            try:
                # معلومات النظام
                system_status = self.nano_brain.get_system_status() if self.nano_brain else {}
                
                return render_template('nano_llama_interface.html', 
                                     system_status=system_status,
                                     app_stats=self.app_stats)
            except Exception as e:
                self.logger.error(f"خطأ في الصفحة الرئيسية: {e}")
                return f"خطأ: {e}", 500

        @app.route('/chat', methods=['POST'])
        def chat():
            """معالج المحادثة"""
            try:
                data = request.get_json()
                user_input = data.get('message', '').strip()
                
                if not user_input:
                    return jsonify({'error': 'رسالة فارغة'}), 400
                
                if not self.nano_brain:
                    return jsonify({'error': 'محرك نانو غير متاح'}), 500
                
                self.app_stats["web_requests"] += 1
                self.app_stats["total_requests"] += 1
                
                # توليد الاستجابة
                start_time = time.time()
                response = self.nano_brain.generate_response(user_input)
                generation_time = time.time() - start_time
                
                # تحديث الإحصائيات
                if response.confidence > 0.5:
                    self.app_stats["successful_responses"] += 1
                else:
                    self.app_stats["failed_responses"] += 1
                
                # إعداد الاستجابة
                response_data = {
                    'response': response.text,
                    'confidence': response.confidence,
                    'method_used': response.method_used,
                    'emotion_detected': response.emotion_detected,
                    'generation_time': generation_time,
                    'saudi_dialect_score': response.saudi_dialect_score,
                    'personality_mood': response.personality_mood
                }
                
                return jsonify(response_data)
                
            except Exception as e:
                self.logger.error(f"خطأ في المحادثة: {e}")
                self.app_stats["failed_responses"] += 1
                return jsonify({'error': f'خطأ: {str(e)}'}), 500

        @app.route('/status')
        def status():
            """حالة النظام"""
            try:
                if not self.nano_brain:
                    return jsonify({'error': 'محرك نانو غير متاح'}), 500
                
                system_status = self.nano_brain.get_system_status()
                system_status['app_stats'] = self.app_stats
                system_status['app_config'] = self.app_config
                
                return jsonify(system_status)
                
            except Exception as e:
                return jsonify({'error': f'خطأ: {str(e)}'}), 500

        @app.route('/optimize', methods=['POST'])
        def optimize():
            """تحسين النظام"""
            try:
                if not self.nano_brain:
                    return jsonify({'error': 'محرك نانو غير متاح'}), 500
                
                optimization_type = request.get_json().get('type', 'quality')
                
                if optimization_type == 'speed':
                    self.nano_brain.llama_engine.optimize_for_speed()
                    message = "تم تحسين النظام للسرعة"
                elif optimization_type == 'quality':
                    self.nano_brain.llama_engine.optimize_for_quality()
                    message = "تم تحسين النظام للجودة"
                elif optimization_type == 'fine_tune':
                    # تشغيل جلسة تحسين
                    session_result = self.nano_brain.fine_tuner.run_fine_tuning_session(examples_count=50)
                    message = f"تم التحسين بنسبة {session_result.improvement_score:.2%}"
                else:
                    return jsonify({'error': 'نوع تحسين غير مدعوم'}), 400
                
                return jsonify({'message': message, 'success': True})
                
            except Exception as e:
                return jsonify({'error': f'خطأ في التحسين: {str(e)}'}), 500

        @app.route('/model/switch', methods=['POST'])
        def switch_model():
            """تغيير النموذج"""
            try:
                if not self.nano_brain:
                    return jsonify({'error': 'محرك نانو غير متاح'}), 500
                
                model_name = request.get_json().get('model_name')
                if not model_name:
                    return jsonify({'error': 'اسم النموذج مطلوب'}), 400
                
                success = self.nano_brain.llama_engine.switch_model(model_name)
                
                if success:
                    return jsonify({'message': f'تم التبديل إلى {model_name}', 'success': True})
                else:
                    return jsonify({'error': 'فشل في تغيير النموذج'}), 500
                    
            except Exception as e:
                return jsonify({'error': f'خطأ: {str(e)}'}), 500

        @app.route('/reset')
        def reset():
            """إعادة تعيين المحادثة"""
            try:
                if self.nano_brain:
                    self.nano_brain.personality.patience_level = 0.6
                    self.nano_brain.conversation_memory.clear()
                
                flash('تم إعادة تعيين المحادثة بنجاح')
                return redirect(url_for('home'))
                
            except Exception as e:
                flash(f'خطأ في إعادة التعيين: {e}')
                return redirect(url_for('home'))

        return app

    def create_web_template(self):
        """إنشاء قالب HTML للواجهة الويب"""
        
        template_dir = self.data_path.parent / "templates"
        template_dir.mkdir(exist_ok=True)
        
        template_content = """<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نانو Llama - المساعد الذكي السعودي</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.1.3/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .chat-container {
            max-width: 800px;
            margin: 20px auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .chat-header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .chat-messages {
            height: 500px;
            overflow-y: auto;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin: 15px 0;
            padding: 15px;
            border-radius: 15px;
            max-width: 80%;
            animation: fadeIn 0.3s ease-in;
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-right: auto;
            text-align: right;
        }
        .nano-message {
            background: #28a745;
            color: white;
            margin-left: auto;
            text-align: left;
        }
        .message-info {
            font-size: 0.8em;
            opacity: 0.8;
            margin-top: 5px;
        }
        .chat-input {
            padding: 20px;
            background: white;
            border-top: 1px solid #dee2e6;
        }
        .system-status {
            background: rgba(255,255,255,0.1);
            padding: 15px;
            border-radius: 10px;
            margin: 10px;
        }
        .status-card {
            background: white;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .loading {
            display: none;
        }
        .loading.show {
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- الواجهة الرئيسية للمحادثة -->
            <div class="col-md-8">
                <div class="chat-container">
                    <div class="chat-header">
                        <h1><i class="fas fa-robot"></i> نانو Llama</h1>
                        <p>المساعد الذكي السعودي المدعوم بتقنية Llama</p>
                    </div>
                    
                    <div class="chat-messages" id="chatMessages">
                        <div class="nano-message">
                            <div>السلام عليكم! أنا نانو، مساعدك الذكي الجديد المطور بتقنية Llama 🤖</div>
                            <div>أتكلم باللهجة السعودية وأقدر أساعدك في أي شي تحتاجه والله!</div>
                            <div class="message-info">
                                <i class="fas fa-brain"></i> محرك: Llama + شخصية نانو
                                <i class="fas fa-flag"></i> اللهجة: سعودية 🇸🇦
                            </div>
                        </div>
                    </div>
                    
                    <div class="chat-input">
                        <div class="input-group">
                            <input type="text" class="form-control" id="messageInput" 
                                   placeholder="اكتب رسالتك هنا..." 
                                   onkeypress="if(event.key==='Enter') sendMessage()">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                <i class="fas fa-paper-plane"></i>
                                <span class="loading" id="loadingIcon">
                                    <i class="fas fa-spinner fa-spin"></i>
                                </span>
                            </button>
                        </div>
                        
                        <div class="mt-3">
                            <button class="btn btn-outline-success btn-sm" onclick="optimizeSystem('quality')">
                                <i class="fas fa-star"></i> تحسين الجودة
                            </button>
                            <button class="btn btn-outline-warning btn-sm" onclick="optimizeSystem('speed')">
                                <i class="fas fa-bolt"></i> تحسين السرعة  
                            </button>
                            <button class="btn btn-outline-info btn-sm" onclick="fineTune()">
                                <i class="fas fa-cogs"></i> ضبط النموذج
                            </button>
                            <button class="btn btn-outline-danger btn-sm" onclick="resetChat()">
                                <i class="fas fa-refresh"></i> إعادة تعيين
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- لوحة المعلومات -->
            <div class="col-md-4">
                <div class="status-card">
                    <h5><i class="fas fa-info-circle"></i> حالة النظام</h5>
                    <div id="systemStatus">
                        {% if system_status %}
                        <div class="mb-2">
                            <strong>النموذج الحالي:</strong> 
                            {{ system_status.llama_engine.current_model }}
                        </div>
                        <div class="mb-2">
                            <strong>حالة التحميل:</strong> 
                            {% if system_status.llama_engine.model_loaded %}
                                <span class="text-success">محمل ✓</span>
                            {% else %}
                                <span class="text-warning">قيد التحميل...</span>
                            {% endif %}
                        </div>
                        <div class="mb-2">
                            <strong>متوسط درجة السعودية:</strong> 
                            {{ "%.1f%%"|format(system_status.nano_brain.avg_saudi_score * 100) }}
                        </div>
                        <div class="mb-2">
                            <strong>متوسط وقت الاستجابة:</strong> 
                            {{ "%.2f"|format(system_status.nano_brain.avg_response_time) }} ثانية
                        </div>
                        {% endif %}
                    </div>
                </div>
                
                <div class="status-card">
                    <h5><i class="fas fa-chart-bar"></i> إحصائيات التطبيق</h5>
                    <div>
                        <div class="mb-1">مجموع الطلبات: {{ app_stats.total_requests }}</div>
                        <div class="mb-1">نجحت: {{ app_stats.successful_responses }}</div>
                        <div class="mb-1">فشلت: {{ app_stats.failed_responses }}</div>
                        <div class="mb-1">الويب: {{ app_stats.web_requests }}</div>
                    </div>
                </div>
                
                <div class="status-card">
                    <h5><i class="fas fa-cog"></i> النماذج المتاحة</h5>
                    <div id="availableModels">
                        {% if system_status and system_status.llama_engine.available_models %}
                        {% for model in system_status.llama_engine.available_models %}
                        <button class="btn btn-outline-primary btn-sm mb-1" 
                                onclick="switchModel('{{ model }}')"
                                style="display: block; width: 100%;">
                            {{ model }}
                        </button>
                        {% endfor %}
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        async function sendMessage() {
            if (isLoading) return;
            
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            
            if (!message) return;
            
            isLoading = true;
            document.getElementById('loadingIcon').classList.add('show');
            
            // إضافة رسالة المستخدم
            addMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: message })
                });
                
                if (!response.ok) {
                    throw new Error('خطأ في الشبكة');
                }
                
                const data = await response.json();
                
                // إضافة رد نانو
                addNanoMessage(data);
                
            } catch (error) {
                addMessage('عذراً، حدث خطأ: ' + error.message, 'nano', true);
            } finally {
                isLoading = false;
                document.getElementById('loadingIcon').classList.remove('show');
            }
        }
        
        function addMessage(text, sender, isError = false) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            if (isError) messageDiv.style.backgroundColor = '#dc3545';
            
            messageDiv.innerHTML = `
                <div>${text}</div>
                <div class="message-info">
                    <i class="fas fa-clock"></i> ${new Date().toLocaleTimeString('ar-SA')}
                </div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function addNanoMessage(data) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message nano-message';
            
            messageDiv.innerHTML = `
                <div>${data.response}</div>
                <div class="message-info">
                    <i class="fas fa-brain"></i> ${data.method_used}
                    <i class="fas fa-chart-line"></i> ثقة: ${(data.confidence * 100).toFixed(1)}%
                    <i class="fas fa-flag"></i> سعودي: ${(data.saudi_dialect_score * 100).toFixed(1)}%
                    <i class="fas fa-clock"></i> ${data.generation_time.toFixed(2)}ث
                </div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        async function optimizeSystem(type) {
            try {
                const response = await fetch('/optimize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ type: type })
                });
                
                const data = await response.json();
                if (data.success) {
                    addMessage(data.message, 'nano');
                } else {
                    addMessage('خطأ في التحسين: ' + data.error, 'nano', true);
                }
            } catch (error) {
                addMessage('خطأ في التحسين: ' + error.message, 'nano', true);
            }
        }
        
        async function fineTune() {
            addMessage('بدء عملية الضبط الدقيق للنموذج... قد تستغرق دقائق', 'nano');
            await optimizeSystem('fine_tune');
        }
        
        async function switchModel(modelName) {
            try {
                const response = await fetch('/model/switch', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ model_name: modelName })
                });
                
                const data = await response.json();
                addMessage(data.success ? data.message : data.error, 'nano', !data.success);
            } catch (error) {
                addMessage('خطأ في تغيير النموذج: ' + error.message, 'nano', true);
            }
        }
        
        function resetChat() {
            if (confirm('هل تريد إعادة تعيين المحادثة؟')) {
                window.location.href = '/reset';
            }
        }
        
        // تحديث حالة النظام كل 30 ثانية
        setInterval(async function() {
            try {
                const response = await fetch('/status');
                const data = await response.json();
                // تحديث العرض هنا إذا أردت
            } catch (error) {
                console.log('خطأ في تحديث الحالة:', error);
            }
        }, 30000);
    </script>
</body>
</html>"""
        
        template_path = template_dir / "nano_llama_interface.html"
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        self.logger.info("تم إنشاء قالب الواجهة الويب")

    def run_terminal_interface(self):
        """تشغيل واجهة المحطة الطرفية"""
        
        print("\n" + "="*60)
        print("🤖 مرحباً بك في نانو Llama - المساعد الذكي السعودي!")
        print("="*60)
        
        if not self.nano_brain:
            print("❌ خطأ: محرك نانو غير متاح")
            return
        
        print("\n💡 أوامر خاصة:")
        print("  /help - عرض المساعدة")
        print("  /status - حالة النظام")
        print("  /optimize - تحسين النظام")
        print("  /reset - إعادة تعيين المحادثة")
        print("  /quit - إنهاء البرنامج")
        print("\n🎯 ابدأ المحادثة:")
        
        while True:
            try:
                user_input = input("\n👤 أنت: ").strip()
                
                if not user_input:
                    continue
                
                # معالجة الأوامر الخاصة
                if user_input.startswith('/'):
                    if user_input == '/quit':
                        print("👋 مع السلامة!")
                        break
                    elif user_input == '/help':
                        self.show_help()
                        continue
                    elif user_input == '/status':
                        self.show_status()
                        continue
                    elif user_input == '/optimize':
                        self.run_optimization_menu()
                        continue
                    elif user_input == '/reset':
                        self.nano_brain.conversation_memory.clear()
                        print("✅ تم إعادة تعيين المحادثة")
                        continue
                    else:
                        print("❓ أمر غير معروف. اكتب /help للمساعدة")
                        continue
                
                # معالجة الرسالة العادية
                self.app_stats["terminal_requests"] += 1
                self.app_stats["total_requests"] += 1
                
                print("🤔 نانو يفكر...")
                start_time = time.time()
                
                response = self.nano_brain.generate_response(user_input)
                generation_time = time.time() - start_time
                
                # عرض الرد
                print(f"\n🤖 نانو: {response.text}")
                
                # عرض التفاصيل
                print(f"\n📊 تفاصيل الرد:")
                print(f"   🎯 الطريقة: {response.method_used}")
                print(f"   📈 الثقة: {response.confidence:.1%}")
                print(f"   🇸🇦 السعودية: {response.saudi_dialect_score:.1%}")
                print(f"   ⏱️  الوقت: {generation_time:.2f} ثانية")
                print(f"   😊 المزاج: {response.personality_mood}")
                
                # تحديث الإحصائيات
                if response.confidence > 0.5:
                    self.app_stats["successful_responses"] += 1
                else:
                    self.app_stats["failed_responses"] += 1
                    
            except KeyboardInterrupt:
                print("\n\n👋 تم إيقاف البرنامج بواسطة المستخدم")
                break
            except Exception as e:
                print(f"\n❌ خطأ: {e}")
                self.app_stats["failed_responses"] += 1

    def show_help(self):
        """عرض المساعدة"""
        
        help_text = """
🔍 دليل الاستخدام - نانو Llama

📝 الأوامر المتاحة:
  /help      - عرض هذه المساعدة
  /status    - عرض حالة النظام والإحصائيات  
  /optimize  - قائمة خيارات التحسين
  /reset     - إعادة تعيين المحادثة
  /quit      - إنهاء البرنامج

💬 المحادثة العادية:
  - اكتب أي رسالة وسيرد عليك نانو باللهجة السعودية
  - نانو يتعلم من محادثاتك ويحسن أداءه تلقائياً
  - يمكنك سؤاله عن أي شيء أو طلب المساعدة

🚀 مميزات متقدمة:
  - يستخدم تقنية Llama للذكاء المتقدم
  - محسن خصيصاً للهجة السعودية
  - يتكيف مع شخصيتك وطريقة كلامك
  - نظام تحسين وضبط تلقائي

💡 نصائح:
  - كن طبيعياً في الكلام
  - جرب أنواع مختلفة من الأسئلة
  - استخدم /optimize لتحسين الأداء
        """
        print(help_text)

    def show_status(self):
        """عرض حالة النظام"""
        
        if not self.nano_brain:
            print("❌ محرك نانو غير متاح")
            return
        
        try:
            status = self.nano_brain.get_system_status()
            
            print("\n" + "="*50)
            print("📊 حالة النظام")
            print("="*50)
            
            # معلومات Llama
            llama_info = status.get('llama_engine', {})
            print(f"🧠 محرك Llama:")
            print(f"   📦 النموذج: {llama_info.get('current_model', 'غير محدد')}")
            print(f"   ✅ محمل: {'نعم' if llama_info.get('model_loaded') else 'لا'}")
            print(f"   🚀 النمط البديل: {'نعم' if llama_info.get('fallback_mode') else 'لا'}")
            
            # إحصائيات الاستخدام
            usage_stats = llama_info.get('usage_stats', {})
            print(f"\n📈 إحصائيات الاستخدام:")
            print(f"   📝 مجموع الطلبات: {usage_stats.get('total_requests', 0)}")
            print(f"   ✅ ناجحة: {usage_stats.get('successful_responses', 0)}")
            print(f"   ❌ فاشلة: {usage_stats.get('failed_responses', 0)}")
            print(f"   ⏱️  متوسط الوقت: {usage_stats.get('avg_response_time', 0):.2f} ثانية")
            print(f"   🇸🇦 متوسط السعودية: {usage_stats.get('avg_saudi_score', 0):.1%}")
            
            # معلومات الشخصية
            personality = status.get('personality', {})
            print(f"\n😊 الشخصية:")
            print(f"   🎭 المزاج: {personality.get('current_mood', 'غير محدد')}")
            print(f"   💪 مستوى العناد: {personality.get('stubbornness_level', 0):.1%}")
            print(f"   ⚡ مستوى الطاقة: {personality.get('energy_level', 0):.1%}")
            
            # إحصائيات التطبيق
            print(f"\n📱 إحصائيات التطبيق:")
            print(f"   🌐 طلبات الويب: {self.app_stats['web_requests']}")
            print(f"   💻 طلبات المحطة: {self.app_stats['terminal_requests']}")
            print(f"   ⏰ وقت التشغيل: {datetime.now() - self.app_stats['start_time']}")
            
        except Exception as e:
            print(f"❌ خطأ في عرض الحالة: {e}")

    def run_optimization_menu(self):
        """قائمة التحسين"""
        
        print("\n🔧 خيارات التحسين:")
        print("1. تحسين للجودة")
        print("2. تحسين للسرعة") 
        print("3. ضبط دقيق للنموذج")
        print("4. تبديل النموذج")
        print("0. العودة")
        
        choice = input("\nاختر رقم: ").strip()
        
        if choice == '1':
            print("⚙️ جاري التحسين للجودة...")
            self.nano_brain.llama_engine.optimize_for_quality()
            print("✅ تم التحسين للجودة!")
            
        elif choice == '2':
            print("⚙️ جاري التحسين للسرعة...")
            self.nano_brain.llama_engine.optimize_for_speed()
            print("✅ تم التحسين للسرعة!")
            
        elif choice == '3':
            print("⚙️ بدء الضبط الدقيق... قد يستغرق دقائق")
            session = self.nano_brain.fine_tuner.run_fine_tuning_session(examples_count=50)
            print(f"✅ تم الضبط الدقيق! تحسن بنسبة: {session.improvement_score:.2%}")
            
        elif choice == '4':
            self.show_model_switch_menu()
            
        elif choice == '0':
            return
        else:
            print("❓ خيار غير صحيح")

    def show_model_switch_menu(self):
        """قائمة تبديل النماذج"""
        
        try:
            available_models = list(self.nano_brain.llama_engine.available_models.keys())
            
            print("\n🔄 النماذج المتاحة:")
            for i, model in enumerate(available_models, 1):
                model_info = self.nano_brain.llama_engine.available_models[model]
                print(f"{i}. {model} - {model_info['description']}")
            
            print("0. العودة")
            
            choice = input("\nاختر النموذج: ").strip()
            
            if choice == '0':
                return
            
            try:
                model_index = int(choice) - 1
                if 0 <= model_index < len(available_models):
                    model_name = available_models[model_index]
                    print(f"⚙️ جاري التبديل إلى {model_name}...")
                    
                    success = self.nano_brain.llama_engine.switch_model(model_name)
                    if success:
                        print(f"✅ تم التبديل إلى {model_name}!")
                    else:
                        print(f"❌ فشل التبديل إلى {model_name}")
                else:
                    print("❓ رقم النموذج غير صحيح")
            except ValueError:
                print("❓ يجب إدخال رقم صحيح")
                
        except Exception as e:
            print(f"❌ خطأ في عرض النماذج: {e}")

    def start_web_server(self):
        """بدء خادم الويب"""
        
        if not HAS_FLASK:
            return False
        
        try:
            # إنشاء قالب الواجهة
            self.create_web_template()
            
            # إنشاء تطبيق Flask
            app = self.create_web_app()
            
            # بدء الخادم
            self.web_server = make_server('127.0.0.1', self.app_config['port'], app, threaded=True)
            
            self.logger.info(f"🌐 تم بدء الخادم على http://127.0.0.1:{self.app_config['port']}")
            
            # تشغيل الخادم في خيط منفصل
            import threading
            server_thread = threading.Thread(target=self.web_server.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ خطأ في بدء الخادم: {e}")
            return False

    def load_app_config(self):
        """تحميل إعدادات التطبيق"""
        
        config_path = self.data_path / "app_config.json"
        
        if config_path.exists():
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    saved_config = json.load(f)
                    self.app_config.update(saved_config)
            except Exception as e:
                self.logger.warning(f"خطأ في تحميل الإعدادات: {e}")

    def save_app_config(self):
        """حفظ إعدادات التطبيق"""
        
        try:
            config_path = self.data_path / "app_config.json"
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.app_config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.logger.error(f"خطأ في حفظ الإعدادات: {e}")

    def run(self):
        """تشغيل التطبيق"""
        
        self.logger.info("🚀 بدء تشغيل نانو Llama...")
        
        # تهيئة محرك نانو
        if not self.initialize_nano_brain():
            print("❌ فشل في تحميل محرك نانو")
            return False
        
        self.is_running = True
        
        # بدء الخادم الويب إذا مطلوب
        web_started = False
        if self.app_config["web_interface"]:
            web_started = self.start_web_server()
            if web_started:
                print(f"🌐 الواجهة الويب متاحة على: http://127.0.0.1:{self.app_config['port']}")
        
        # تشغيل واجهة المحطة إذا مطلوب
        if self.app_config["terminal_interface"]:
            try:
                self.run_terminal_interface()
            except KeyboardInterrupt:
                print("\n👋 تم إيقاف البرنامج")
        
        # حفظ البيانات عند الإنهاء
        self.cleanup()
        return True

    def cleanup(self):
        """تنظيف الموارد"""
        
        self.logger.info("🧹 تنظيف الموارد...")
        
        # حفظ الإعدادات
        self.save_app_config()
        
        # حفظ حالة نانو
        if self.nano_brain:
            self.nano_brain.save_brain_state()
        
        # إيقاف الخادم
        if self.web_server:
            self.web_server.shutdown()
        
        self.logger.info("✅ تم تنظيف الموارد بنجاح")

def main():
    """الدالة الرئيسية"""
    
    print("🤖 نانو Llama - المساعد الذكي السعودي المطور")
    print("   مدعوم بتقنية Llama المجانية 🆓")
    print("   للحصول على أفضل تجربة، تأكد من:")
    print("   - تثبيت مكتبة transformers")
    print("   - توفر ذاكرة كافية لتحميل النماذج")
    print("   - اتصال بالإنترنت لتحميل النماذج لأول مرة")
    print()
    
    try:
        # إنشاء وتشغيل التطبيق
        app = NanoLlamaApp()
        success = app.run()
        
        if not success:
            print("❌ فشل في تشغيل التطبيق")
            return 1
        
        return 0
        
    except KeyboardInterrupt:
        print("\n👋 تم إيقاف البرنامج بواسطة المستخدم")
        return 0
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)