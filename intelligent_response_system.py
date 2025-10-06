# intelligent_response_system.py - نظام الردود الذكي والمتطور لنانو
import json
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import random

class IntelligentResponseSystem:
    """نظام الردود الذكي والمتطور لنانو"""
    
    def __init__(self):
        self.knowledge_base = self.initialize_knowledge_base()
        self.response_patterns = self.initialize_response_patterns()
        self.conversation_context = []
        
    def initialize_knowledge_base(self) -> Dict:
        """قاعدة المعرفة الأساسية لنانو"""
        return {
            "geography": {
                "عاصمة السعودية": "الرياض هي عاصمة المملكة العربية السعودية الحبيبة",
                "مدن سعودية": ["الرياض", "جدة", "مكة المكرمة", "المدينة المنورة", "الدمام", "الطائف", "أبها", "تبوك", "القصيم", "حائل"],
                "محافظات": ["الأحساء", "جازان", "نجران", "الباحة", "عسير", "الحدود الشمالية"]
            },
            
            "religion": {
                "أذكار": [
                    "سبحان الله وبحمده، سبحان الله العظيم",
                    "لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير",
                    "اللهم صل وسلم على نبينا محمد",
                    "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه",
                    "الحمد لله رب العالمين"
                ],
                "دعاء": [
                    "اللهم اهدني فيمن هديت، وعافني فيمن عافيت",
                    "ربنا آتنا في الدنيا حسنة وفي الآخرة حسنة وقنا عذاب النار",
                    "اللهم أعني على ذكرك وشكرك وحسن عبادتك"
                ]
            },
            
            "general_info": {
                "الوقت الحالي": datetime.now().strftime("%H:%M"),
                "التاريخ": datetime.now().strftime("%Y-%m-%d"),
                "معلومات_نانو": "أنا نانو، مساعد ذكي باللهجة السعودية، هنا عشان أساعدك في أي شي تحتاجه"
            },
            
            "congratulations": {
                "ترقية": [
                    "ألف مبروك الترقية! الله يبارك لك ويزيدك من فضله",
                    "تستاهل كل خير، مبروك الترقية وإن شاء الله دايماً للأمام",
                    "الله يكرمك! مبروك الترقية وعقبال المناصب الأعلى"
                ],
                "نجاح": [
                    "ألف مبروك النجاح! تعبك ما راح سدى",
                    "الله يبارك لك، مبروك النجاح وعقبال درجات أعلى",
                    "تستاهل كل خير، مبروك النجاح"
                ],
                "زواج": [
                    "ألف مبروك! الله يبارك لكم ويجمع بينكم في خير",
                    "مبروك الزواج، الله يتمم عليكم بالخير والبركة",
                    "بالرفاه والبنين، مبروك الزواج"
                ]
            }
        }
    
    def initialize_response_patterns(self) -> Dict:
        """أنماط الردود المختلفة"""
        return {
            "question_patterns": [
                r"وش|إيش|شنو|كيف|متى|وين|مين|ليه|لماذا",
                r"\?|\؟",
                r"^(هل|أهو|صح|خطأ)",
            ],
            
            "congratulation_patterns": [
                r"ترقيت|اترقيت|حصلت على ترقية|رقوني",
                r"نجحت|تخرجت|نجاحي|تخرجي",
                r"تزوجت|خطبت|عرسي|زواجي|خطوبتي",
                r"حصلت على|فزت بـ|ربحت",
                r"مولود جديد|طفل جديد|بيبي|مولود"
            ],
            
            "religious_patterns": [
                r"اذكر ربك|قول ذكر|أذكار|استغفار|تسبيح",
                r"ادع لي|ادعي لي|دعاء|اللهم",
                r"آية|قرآن|حديث|سورة"
            ],
            
            "location_patterns": [
                r"عاصمة السعودية|عاصمة المملكة|عاصمة البلد",
                r"مدن سعودية|مدن المملكة|محافظات",
                r"وين الرياض|وين جدة|وين مكة"
            ],
            
            "time_patterns": [
                r"كم الساعة|وش الوقت|الوقت الحين|الساعة كم|وقت الحين",
                r"أي يوم|اليوم شنو|التاريخ|اليوم كم|تاريخ كم"
            ],
            
            "personal_patterns": [
                r"مين انت|شنو اسمك|من انت|تعريف نفسك",
                r"وش تقدر تسوي|قدراتك إيش|وش مهاراتك"
            ]
        }
    
    def detect_intent(self, text: str) -> Tuple[str, float]:
        """تحديد نية المستخدم من النص"""
        text_lower = text.lower()
        
        # البحث عن الأنماط
        for intent, patterns in self.response_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower):
                    return intent.replace("_patterns", ""), 0.9
        
        # تحديد أنماط خاصة
        if any(word in text_lower for word in ["مبروك", "ألف مبروك", "تهنئة"]):
            return "congratulation_response", 0.8
            
        if any(word in text_lower for word in ["شكرا", "يعطيك العافية", "جزاك الله"]):
            return "gratitude", 0.8
            
        if any(word in text_lower for word in ["صباح الخير", "مساء الخير", "أهلا", "مرحبا"]):
            return "greeting", 0.8
            
        if any(word in text_lower for word in ["باي", "وداع", "الله معك", "تصبح على خير"]):
            return "farewell", 0.8
            
        # افتراضي: محادثة عامة
        return "general_conversation", 0.5
    
    def extract_keywords(self, text: str) -> List[str]:
        """استخراج الكلمات المفتاحية من النص"""
        keywords = []
        text_lower = text.lower()
        
        # استخراج كلمات مهمة
        important_words = re.findall(r'\b(?:عاصمة|مدينة|ترقية|نجاح|زواج|دعاء|ذكر|وقت|ساعة|يوم)\b', text_lower)
        keywords.extend(important_words)
        
        return keywords
    
    def generate_response(self, text: str) -> str:
        """توليد الرد المناسب"""
        intent, confidence = self.detect_intent(text)
        keywords = self.extract_keywords(text)
        
        # إضافة السياق للمحادثة
        self.conversation_context.append({
            "user_input": text,
            "intent": intent,
            "keywords": keywords,
            "timestamp": datetime.now()
        })
        
        # توليد الرد بناء على النية
        if intent == "question":
            return self.handle_question(text, keywords)
        elif intent == "congratulation":
            return self.handle_congratulation(text, keywords)
        elif intent == "religious":
            return self.handle_religious_request(text, keywords)
        elif intent == "location":
            return self.handle_location_question(text, keywords)
        elif intent == "time":
            return self.handle_time_question(text, keywords)
        elif intent == "personal":
            return self.handle_personal_question(text, keywords)
        elif intent == "greeting":
            return self.handle_greeting(text)
        elif intent == "farewell":
            return self.handle_farewell(text)
        elif intent == "gratitude":
            return self.handle_gratitude(text)
        else:
            return self.handle_general_conversation(text)
    
    def handle_question(self, text: str, keywords: List[str]) -> str:
        """التعامل مع الأسئلة"""
        text_lower = text.lower()
        
        if "عاصمة" in text_lower and "سعود" in text_lower:
            return "عاصمة المملكة العربية السعودية هي الرياض الحبيبة 🏛️"
            
        if any(city in text_lower for city in ["رياض", "جدة", "مكة", "مدينة"]):
            return "هذي من أهم وأجمل مدن المملكة العربية السعودية 🇸🇦"
            
        if "كيف الحال" in text_lower or "كيفك" in text_lower:
            return "الحمدلله بخير وعافية، كيف حالك انت؟ إيش اللي تحتاجه؟ 😊"
            
        # تحقق من أسئلة الوقت أولاً
        if any(word in text_lower for word in ["كم الساعة", "وش الوقت", "الوقت الحين", "الساعة كم"]):
            return self.handle_time_question(text, keywords)
        
        # تحقق من الأسئلة الشخصية
        if any(word in text_lower for word in ["مين انت", "من انت", "شنو اسمك", "تعريف نفسك"]):
            return self.handle_personal_question(text, keywords)
            
        if "إيش" in text_lower or "وش" in text_lower:
            return "حبيبي، ممكن توضح السؤال أكثر عشان أقدر أساعدك بشكل أفضل؟ 🤔"
            
        return "سؤال مثير للاهتمام! ممكن تعطيني تفاصيل أكثر عشان أقدر أجاوب بدقة؟ 💭"
    
    def handle_congratulation(self, text: str, keywords: List[str]) -> str:
        """التعامل مع التهاني"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["ترقيت", "ترقية", "منصب"]):
            return random.choice(self.knowledge_base["congratulations"]["ترقية"]) + " 🎉"
            
        if any(word in text_lower for word in ["نجحت", "تخرجت", "نجاح"]):
            return random.choice(self.knowledge_base["congratulations"]["نجاح"]) + " 📚✨"
            
        if any(word in text_lower for word in ["تزوجت", "زواج", "عرس"]):
            return random.choice(self.knowledge_base["congratulations"]["زواج"]) + " 💍❤️"
            
        return "ألف ألف مبروك! الله يبارك لك ويزيدك من فضله وكرمه 🎊✨"
    
    def handle_religious_request(self, text: str, keywords: List[str]) -> str:
        """التعامل مع الطلبات الدينية"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["اذكر", "ذكر", "تسبيح"]):
            dhikr = random.choice(self.knowledge_base["religion"]["أذكار"])
            return f"إليك هذا الذكر المبارك:\n\n🤲 {dhikr}\n\nجعله الله في ميزان حسناتك"
            
        if any(word in text_lower for word in ["ادع", "دعاء", "اللهم"]):
            dua = random.choice(self.knowledge_base["religion"]["دعاء"])
            return f"اللهم آمين:\n\n🤲 {dua}\n\nاللهم استجب دعاءنا وتقبل منا"
            
        if "استغفار" in text_lower:
            return "أستغفر الله العظيم الذي لا إله إلا هو الحي القيوم وأتوب إليه\n\nاللهم اغفر لنا ذنوبنا وتقبل توبتنا 🤲"
            
        return "بارك الله فيك على هذا السؤال الطيب 🤲\nاللهم اهدنا واهد بنا واجعلنا سبباً لمن اهتدى"
    
    def handle_location_question(self, text: str, keywords: List[str]) -> str:
        """التعامل مع أسئلة الأماكن"""
        text_lower = text.lower()
        
        if "عاصمة" in text_lower:
            return self.knowledge_base["geography"]["عاصمة السعودية"] + " 🏛️🇸🇦"
            
        if "مدن" in text_lower:
            cities = ", ".join(self.knowledge_base["geography"]["مدن سعودية"][:5])
            return f"من أهم مدن المملكة: {cities} وغيرها الكثير من المدن الجميلة 🏙️"
            
        return "المملكة العربية السعودية بلد واسع وجميل، فيه مدن ومحافظات كثيرة كل وحدة لها طابعها الخاص 🗺️"
    
    def handle_time_question(self, text: str, keywords: List[str]) -> str:
        """التعامل مع أسئلة الوقت"""
        current_time = datetime.now()
        
        if any(word in text.lower() for word in ["ساعة", "وقت"]):
            time_str = current_time.strftime("%H:%M")
            return f"الوقت الحين الساعة {time_str} 🕐"
            
        if "يوم" in text.lower() or "تاريخ" in text.lower():
            date_str = current_time.strftime("%Y-%m-%d")
            day_name = ["الاثنين", "الثلاثاء", "الأربعاء", "الخميس", "الجمعة", "السبت", "الأحد"][current_time.weekday()]
            return f"اليوم {day_name} الموافق {date_str} 📅"
            
        return f"الوقت الحالي: {current_time.strftime('%H:%M')} والتاريخ: {current_time.strftime('%Y-%m-%d')} ⏰"
    
    def handle_personal_question(self, text: str, keywords: List[str]) -> str:
        """التعامل مع الأسئلة الشخصية"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["مين", "اسم", "من انت"]):
            return "أنا نانو، مساعدك الذكي باللهجة السعودية الأصيلة! 🤖\nهنا عشان أساعدك في أي شي تحتاجه، من معلومات لأسئلة لحتى محادثة حلوة ☕"
            
        if any(word in text_lower for word in ["تقدر", "مهارات", "قدرات"]):
            return """أقدر أساعدك في أشياء كثيرة:
