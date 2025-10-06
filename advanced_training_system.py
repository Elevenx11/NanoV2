# advanced_training_system.py - نظام التدريب المتقدم لتطوير ذكاء نانو
import json
import random
import time
from datetime import datetime
from typing import List, Dict, Set
import re
import os

class AdvancedTrainingSystem:
    """نظام التدريب المتقدم لنانو"""
    
    def __init__(self, corpus_path="corpus.json"):
        self.corpus_path = corpus_path
        self.training_sessions = 0
        self.quality_filters = self.setup_quality_filters()
        self.conversation_patterns = self.setup_conversation_patterns()
        
    def setup_quality_filters(self) -> Dict:
        """إعداد مرشحات الجودة"""
        return {
            # كلمات يجب تجنبها (تحيز لمجالات معينة)
            "avoid_words": [
                # أسماء أشخاص مشهورين
                "ميسي", "كريستيانو", "محمد صلاح", "ابن سلمان",
                # أفلام وألعاب محددة
                "انمي", "ناروتو", "قاتل الشياطين", "فورتنايت", "ببجي",
                # أغاني ومشاهير محددين
                "عبدالمجيد عبدالله", "محمد عبده", "طلال مداح",
                # أحداث تاريخية محددة جداً
                "معركة الدرعية", "حرب الخليج", "كورونا",
                # ماركات وشركات محددة
                "سامسونج", "آيفون", "تسلا", "نتفليكس"
            ],
            
            # كلمات مرغوبة (عامة ومفيدة)
            "preferred_words": [
                # أنشطة يومية عامة
                "شرب", "أكل", "نوم", "قراءة", "كتابة", "مشي", "رياضة",
                # مشاعر وتفاعلات
                "فرح", "حزن", "تعب", "راحة", "ضحك", "بكا",
                # أماكن عامة
                "بيت", "شغل", "مدرسة", "مسجد", "سوق", "حديقة",
                # زمن وطقس
                "صباح", "مساء", "ليل", "صيف", "شتا", "حر", "برد"
            ],
            
            # أنماط الجمل المفيدة
            "useful_patterns": [
                r"كيف حال",
                r"وش رايك",
                r"شلونك مع",
                r"متى بت",
                r"وين رح",
                r"ليش ما",
                r"الله يعين"
            ]
        }
    
    def setup_conversation_patterns(self) -> Dict:
        """إعداد أنماط المحادثات الطبيعية"""
        return {
            # محادثات يومية عامة
            "daily_conversations": [
                # الصباح
                "صباح الخير كيف نومك",
                "الحمدلله نومة هنيئة وانت كيفك",
                "بخير الحمدلله شنو برنامجك اليوم",
                "عندي شغل كثير بس ان شاء الله نخلصه",
                
                # الطعام والشراب
                "وش تغديت اليوم",
                "اكلت شوي رز ولحم وانت",
                "انا ما تغديت للحين جوعان",
                "يلا تعال نروح نتغدى سوا",
                "اشرب موية كثير مفيد للصحة",
                "القهوة العربية أحسن من كل شي",
                
                # الطقس والجو
                "الجو اليوم كيف تشوفه",
                "حار مرة والله ما يطاق",
                "البرد احسن من الحر بكثير",
                "المطر امس كان حلو والله",
                "الغبار اليوم قوي خلنا في البيت",
                
                # العمل والدراسة
                "شلونك مع الشغل هالفترة",
                "متعب بس الحمدلله رزق",
                "الدراسة صعبة بس لازم نصبر",
                "اختبارات هالاسبوع وانا خايف",
                "خلصت مشروعي اخيرا الحمدلله",
                
                # الصحة والرياضة
                "روحت الطبيب امس فحص دوري",
                "المشي كل يوم مفيد للجسم",
                "باخذ فيتامينات عشان الصحة",
                "تعبان شوي بس عادي مو شي كبير",
                "النوم المبكر مهم للصحة",
                
                # التسوق والحاجات
                "بروح السوق اشتري حاجات البيت",
                "الاسعار غلت مرة هالايام",
                "اشتريت ملابس جديدة للعيد",
                "محتاج اشتري اغراض للبيت",
                "السوق مزدحم امس كان",
                
                # الأصدقاء والعائلة
                "شلون الوالدين عندك",
                "الحمدلله بخير يسلموا لك",
                "الاصدقاء ما شفناهم من فترة",
                "خلنا نطلع نتجمع هالويكند",
                "العائلة مهمة لازم نقضي وقت معهم"
            ],
            
            # تفاعلات اجتماعية
            "social_interactions": [
                # الترحيب والوداع
                "اهلا وسهلا نورت المكان",
                "الله يعطيك العافية تسلم",
                "في امان الله ونشوفك قريب",
                "سلام عليكم ورحمة الله",
                "وعليكم السلام ومرحبا فيك",
                
                # الدعم والمساعدة
                "اذا تحتاج مساعدة كلمني",
                "ما عليك منا نساعدك بكل شي",
                "الله يوفقك ويسهل امورك",
                "لا تتردد اطلب اي شي تحتاجه",
                "احنا هنا عشانك متى ما احتجت",
                
                # التعبير عن المشاعر
                "فرحان لك والله تستاهل الخير",
                "متضايق من الموضوع بس صار خلاص",
                "مبسوط اليوم لان شفت اصحابي",
                "متحمس للاجازة الجاية ان شاء الله",
                "قلقان من الامتحان بكرة"
            ],
            
            # أسئلة وإجابات منطقية
            "logical_qa": [
                # أسئلة عامة
                "وش رايك نروح نتمشى العصر",
                "فكرة حلوة الجو حلو اليوم",
                "متى موعدنا بكرة",
                "الساعة ثلاثة العصر اذا ينفعك",
                "وين نتقابل",
                "في المقهى اللي قريب من البيت",
                
                # حل مشاكل
                "جوالي تعلق ما يشتغل",
                "جرب تطفيه وتشغله مرة ثانية",
                "السيارة ما تبدي شنو المشكلة",
                "يمكن البطارية خلصت او البنزين",
                "ما اقدر انام من التفكير",
                "حاول تقرا شي او تسمع موسيقى هادية",
                
                # نصائح عملية
                "كيف احفظ الدروس بسرعة",
                "اقرا بصوت عالي وكرر اكثر من مرة",
                "وش افضل وقت للمذاكرة",
                "الصبح الباكر المخ يكون صافي",
                "كيف اوفر فلوس",
                "سوي ميزانية واكتب كل شي تصرفه"
            ]
        }
    
    def generate_natural_conversations(self, count: int = 200) -> List[str]:
        """توليد محادثات طبيعية متنوعة"""
        conversations = []
        
        # إضافة المحادثات الموجودة
        for category, phrases in self.conversation_patterns.items():
            conversations.extend(phrases)
        
        # توليد محادثات جديدة بناءً على الأنماط
        base_questions = [
            "كيف", "وش", "متى", "وين", "ليش", "شلون"
        ]
        
        base_topics = [
            "الشغل", "الدراسة", "البيت", "الاكل", "النوم", 
            "الطقس", "الصحة", "الاصدقاء", "العائلة"
        ]
        
        responses = [
            "الحمدلله", "بخير", "عادي", "زين", "حلو", 
            "صعب شوي", "ما بعرف", "يمكن", "ان شاء الله"
        ]
        
        # توليد تركيبات جديدة
        for i in range(50):
            question = f"{random.choice(base_questions)} حالك مع {random.choice(base_topics)}"
            answer = f"{random.choice(responses)} والله {random.choice(['متعب', 'مرتاح', 'مبسوط', 'متضايق'])}"
            conversations.extend([question, answer])
        
        return conversations[:count]
    
    def generate_daily_life_phrases(self, count: int = 150) -> List[str]:
        """توليد عبارات الحياة اليومية"""
        daily_phrases = []
        
        # أنشطة يومية
        activities = [
            "قريت كتاب حلو امس",
            "كتبت في دفتر ملاحظاتي",
            "مشيت نص ساعة في الحديقة",
            "شربت قهوة الصباح زي كل يوم",
            "اكلت فطار خفيف وصحي",
            "نمت بدري امس كان يوم متعب",
            "صحيت الفجر وقريت شوي",
            "رتبت البيت والغرفة",
            "غسلت الملابس وكويتها",
            "طبخت اكلة جديدة اليوم"
        ]
        
        # مشاعر وأحاسيس
        feelings = [
            "حاسس براحة اليوم والحمدلله",
            "متفائل للمستقبل ان شاء الله",
            "شوي متوتر بس هذا طبيعي",
            "مبسوط لاني خلصت شغلي",
            "متحمس للاجازة الجاية",
            "هادي اليوم مافي ضغوط",
            "متعب شوي من الشغل",
            "مرتاح لاني نمت زين"
        ]
        
        # تفاعلات اجتماعية بسيطة
        social = [
            "كلمت صديقي شفت كيف حاله",
            "زرت اهلي وقضيت وقت حلو",
            "تجمعنا مع الاصدقاء في المقهى",
            "ساعدت جاري في شي محتاجه",
            "شكرت الموظف لانه ساعدني",
            "سلمت على الجيران بالممر"
        ]
        
        # جمع كل الفئات
        daily_phrases.extend(activities)
        daily_phrases.extend(feelings)
        daily_phrases.extend(social)
        
        # إضافة تنويعات
        while len(daily_phrases) < count:
            # تنويع على الأنشطة
            activity_templates = [
                "اليوم {action} كان {feeling}",
                "امس {action} بس {feeling}",
                "بكرة بـ{action} ان شاء الله"
            ]
            
            actions = ["اقرا", "اكتب", "امشي", "اطبخ", "ارتب", "انظف"]
            feelings = ["حلو", "متعب", "مفيد", "مريح", "صعب"]
            
            template = random.choice(activity_templates)
            new_phrase = template.format(
                action=random.choice(actions),
                feeling=random.choice(feelings)
            )
            daily_phrases.append(new_phrase)
        
        return daily_phrases[:count]
    
    def filter_and_improve_text(self, text: str) -> tuple:
        """تصفية وتحسين النص"""
        # تنظيف النص
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)  # توحيد المسافات
        
        # فحص الجودة
        quality_score = 0
        
        # نقاط إيجابية للكلمات المرغوبة
        for word in self.quality_filters["preferred_words"]:
            if word in text:
                quality_score += 2
        
        # نقاط سلبية للكلمات المتجنبة
        for word in self.quality_filters["avoid_words"]:
            if word in text:
                quality_score -= 5
        
        # نقاط إيجابية للأنماط المفيدة
        for pattern in self.quality_filters["useful_patterns"]:
            if re.search(pattern, text):
                quality_score += 3
        
        # فحص الطول والتعقيد
        word_count = len(text.split())
        if 3 <= word_count <= 15:  # طول مناسب
            quality_score += 1
        
        # فحص الأحرف العربية
        arabic_ratio = len([c for c in text if '\u0600' <= c <= '\u06FF']) / len(text)
        if arabic_ratio > 0.7:
            quality_score += 2
        
        is_good_quality = quality_score > 0
        
        return text, is_good_quality, quality_score
    
    def progressive_training_session(self, session_number: int):
        """جلسة تدريب تدريجية"""
        print(f"\n🎯 جلسة التدريب رقم {session_number}")
        print("=" * 50)
        
        # تحميل البيانات الحالية
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                current_sentences = data.get("sentences", [])
        except FileNotFoundError:
            current_sentences = []
        
        initial_count = len(current_sentences)
        print(f"📊 الجمل الحالية: {initial_count}")
        
        # توليد محتوى جديد حسب مستوى الجلسة
        new_content = []
        
        if session_number <= 5:  # المراحل الأولى - محادثات أساسية
            print("🌱 المرحلة: محادثات أساسية")
            new_content.extend(self.generate_natural_conversations(100))
            new_content.extend(self.generate_daily_life_phrases(100))
        
        elif session_number <= 15:  # المراحل المتوسطة - تطوير التعقيد
            print("🌿 المرحلة: تطوير متوسط")
            new_content.extend(self.generate_natural_conversations(150))
            new_content.extend(self.generate_daily_life_phrases(150))
            new_content.extend(self.generate_complex_interactions(100))
        
        else:  # المراحل المتقدمة - ذكاء متقدم
            print("🌳 المرحلة: ذكاء متقدم")
            new_content.extend(self.generate_natural_conversations(200))
            new_content.extend(self.generate_daily_life_phrases(200))
            new_content.extend(self.generate_complex_interactions(150))
            new_content.extend(self.generate_philosophical_content(50))
        
        # تصفية وتحسين المحتوى
        high_quality_content = []
        total_processed = 0
        
        for text in new_content:
            cleaned_text, is_good, score = self.filter_and_improve_text(text)
            total_processed += 1
            
            if is_good and cleaned_text not in current_sentences:
                high_quality_content.append(cleaned_text)
        
        # إضافة المحتوى الجديد
        current_sentences.extend(high_quality_content)
        
        # حفظ البيانات المحدثة
        updated_data = {"sentences": current_sentences}
        with open(self.corpus_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        # إحصائيات الجلسة
        final_count = len(current_sentences)
        added_count = final_count - initial_count
        
        print(f"✅ تم معالجة: {total_processed} نص")
        print(f"✅ تم إضافة: {added_count} جملة عالية الجودة")
        print(f"📈 إجمالي الجمل الآن: {final_count}")
        print(f"⭐ معدل الجودة: {(added_count/total_processed)*100:.1f}%")
        
        return added_count
    
    def generate_complex_interactions(self, count: int = 100) -> List[str]:
        """توليد تفاعلات معقدة"""
        complex_phrases = [
            # مناقشات وآراء
            "وش رايك في الموضوع ذا",
            "صراحة انا مو متفق معك",
            "نقطة حلوة ما فكرت فيها",
            "يمكن انت محق في كلامك",
            "خلنا نشوف الموضوع من زاوية ثانية",
            
            # حل مشاكل معقدة
            "المشكلة معقدة شوي بس حلها موجود",
            "لازم نفكر في الحل من كل الجهات",
            "الوضع يحتاج صبر وحكمة",
            "كل مشكلة لها حل بإذن الله",
            
            # تخطيط ومستقبل
            "خططي للشهر الجاي واضحة",
            "لازم اخطط للمستقبل زين",
            "الاهداف مهمة في الحياة",
            "التخطيط نص النجاح"
        ]
        
        return complex_phrases[:count]
    
    def generate_philosophical_content(self, count: int = 50) -> List[str]:
        """توليد محتوى فلسفي بسيط"""
        philosophical = [
            "الصبر مفتاح الفرج",
            "كل شي له حكمة من ربنا",
            "الحياة مدرسة نتعلم منها",
            "التفاؤل يخلي الحياة اجمل",
            "الشكر يزيد النعمة",
            "التواضع من اجمل الصفات",
            "الصداقة كنز لا يقدر بثمن",
            "العلم نور يضيء الطريق"
        ]
        
        return philosophical[:count]
    
    def run_intelligence_development_program(self, target_sessions: int = 20):
        """برنامج تطوير الذكاء المتدرج"""
        print("🚀 بدء برنامج تطوير ذكاء نانو المتقدم")
        print("🎯 الهدف: الوصول لمستوى الذكاء الاصطناعي السعودي")
        print(f"📅 عدد الجلسات المخططة: {target_sessions}")
        print("="*70)
        
        total_added = 0
        
        for session in range(1, target_sessions + 1):
            try:
                added_this_session = self.progressive_training_session(session)
                total_added += added_this_session
                
                # فترة راحة بين الجلسات
                if session < target_sessions:
                    print(f"⏳ راحة قصيرة قبل الجلسة التالية...")
                    time.sleep(2)
                
            except Exception as e:
                print(f"❌ خطأ في الجلسة {session}: {str(e)}")
                continue
        
        print("\n" + "="*70)
        print(f"🎉 انتهى برنامج التطوير!")
        print(f"📊 إجمالي الجمل المضافة: {total_added}")
        print(f"🧠 مستوى الذكاء المتوقع: متقدم")
        print(f"🇸🇦 جاهز للمنافسة مع الذكاء الاصطناعي السعودي!")

# دالة للاختبار والتشغيل
def main():
    """الدالة الرئيسية"""
    trainer = AdvancedTrainingSystem()
    
    print("مرحباً بك في نظام تطوير ذكاء نانو المتقدم!")
    print("=" * 50)
    
    choice = input("اختر الوضع:\n1. جلسة تدريب واحدة\n2. برنامج تطوير كامل (20 جلسة)\n3. جلسات مخصصة\nاختيارك: ")
    
    if choice == "1":
        trainer.progressive_training_session(1)
        
    elif choice == "2":
        trainer.run_intelligence_development_program(20)
        
    elif choice == "3":
        sessions = int(input("كم جلسة تريد؟ "))
        trainer.run_intelligence_development_program(sessions)
        
    else:
        print("اختيار غير صحيح")

if __name__ == "__main__":
    main()