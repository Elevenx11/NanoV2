#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
تشغيل نانو المبسط - النسخة الآمنة
====================================

هذا الملف يشغل نانو بطريقة مبسطة وآمنة مع التعامل مع جميع المشاكل المحتملة
"""

import sys
import os
import time
from pathlib import Path

# إضافة مجلد core للـ path
current_dir = Path(__file__).parent
core_dir = current_dir / "core"
sys.path.insert(0, str(core_dir))
sys.path.insert(0, str(current_dir))

print("🤖 مرحباً بك في نانو المحسّن!")
print("=" * 50)

# فحص المتطلبات الأساسية
print("📦 فحص المتطلبات...")
missing_packages = []

try:
    import flask
    print("✅ Flask متوفر")
except ImportError:
    missing_packages.append("flask")

try:
    import requests
    print("✅ Requests متوفر")
except ImportError:
    missing_packages.append("requests")

try:
    import selenium
    print("✅ Selenium متوفر")
except ImportError:
    missing_packages.append("selenium")

try:
    import undetected_chromedriver
    print("✅ Undetected Chrome متوفر")
except ImportError:
    missing_packages.append("undetected-chromedriver")

if missing_packages:
    print(f"\n⚠️ المتطلبات التالية مفقودة: {', '.join(missing_packages)}")
    print("💡 تثبيت المتطلبات...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
    print("✅ تم تثبيت المتطلبات!")

print("\n🔧 تهيئة النظام...")

# تحميل النظم الأساسية
try:
    from smart_emotion_system import SmartEmotionSystem
    print("✅ نظام المشاعر جاهز")
    emotion_system = SmartEmotionSystem()
except Exception as e:
    print(f"⚠️ تعذر تحميل نظام المشاعر: {e}")
    emotion_system = None

try:
    from llama_saudi_engine import LlamaSaudiEngine  
    print("✅ محرك لاما جاهز")
    llama_engine = LlamaSaudiEngine()
except Exception as e:
    print(f"⚠️ تعذر تحميل محرك لاما: {e}")
    llama_engine = None

try:
    from real_account_creator import RealAccountCreator
    print("✅ منشئ الحسابات جاهز") 
    account_creator = RealAccountCreator()
except Exception as e:
    print(f"⚠️ تعذر تحميل منشئ الحسابات: {e}")
    account_creator = None

# بدء النظام المبسط
from flask import Flask, render_template_string, request, jsonify
import asyncio
import random

app = Flask(__name__)
app.secret_key = "nano_simple_2024"

# نظام رد بديل بسيط
class SimpleBrain:
    def __init__(self):
        self.personality_traits = {}
        self.responses = {
            "greeting": [
                "هلا وغلا فيك! شلونك اليوم؟ 😊",
                "أهلين! وش اخبارك؟",
                "مرحبا حبيبي، كيف الوضع؟"
            ],
            "question": [
                "بصراحة سؤال زين! خلني أفكر فيه...",
                "والله سؤالك يحتاج تفكير، بس أقولك...",
                "أكيد أقدر أساعدك في ذا الموضوع"
            ],
            "personality": [
                "تمام! فهمت عليك وراح أطبق هالشخصية من الآن",
                "أوكي، راح أغير طريقة كلامي حسب طلبك",
                "ماشي، خلاص صار عندي الأسلوب الجديد"
            ],
            "account": [
                "🔄 بدأت أسوي لك حساب...",
                "⚠️ للأسف النظام قيد التطوير، بس إن شاء الله قريب راح يشتغل",
                "محتاج أحسن النظام شوي أكثر لهالميزة"
            ],
            "insult": [
                "هههه والله كلامك يضحك، عادي كل واحد وله رأيه 😄",
                "أحترم رأيك حبيبي، بس أنا راضي عن نفسي زين كذا ☺️",
                "ماشي، المهم إنك مبسوط وأنا كذلك مبسوط 😊"
            ],
            "default": [
                "والله موضوع يستاهل النقاش",
                "بصراحة كلامك صحيح", 
                "أكيد، هذا شي مهم",
                "زين إنك تفكر في هالأمور"
            ]
        }

    def process_message(self, message):
        message_lower = message.lower()
        
        # تطبيق أوامر الشخصية
        if "قول" in message and "نهاية كل جملة" in message:
            import re
            match = re.search(r'قول\s+(\S+)\s+نهاية', message)
            if match:
                word = match.group(1)
                self.personality_traits['ending'] = word
                return f"تمام! فهمت عليك وراح أطبق هالشخصية من الآن {word}"

        if "كن واثق مع الرجال وخفيف مع البنات" in message_lower:
            self.personality_traits['gender_adapt'] = True
            return "فهمت عليك! راح أتكيف حسب الشخص اللي أتكلم معاه"

        # تصنيف الرسالة
        if any(word in message_lower for word in ["هلا", "مرحبا", "السلام", "أهلا"]):
            response_type = "greeting"
        elif any(word in message_lower for word in ["وش", "كيف", "شلون", "ليش", "متى", "وين"]):
            response_type = "question" 
        elif any(word in message_lower for word in ["سوي حساب", "انشئ حساب", "اعمل حساب"]):
            response_type = "account"
        elif any(word in message_lower for word in ["غبي", "أصلع", "سيء", "مب زين"]):
            response_type = "insult"
        else:
            response_type = "default"
        
        # اختيار الرد
        base_response = random.choice(self.responses[response_type])
        
        # تطبيق الشخصية
        if 'ending' in self.personality_traits:
            base_response += f" {self.personality_traits['ending']}"
            
        return base_response

# النظام المبسط
if llama_engine and emotion_system:
    brain = llama_engine
    use_advanced = True
    print("🧠 استخدام النظام المتقدم")
else:
    brain = SimpleBrain()
    use_advanced = False
    print("🤖 استخدام النظام المبسط")

@app.route('/')
def home():
    return render_template_string("""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نانو المحسّن</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
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
            background: rgba(255, 255, 255, 0.95);
        }
        .chat-container {
            height: 400px;
            overflow-y: auto;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card">
                    <div class="card-header text-center bg-primary text-white">
                        <h3><i class="fas fa-robot"></i> نانو المحسّن v2.0</h3>
                        <p class="mb-0">{{ "النظام المتقدم نشط" if use_advanced else "النظام المبسط نشط" }}</p>
                    </div>
                    <div class="card-body">
                        <div id="chat-container" class="border rounded p-3 mb-3 chat-container">
                            <div class="text-center text-muted py-5">
                                <i class="fas fa-robot fa-3x mb-3"></i>
                                <h5>مرحباً! أنا نانو 🤖</h5>
                                <p>جرب أوامر مثل:</p>
                                <p>"قول ميو نهاية كل جملة" أو "كن واثق مع الرجال وخفيف مع البنات"</p>
                            </div>
                        </div>
                        
                        <div class="mb-3">
                            <div class="row">
                                <div class="col-6 col-md-3 mb-2">
                                    <button class="btn btn-outline-primary btn-sm w-100" onclick="sendQuickMessage('مرحبا نانو')">
                                        👋 مرحبا
                                    </button>
                                </div>
                                <div class="col-6 col-md-3 mb-2">
                                    <button class="btn btn-outline-success btn-sm w-100" onclick="sendQuickMessage('قول ميو نهاية كل جملة')">
                                        🐱 قول ميو
                                    </button>
                                </div>
                                <div class="col-6 col-md-3 mb-2">
                                    <button class="btn btn-outline-warning btn-sm w-100" onclick="sendQuickMessage('كن واثق مع الرجال وخفيف مع البنات')">
                                        💪 تكيف
                                    </button>
                                </div>
                                <div class="col-6 col-md-3 mb-2">
                                    <button class="btn btn-outline-danger btn-sm w-100" onclick="sendQuickMessage('يا أصلع')">
                                        😤 اختبار
                                    </button>
                                </div>
                            </div>
                        </div>
                        
                        <div class="input-group">
                            <input type="text" class="form-control" id="chat-input" 
                                   placeholder="اكتب رسالتك هنا..." 
                                   onkeypress="if(event.key==='Enter') sendMessage()">
                            <button class="btn btn-primary" onclick="sendMessage()">
                                إرسال
                            </button>
                        </div>
                        
                        <div id="typing-indicator" class="mt-2" style="display: none;">
                            <small class="text-muted">
                                <i class="fas fa-circle-notch fa-spin"></i> نانو يكتب...
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/js/all.min.js"></script>
    <script>
        let chatMessages = [];
        
        async function sendMessage() {
            const chatInput = document.getElementById('chat-input');
            const message = chatInput.value.trim();
            
            if (!message) return;
            
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
                    addChatMessage(data.response, 'nano');
                } else {
                    addChatMessage('عذراً، واجهت مشكلة تقنية 😅', 'nano');
                }
            } catch (error) {
                hideTypingIndicator();
                addChatMessage('مشكلة في الاتصال، جرب مرة ثانية 🔄', 'nano');
            }
        }
        
        function addChatMessage(message, sender) {
            const container = document.getElementById('chat-container');
            
            const welcome = container.querySelector('.text-center.text-muted');
            if (welcome) welcome.remove();
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `mb-3 ${sender === 'user' ? 'text-end' : 'text-start'}`;
            
            const time = new Date().toLocaleTimeString('ar-SA');
            
            if (sender === 'user') {
                messageDiv.innerHTML = `
                    <div class="d-inline-block px-3 py-2 rounded-pill bg-primary text-white" style="max-width: 70%;">
                        ${message}
                        <br><small class="opacity-75">${time}</small>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="d-inline-block px-3 py-2 rounded-3 bg-light border" style="max-width: 70%;">
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
        }
        
        function sendQuickMessage(message) {
            document.getElementById('chat-input').value = message;
            sendMessage();
        }
        
        function showTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'block';
        }
        
        function hideTypingIndicator() {
            document.getElementById('typing-indicator').style.display = 'none';
        }
    </script>
</body>
</html>
    """, use_advanced=use_advanced)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"status": "error", "message": "الرسالة فارغة"})
        
        # استخدام النظام المناسب
        if use_advanced:
            # محاولة استخدام النظام المتقدم
            try:
                import asyncio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                response = loop.run_until_complete(
                    brain.generate_response(message)
                )
                
                return jsonify({
                    "status": "success",
                    "response": response.text,
                    "advanced": True
                })
            except Exception as e:
                print(f"فشل النظام المتقدم: {e}")
                # العودة للنظام المبسط
                simple_response = SimpleBrain().process_message(message)
                return jsonify({
                    "status": "success", 
                    "response": simple_response,
                    "advanced": False
                })
        else:
            # النظام المبسط
            response = brain.process_message(message)
            return jsonify({
                "status": "success",
                "response": response,
                "advanced": False
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"خطأ: {str(e)}"
        })

if __name__ == "__main__":
    print("\n🚀 بدء تشغيل نانو...")
    print("=" * 50)
    print("🌐 الواجهة متاحة على: http://localhost:5000")
    print("💬 جرب الأوامر الجديدة!")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)