📚 الإجابة على الأسئلة العامة
🗺️ معلومات عن المملكة والمدن
🤲 الأذكار والأدعية
🎉 تهنئة بالمناسبات السعيدة
💬 محادثة ودردشة حلوة
⏰ معرفة الوقت والتاريخ

وأشياء كثيرة ثانية! جرب أسألني أي شي 😊"""
            
        return "أنا هنا عشانك! أسألني أي شي تبي تعرفه أو تحتاج مساعدة فيه 😊"
    
    def handle_greeting(self, text: str) -> str:
        """التعامل مع التحيات"""
        greetings = [
            "أهلاً وسهلاً بك! كيف حالك؟ 😊",
            "حياك الله! إيش اللي تحتاجه؟ 🌟",
            "مرحبا بك! نورت المكان ✨",
            "السلام عليكم ورحمة الله وبركاته 🤲",
            "أهلين! كيف الصحة والعافية؟ 😊"
        ]
        return random.choice(greetings)
    
    def handle_farewell(self, text: str) -> str:
        """التعامل مع الوداع"""
        farewells = [
            "الله معك! تصبح على خير 🌙",
            "باي باي! إن شاء الله نشوفك قريباً 👋",
            "في أمان الله، اعتني بنفسك 🤗",
            "يعطيك العافية، الله يحفظك 🤲",
            "مع السلامة، ونورت المكان! ✨"
        ]
        return random.choice(farewells)
    
    def handle_gratitude(self, text: str) -> str:
        """التعامل مع الشكر"""
        gratitude_responses = [
            "الله يعافيك! ما سويت شي 😊",
            "من عيوني، أي وقت تحتاج مساعدة! 🤗",
            "وياك، هذا واجبي ☺️",
            "الله يكرمك، أنا في الخدمة دايماً 🌟",
            "ما عليك شكر، إحنا هنا عشانك! ❤️"
        ]
        return random.choice(gratitude_responses)
    
    def handle_general_conversation(self, text: str) -> str:
        """التعامل مع المحادثة العامة"""
        text_lower = text.lower()
        
        # ردود ذكية حسب السياق
        if any(word in text_lower for word in ["تعبان", "زعلان", "حزين"]):
            return "الله يعطيك القوة، إن شاء الله كل شي بيصير أحسن 🤗\nأنا هنا إذا تبي تحكي أو تحتاج أي شي"
            
        if any(word in text_lower for word in ["فرحان", "مبسوط", "سعيد"]):
            return "الله يديم عليك الفرحة والسعادة! 😊✨\nإيش المناسبة الحلوة؟"
            
        if any(word in text_lower for word in ["مساعدة", "ساعدني", "محتاج"]):
            return "طبعاً! أنا هنا عشان أساعدك 🤝\nقول لي إيش اللي تحتاجه بالضبط"
            
        if any(word in text_lower for word in ["ملل", "زهق", "ما أدري وش أسوي", "ما عندي شي أسويه"]):
            return "فهمتك! الملل شي طبيعي 😅\nممكن تجرب تقرا كتاب، تشوف فيلم، تتواصل مع الأصدقاء، أو حتى تتعلم شي جديد!"
            
        # ردود عامة ذكية
        general_responses = [
            "أحس إنك تبي تحكي عن شي، أنا مستمع لك 👂",
            "إيش رأيك نتكلم عن موضوع يهمك؟ 💬",
            "أنا هنا إذا تبي تسولف أو تسأل عن أي شي 😊",
            "حلو! إيش اللي في بالك تحكي عنه؟ 🤔",
            "أحب الدردشة معك! وش الأخبار؟ ☕"
        ]
        
        return random.choice(general_responses)

def test_intelligent_system():
    """اختبار النظام الذكي"""
    system = IntelligentResponseSystem()
    
    test_cases = [
        "وش عاصمة السعودية؟",
        "أنا ترقيت في العمل!",
        "اذكر ربك",
        "كم الساعة؟",
        "مين انت؟",
        "صباح الخير",
        "شكراً لك",
        "أنا تعبان اليوم",
        "باي باي",
        "ما أدري وش أسوي"
    ]
    
    print("🧠 اختبار نظام الردود الذكي لنانو")
    print("=" * 50)
    
    for i, test_input in enumerate(test_cases, 1):
        response = system.generate_response(test_input)
        print(f"\n{i}. المستخدم: {test_input}")
        print(f"   نانو: {response}")
        print("-" * 30)

if __name__ == "__main__":
    test_intelligent_system()