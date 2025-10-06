# nano_smart_response.py - نظام الردود الذكي والمتطور لنانو - الإصدار النهائي
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

class NanoSmartResponse:
    """نظام الردود الذكي والمتطور لنانو - الإصدار النهائي"""
    
    def __init__(self):
        self.knowledge_base = self.initialize_knowledge_base()
        self.conversation_context = []
        
    def initialize_knowledge_base(self) -> Dict:
        """قاعدة المعرفة الشاملة لنانو"""
        return {
            "geography": {
                "عاصمة_السعودية": "الرياض هي عاصمة المملكة العربية السعودية الحبيبة 🏛️🇸🇦",
                "مدن_رئيسية": {
                    "الرياض": "عاصمة المملكة ومركز الاقتصاد والسياسة",
                    "جدة": "عروس البحر الأحمر وبوابة الحرمين الشريفين",
                    "مكة المكرمة": "أقدس بقاع الأرض وقبلة المسلمين",
                    "المدينة المنورة": "مدينة الرسول ﷺ والمسجد النبوي الشريف",
                    "الدمام": "عاصمة المنطقة الشرقية ومركز البترول",
                    "الطائف": "مصيف المملكة ومدينة الورد والعسل"
                }
            },
            
            "religion": {
                "أذكار_صباح_مساء": [
                    "أعوذ بالله من الشيطان الرجيم، بسم الله الرحمن الرحيم",
                    "سبحان الله وبحمده، سبحان الله العظيم",
                    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
                    "اللهم صل وسلم وبارك على نبينا محمد",
                    "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
                    "الحمد لله رب العالمين، الرحمن الرحيم، مالك يوم الدين",
                    "لا حول ولا قوة إلا بالله العلي العظيم"
                ],
                "أدعية_مأثورة": [
                    "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار",
                    "اللهم اهدني فيمن هديت، وعافني فيمن عافيت، وتولني فيمن توليت",
                    "اللهم أعني على ذكرك وشكرك وحسن عبادتك",
                    "اللهم اغفر لي ذنبي وخطئي وجهلي",
                    "رب اشرح لي صدري ويسر لي أمري",
                    "اللهم إنك عفو تحب العفو فاعف عني"
                ]
            },
            
            "congratulations": {
                "ترقية": [
                    "ألف مبروك الترقية! الله يبارك لك ويزيدك من فضله 🎉",
                    "تستاهل كل خير، مبروك الترقية وإن شاء الله دايماً للأمام 📈",
                    "الله يكرمك! مبروك الترقية وعقبال المناصب الأعلى 🚀",
                    "عقبال ما تصير مدير عام! مبروك الترقية وبالتوفيق 💼"
                ],
                "نجاح": [
                    "ألف مبروك النجاح! تعبك وسهرك ما راح سدى 📚",
                    "الله يبارك لك، مبروك النجاح وعقبال درجات أعلى ✨",
                    "تستاهل كل خير، مبروك النجاح والتفوق 🏆",
                    "فرحتك فرحتنا! مبروك النجاح وإن شاء الله المستقبل أحلى 🌟"
                ],
                "زواج": [
                    "ألف مبروك! الله يبارك لكم ويجمع بينكم في خير 💍",
                    "مبروك الزواج، الله يتمم عليكم بالخير والبركة 💒",
                    "بالرفاه والبنين، مبروك الزواج السعيد ❤️",
                    "عقبال فرحة الأولاد! مبروك الزواج 👶"
                ]
            },
            
            "general_knowledge": {
                "نانو_معلومات": {
                    "الاسم": "أنا نانو، مساعدك الذكي باللهجة السعودية الأصيلة! 🤖",
                    "المهام": [
                        "📚 الإجابة على الأسئلة العامة والثقافية",
                        "🗺️ معلومات عن المملكة العربية السعودية",
                        "🤲 تذكير بالأذكار والأدعية المأثورة",
                        "🎉 تهنئة بالمناسبات السعيدة والإنجازات",
                        "💬 محادثة ودردشة ممتعة ومفيدة",
                        "⏰ معرفة الوقت والتاريخ الحالي",
                        "🧠 نصائح وحلول للمشاكل اليومية",
                        "😊 دعم نفسي وتحفيز إيجابي"
                    ]
                }
            }
        }
    
    def detect_intent_advanced(self, text: str) -> Tuple[str, float]:
        """تحديد نية المستخدم المتقدم"""
        text_clean = text.lower().strip()
        
        # أنماط محددة بدقة أكبر
        patterns = {
            "geography_question": [
                r"وش عاصمة|إيش عاصمة|عاصمة السعودية|عاصمة المملكة",
                r"مدن سعودية|مدن المملكة|أهم المدن",
                r"وين الرياض|وين جدة|وين مكة|معلومات عن"
            ],
            "time_question": [
                r"كم الساعة|وش الوقت|الوقت الحين|الساعة كم",
                r"أي يوم|اليوم شنو|التاريخ|تاريخ اليوم"
            ],
            "personal_question": [
                r"مين انت|من انت|شنو اسمك|اسمك إيش",
                r"تعريف نفسك|وش تقدر تسوي|قدراتك|مهاراتك"
            ],
            "religious_request": [
                r"اذكر ربك|قول ذكر|أذكار|تسبيح|استغفار",
                r"ادع لي|ادعي لي|دعاء|اللهم|ربنا",
                r"آية|حديث|قرآن|سورة"
            ],
            "congratulation": [
                r"ترقيت|اترقيت|حصلت على ترقية|ترقوني|رقوني",
                r"نجحت|تخرجت|نجاحي|تخرجي|خلصت الجامعة",
                r"تزوجت|خطبت|عرسي|زواجي|خطوبتي",
                r"حصلت على|فزت|ربحت|حققت"
            ],
            "greeting": [
                r"صباح الخير|مساء الخير|أهلا|مرحبا|هلا|السلام عليكم",
                r"كيف الحال|كيفك|شلونك|إيش أخبارك"
            ],
            "farewell": [
                r"باي|وداع|الله معك|تصبح على خير|في أمان الله",
                r"مع السلامة|خلاص|يلا باي"
            ],
            "gratitude": [
                r"شكرا|شكراً|يعطيك العافية|جزاك الله خير|الله يكرمك",
                r"تسلم|ما قصرت|كثر خيرك"
            ],
            "emotion_sad": [
                r"تعبان|زعلان|حزين|مكتئب|ضايق|متضايق",
                r"مو مرتاح|حاسس بضيق|صدري ضايق"
            ],
            "emotion_happy": [
                r"فرحان|مبسوط|سعيد|مرتاح|منبسط|متحمس",
                r"حاسس بفرحة|الحمدلله مرتاح"
            ],
            "need_help": [
                r"ساعدني|محتاج مساعدة|أبي مساعدة|تقدر تساعدني",
                r"ما أدري وش أسوي|ما عندي شي أسويه|ملل|زهق"
            ]
        }
        
        # البحث عن التطابقات
        for intent, pattern_list in patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, text_clean):
                    confidence = 0.95 if len(re.findall(pattern, text_clean)) > 0 else 0.8
                    return intent, confidence
        
        # إذا لم نجد تطابق محدد، نحدد بناء على الكلمات المفتاحية
        if "?" in text or "؟" in text:
            return "general_question", 0.7
        
        return "general_conversation", 0.5
    
    def generate_smart_response(self, user_input: str) -> str:
        """توليد الرد الذكي والمناسب"""
        intent, confidence = self.detect_intent_advanced(user_input)
        
        # إضافة السياق للمحادثة
        self.conversation_context.append({
            "user_input": user_input,
            "intent": intent,
            "confidence": confidence,
            "timestamp": datetime.now()
        })
        
        # توليد الرد المناسب
        if intent == "geography_question":
            return self.handle_geography_question(user_input)
        elif intent == "time_question":
            return self.handle_time_question(user_input)
        elif intent == "personal_question":
            return self.handle_personal_question(user_input)
        elif intent == "religious_request":
            return self.handle_religious_request(user_input)
        elif intent == "congratulation":
            return self.handle_congratulation(user_input)
        elif intent == "greeting":
            return self.handle_greeting(user_input)
        elif intent == "farewell":
            return self.handle_farewell(user_input)
        elif intent == "gratitude":
            return self.handle_gratitude(user_input)
        elif intent == "emotion_sad":
            return self.handle_sad_emotion(user_input)
        elif intent == "emotion_happy":
            return self.handle_happy_emotion(user_input)
        elif intent == "need_help":
            return self.handle_help_request(user_input)
        elif intent == "general_question":
            return self.handle_general_question(user_input)
        else:
            return self.handle_general_conversation(user_input)
    
    def handle_geography_question(self, text: str) -> str:
        """التعامل مع أسئلة الجغرافيا"""
        text_lower = text.lower()
        
        if "عاصمة" in text_lower and ("سعود" in text_lower or "مملكة" in text_lower):
            return self.knowledge_base["geography"]["عاصمة_السعودية"]
        
        cities = self.knowledge_base["geography"]["مدن_رئيسية"]
        
        for city, description in cities.items():
            if city in text_lower or any(part in text_lower for part in city.split()):
                return f"🏙️ {city}: {description}"
        
        if "مدن" in text_lower:
            city_list = ", ".join(list(cities.keys())[:4])
            return f"من أهم مدن المملكة: {city_list} وغيرها الكثير من المدن الجميلة 🇸🇦"
        
        return "المملكة العربية السعودية بلد واسع وجميل، فيه مدن ومحافظات كثيرة كل وحدة لها طابعها الخاص 🗺️"
    
    def handle_time_question(self, text: str) -> str:
        """التعامل مع أسئلة الوقت"""
        current_time = datetime.now()
        
        if any(word in text.lower() for word in ["ساعة", "وقت"]):
            time_str = current_time.strftime("%H:%M")
            # تحديد فترة اليوم
            hour = current_time.hour
            if 5 <= hour < 12:
                period = "صباح الخير! ☀️"
            elif 12 <= hour < 17:
                period = "ظهرك سعيد! 🌤️"
            elif 17 <= hour < 20:
                period = "مساء الخير! 🌅"
            else:
                period = "مساء الخير! 🌙"
            
            return f"{period}\nالوقت الحين الساعة {time_str} 🕐"
        
        if "يوم" in text.lower() or "تاريخ" in text.lower():
            date_str = current_time.strftime("%Y-%m-%d")
            # أسماء الأيام بالعربي
            days = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"]
            day_name = days[current_time.weekday()]
            return f"اليوم {day_name} الموافق {date_str} 📅"
        
        return f"الوقت: {current_time.strftime('%H:%M')} والتاريخ: {current_time.strftime('%Y-%m-%d')} ⏰"
    
    def handle_personal_question(self, text: str) -> str:
        """التعامل مع الأسئلة الشخصية عن نانو"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["مين", "اسم", "من انت", "تعريف"]):
            return self.knowledge_base["general_knowledge"]["نانو_معلومات"]["الاسم"] + \
                   "\nهنا عشان أساعدك في أي شي تحتاجه، من معلومات لأسئلة لحتى محادثة حلوة ☕"
        
        if any(word in text_lower for word in ["تقدر", "مهارات", "قدرات"]):
            tasks = self.knowledge_base["general_knowledge"]["نانو_معلومات"]["المهام"]
            task_list = "\n".join(tasks)
            return f"أقدر أساعدك في أشياء كثيرة:\n\n{task_list}\n\nوأشياء كثيرة ثانية! جرب أسألني أي شي 😊"
        
        return "أنا هنا عشانك! أسألني أي شي تبي تعرفه أو تحتاج مساعدة فيه 😊"
    
    def handle_religious_request(self, text: str) -> str:
        """التعامل مع الطلبات الدينية"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["اذكر", "ذكر", "تسبيح", "أذكار"]):
            dhikr = random.choice(self.knowledge_base["religion"]["أذكار_صباح_مساء"])
            return f"إليك هذا الذكر المبارك:\n\n🤲 {dhikr}\n\nجعله الله في ميزان حسناتك"
        
        if any(word in text_lower for word in ["ادع", "دعاء", "اللهم", "ربنا"]):
            dua = random.choice(self.knowledge_base["religion"]["أدعية_مأثورة"])
            return f"اللهم آمين:\n\n🤲 {dua}\n\nاللهم استجب دعاءنا وتقبل منا"
        
        if "استغفار" in text_lower:
            return "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه\n\n🤲 اللهم اغفر لنا ذنوبنا وتقبل توبتنا"
        
        return "بارك الله فيك على هذا السؤال الطيب 🤲\nاللهم اهدنا واهد بنا واجعلنا سبباً لمن اهتدى"
    
    def handle_congratulation(self, text: str) -> str:
        """التعامل مع التهاني والمناسبات"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["ترقيت", "ترقية", "منصب", "وظيفة جديدة"]):
            return random.choice(self.knowledge_base["congratulations"]["ترقية"])
        
        if any(word in text_lower for word in ["نجحت", "تخرجت", "نجاح", "تخرج"]):
            return random.choice(self.knowledge_base["congratulations"]["نجاح"])
        
        if any(word in text_lower for word in ["تزوجت", "زواج", "عرس", "خطبت"]):
            return random.choice(self.knowledge_base["congratulations"]["زواج"])
        
        return "ألف ألف مبروك! الله يبارك لك ويزيدك من فضله وكرمه 🎊✨"
    
    def handle_greeting(self, text: str) -> str:
        """التعامل مع التحيات"""
        greetings = [
            "أهلاً وسهلاً بك! كيف حالك اليوم؟ 😊",
            "حياك الله! إيش اللي تحتاجه؟ 🌟",
            "مرحبا بك! نورت المكان ✨",
            "وعليكم السلام ورحمة الله وبركاته 🤲",
            "أهلين! كيف الصحة والعافية؟ 😊",
            "يا هلا والله! كيف الأحوال؟ 🤗"
        ]
        
        if "السلام عليكم" in text.lower():
            return "وعليكم السلام ورحمة الله وبركاته 🤲\nأهلاً وسهلاً بك، كيف حالك؟"
        
        return random.choice(greetings)
    
    def handle_farewell(self, text: str) -> str:
        """التعامل مع الوداع"""
        farewells = [
            "الله معك! تصبح على خير 🌙",
            "باي باي! إن شاء الله نشوفك قريباً 👋",
            "في أمان الله، اعتني بنفسك 🤗",
            "يعطيك العافية، الله يحفظك 🤲",
            "مع السلامة، ونورت المكان! ✨",
            "الله يوفقك، ودايماً في الخدمة! 😊"
        ]
        return random.choice(farewells)
    
    def handle_gratitude(self, text: str) -> str:
        """التعامل مع الشكر"""
        gratitude_responses = [
            "الله يعافيك! ما سويت شي يستاهل الشكر 😊",
            "من عيوني، أي وقت تحتاج مساعدة! 🤗",
            "وياك، هذا واجبي وأنا سعيد إني ساعدتك ☺️",
            "الله يكرمك، أنا في الخدمة دايماً 🌟",
            "ما عليك شكر، إحنا هنا عشانك! ❤️",
            "تسلم، الله يخليك! دايماً في الخدمة 🤝"
        ]
        return random.choice(gratitude_responses)
    
    def handle_sad_emotion(self, text: str) -> str:
        """التعامل مع المشاعر الحزينة"""
        supportive_responses = [
            "الله يعطيك القوة، إن شاء الله كل شي بيصير أحسن 🤗\nأنا هنا إذا تبي تحكي أو تحتاج أي شي",
            "لا تزعل، الحياة فيها صعود ونزول والمهم إنك تتجاوز الصعاب 💪\nدايماً فاكر إن بعد العسر يسر",
            "حاسس بضيقك، بس الله ما يكلف نفس إلا وسعها 🤲\nاستغفر كثير وادع ربك، هو مجيب الدعوات",
            "أعرف إنك تمر بوقت صعب، بس تأكد إن هذا مو نهاية العالم 🌅\nكل مشكلة ولها حل بإذن الله"
        ]
        return random.choice(supportive_responses)
    
    def handle_happy_emotion(self, text: str) -> str:
        """التعامل مع المشاعر السعيدة"""
        happy_responses = [
            "الله يديم عليك الفرحة والسعادة! 😊✨\nإيش المناسبة الحلوة؟",
            "حلو شوفك مبسوط! الله يزيد فرحتك 🌟\nشاركني إيش اللي فرحك",
            "ما شاء الله عليك! السعادة تطلع من عيونك 😄\nالله يحفظ لك فرحتك",
            "يا الله على الطاقة الإيجابية! 🎉\nفرحتك تفرح القلب، الله يديمها عليك"
        ]
        return random.choice(happy_responses)
    
    def handle_help_request(self, text: str) -> str:
        """التعامل مع طلبات المساعدة"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["ملل", "زهق", "ما أدري وش أسوي"]):
            return """فهمتك! الملل شي طبيعي يصير للكل 😅
            
إليك بعض الأفكار الحلوة:
📚 اقرا كتاب أو مقال مفيد
🎬 شاهد فيلم وثائقي أو فيديوهات تعليمية
👥 تواصل مع الأصدقاء والأهل
🏃‍♂️ امارس رياضة أو تمارين خفيفة
🎨 جرب هواية جديدة زي الرسم أو الكتابة
🍳 طبخ وصفة جديدة
🧹 رتب البيت أو الغرفة
📱 تعلم مهارة جديدة من النت

إيش رأيك؟ أي واحد يعجبك أكثر؟"""
        
        if "محتاج مساعدة" in text_lower or "ساعدني" in text_lower:
            return "طبعاً! أنا هنا عشان أساعدك 🤝\nقول لي إيش المشكلة أو إيش اللي تحتاجه بالضبط، وإن شاء الله نلقى له حل"
        
        return "أنا هنا عشانك! 😊\nقول لي إيش اللي تحتاجه وإن شاء الله أقدر أساعدك"
    
    def handle_general_question(self, text: str) -> str:
        """التعامل مع الأسئلة العامة"""
        return "سؤال حلو! 🤔\nممكن توضح أكثر عشان أقدر أعطيك جواب مفصل ومفيد؟"
    
    def handle_general_conversation(self, text: str) -> str:
        """التعامل مع المحادثة العامة"""
        general_responses = [
            "أحس إنك تبي تحكي عن شي، أنا مستمع لك 👂",
            "إيش رأيك نتكلم عن موضوع يهمك؟ 💬",
            "أنا هنا إذا تبي تسولف أو تسأل عن أي شي 😊",
            "حلو! إيش اللي في بالك تحكي عنه؟ 🤔",
            "أحب الدردشة معك! وش الأخبار؟ ☕",
            "يا هلا! إيش اللي جابك اليوم؟ 😄"
        ]
        return random.choice(general_responses)

def comprehensive_test():
    """اختبار شامل للنظام"""
    nano = NanoSmartResponse()
    
    test_cases = [
        "وش عاصمة السعودية؟",
        "أنا ترقيت في العمل!",
        "اذكر ربك",
        "كم الساعة؟",
        "مين انت؟",
        "صباح الخير",
        "شكراً لك يا نانو",
        "أنا تعبان ومكتئب",
        "أنا فرحان ومبسوط اليوم!",
        "ساعدني ما أدري وش أسوي",
        "باي باي",
        "السلام عليكم",
        "وش تقدر تسوي؟",
        "معلومات عن جدة",
        "ادع لي",
        "نجحت في الامتحان!",
        "أي يوم اليوم؟",
        "أنا زعلان من صديقي"
    ]
    
    print("🚀 اختبار النظام الذكي الشامل لنانو")
    print("=" * 60)
    
    for i, test_input in enumerate(test_cases, 1):
        response = nano.generate_smart_response(test_input)
        print(f"\n{i:2d}. 👤 المستخدم: {test_input}")
        print(f"    🤖 نانو: {response}")
        print("-" * 50)

if __name__ == "__main__":
    comprehensive_test()