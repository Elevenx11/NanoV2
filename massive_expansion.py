# massive_expansion.py - نظام التوسيع الضخم لنانو
import json
import random
import itertools
from typing import List, Dict, Set
from continuous_learning import ContinuousLearningSystem

class MassiveCorpusExpansion(ContinuousLearningSystem):
    """نظام التوسيع الضخم للوصول إلى 15000+ جملة"""
    
    def __init__(self, target_sentences: int = 15000, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.target_sentences = target_sentences
        self.expansion_categories = self.initialize_expansion_categories()
        
    def initialize_expansion_categories(self) -> Dict[str, int]:
        """تحديد أهداف التوسيع لكل فئة"""
        return {
            "daily_life": 2000,           # الحياة اليومية
            "emotions_advanced": 1500,    # المشاعر المتقدمة
            "social_interactions": 2000,  # التفاعلات الاجتماعية
            "cultural_expressions": 1500, # التعبيرات الثقافية
            "work_education": 1200,       # العمل والتعليم
            "family_relationships": 1500, # العلاقات العائلية
            "food_cooking": 800,          # الطعام والطبخ
            "travel_places": 700,         # السفر والأماكن
            "health_fitness": 800,        # الصحة واللياقة
            "technology_modern": 700,     # التقنية والعصر الحديث
            "weather_nature": 500,        # الطقس والطبيعة
            "shopping_commerce": 600,     # التسوق والتجارة
            "entertainment_hobbies": 800, # الترفيه والهوايات
            "philosophy_wisdom": 600,     # الفلسفة والحكمة
            "religious_spiritual": 1000, # الديني والروحاني
        }
    
    def generate_dynamic_variations(self, base_sentences: List[str], target_count: int) -> List[str]:
        """توليد تنويعات ديناميكية من الجمل الأساسية"""
        variations = []
        
        # قوائم الكلمات للاستبدال
        time_words = ["اليوم", "امبارح", "بكرة", "الصبح", "المسا", "الليل", "الفجر", "العصر"]
        emotion_words = ["مبسوط", "فرحان", "سعيد", "مرتاح", "هادي", "مطمئن", "راضي", "منشرح"]
        family_words = ["أمي", "أبوي", "أختي", "أخوي", "جدي", "جدتي", "العائلة", "الأهل"]
        activity_words = ["قريت", "كتبت", "شاهدت", "استمعت", "تعلمت", "مارست", "زرت", "اتصلت"]
        
        # توليد تنويعات
        for base in base_sentences:
            for i in range(target_count // len(base_sentences) + 1):
                varied = base
                
                # استبدال عشوائي للكلمات
                if "اليوم" in varied:
                    varied = varied.replace("اليوم", random.choice(time_words))
                if "فرحان" in varied or "مبسوط" in varied:
                    varied = varied.replace("فرحان", random.choice(emotion_words))
                    varied = varied.replace("مبسوط", random.choice(emotion_words))
                
                # إضافة تنويعات في البداية والنهاية
                prefixes = ["", "الحمدلله ", "والله ", "أحمد الله ", "بصراحة ", "صدقني "]
                suffixes = ["", " والحمدلله", " إن شاء الله", " بإذن الله", " ربي يكرمك", " الله يعطيك العافية"]
                
                varied = random.choice(prefixes) + varied + random.choice(suffixes)
                variations.append(varied)
                
                if len(variations) >= target_count:
                    break
            
            if len(variations) >= target_count:
                break
        
        return list(set(variations))[:target_count]
    
    def generate_daily_life_expansion(self) -> List[str]:
        """توليد جمل الحياة اليومية المتنوعة"""
        base_sentences = [
            "قمت من النوم على صوت الأذان",
            "شربت قهوتي العربية وأنا أشوف الطيور",
            "الفجر اليوم كان جميل والجو منعش",
            "دعيت دعوة الصباح وتوكلت على الله",
            "بديت يومي بالبسملة",
            "صليت الفجر في المسجد",
            "المغرب اليوم كان هادي",
            "سهرت مع الأهل وقضينا وقت حلو",
            "نمت مبكر عشان أقوم نشيط",
            "استغفرت قبل النوم",
            "اشتغلت في البيت ونظفت",
            "طبخت وجبة لذيذة",
            "غسلت الملابس وكويتها",
            "سقيت النباتات",
            "رتبت المكتبة وقريت كتاب",
            "شاهدت برنامج مفيد",
            "لعبت مع الأطفال",
            "استمعت للقرآن",
            "اتصلت بصديق قديم",
            "تمشيت في الحي",
            "حسيت بالامتنان",
            "فرحت لأن يومي كان حلو",
            "تعبت شوي بس مرتاح",
            "حسيت بالرضا",
            "استمتعت بالوقت",
            "شعرت بالطمأنينة",
            "حمدت الله على الصحة",
            "سعدت لأن تعلمت شي جديد",
            "أعجبني كلام حلو سمعته",
            "تأثرت من قصة مؤثرة"
        ]
        
        return self.generate_dynamic_variations(base_sentences, 450)
    
    def generate_emotions_advanced_expansion(self) -> List[str]:
        """توليد المشاعر المتقدمة والمعقدة"""
        base_emotions = [
            "فرحان وحزين في نفس الوقت",
            "خايف ومتحمس للتحدي الجديد", 
            "مشتاق لأهلي وراضي عن قراري",
            "متضايق من الموقف بس فاهم الحكمة",
            "محتار بين خيارين",
            "مبسوط من الداخل رغم التعب",
            "حاسس بالوحدة رغم إني مع ناس",
            "هادي من برا بس جواي عاصفة",
            "متفائل بالمستقبل رغم الصعوبة",
            "محب للحياة رغم المشاكل",
            "شعرت بحنين خفيف للطفولة",
            "حسيت بفخر صامت",
            "تأثرت من كرم شخص غريب",
            "استاء من طريقة الكلام",
            "أعجبت بالهدوء في العيون",
            "انتابني شعور غريب بالحنين",
            "شعرت بالخجل من الثناء",
            "تملكني إحساس بالمسؤولية",
            "شعرت بالضعف أمام عظمة الخلق",
            "أحسست بالطمأنينة في المصاعب",
            "بكيت من الفرح",
            "ضحكت من قلبي أول مرة من زمان",
            "صرخت من الخوف",
            "سكت كثير وأنا أفكر",
            "عضيت على شفتي من الغضب",
            "غمضت عيني وتنهدت",
            "ابتسمت ابتسامة حزينة",
            "هزيت راسي بالموافقة",
            "حبست دمعتي عشان ما أبكي",
            "فتحت عيني بدهشة"
        ]
        return self.generate_dynamic_variations(base_emotions, 330)
    
    def generate_social_interactions_expansion(self) -> List[str]:
        """توليد التفاعلات الاجتماعية المتقدمة"""
        base_social = [
            "جلست مع صديقي نتكلم عن أحلامنا",
            "ناقشت مع أبوي موضوع مهم",
            "تبادلت الآراء مع زملائي",
            "استمعت لقصة جدي عن الماضي",
            "شاركت تجربتي مع شخص",
            "طلبت نصيحة من أمي",
            "أعطيت رأيي بصراحة",
            "تعلمت شي جديد من محادثة",
            "شرحت وجهة نظري",
            "استفدت من تجارب الآخرين",
            "رحبت بالضيوف بحفاوة",
            "شكرت الشخص اللي ساعدني",
            "اعتذرت عن خطئي بصدق",
            "باركت لصديقي إنجازه",
            "عزيت جاري في فقدانه",
            "هنأت زميلي بترقيته",
            "قدمت واجب العزاء",
            "زرت مريض وطمأنت على صحته",
            "دعيت صديق لحضور مناسبة",
            "شاركت في فرحة قريب",
            "تدخلت بحكمة في مشكلة",
            "صالحت بين أخوين",
            "حليت خلاف في العمل",
            "وقفت موقف عادل",
            "اقترحت حل وسط",
            "تنازلت عن حقي لأجل السلام",
            "اعترفت بخطئي وطلبت السماح",
            "سامحت شخص أذاني",
            "تجاهلت كلام جارح",
            "دعوت للهدوء والتفاهم"
        ]
        return self.generate_dynamic_variations(base_social, 500)
    
    def generate_cultural_expressions_expansion(self) -> List[str]:
        """توليد التعبيرات الثقافية السعودية الأصيلة"""
        base_cultural = [
            "بيتنا بيتك وكل اللي عندنا لك",
            "اهلاً وسهلاً بك يا أهل وفين",
            "على الرحب والسعة يا غالي",
            "حياك الله وزادك رفعة",
            "الله يعطيك العافية والقوة",
            "بارك الله فيك وفي أهلك",
            "الله يجعله في ميزان حسناتك",
            "بعد إذنك إن شاء الله",
            "يا هلا باللي نور المكان",
            "كثر خيرك وقل شرك",
            "زادك الله من فضله وكرمه",
            "على بركة الرحمن يا رب",
            "ما قصرت يا خوي جزاك الله خير",
            "والله يعطيك على قد نيتك",
            "يعطيك العافية في قلبك ودينك",
            "الحمدلله اللي جمعنا على خير",
            "ما شاء الله تبارك الرحمن",
            "سبحان الله وبحمده رب العالمين",
            "الله م حد عليه وأجيح الخالق",
            "قدرنا عندك وإن قل زادنا شرف",
            "عينك علينا باردة يا غالي",
            "عساك على القوة يا هل الطيب",
            "الله يوفقك لكل خير",
            "من جد وجد ومن زرع حصد",
            "الصبر مفتاح الفرج بإذن الله",
            "الحمدلله رب العالمين على كل النعم",
            "لا إله إلا الله محمد رسول الله",
            "اللهم اعز الإسلام والمسلمين",
            "تقبل الله منا ومنكم صالح الأعمال"
            "ما نخليك تروح إلا بعد العشا",
            "الضيف عزيز وله كل التقدير والاحترام",
            "أهلاً وسهلاً مية مرحبا فيك",
            "نورت البيت بوجودك الكريم",
            "تفضل اجعل نفسك في بيتك",
            "عساك على القوة وما قصرت",
            "الله يكرمك زي ما كرمتنا بالزيارة",
        ]
        
        # التعبيرات الدينية والدعوات
        religious_expressions = [
            "اللهم بارك وزد من خيرك وفضلك",
            "ربي يحفظك من عينه ومن كل شر",
            "الله يوفقك ويسهل دربك في الدنيا والآخرة",
            "بإذن الله كل شي بيتيسر على خير",
            "ما كتبه الله لك بيجيك مهما طال الوقت",
            "التوكل على الله والله ما يضيع عبده",
            "الصبر مفتاح الفرج والعجلة من الشيطان",
            "الحمد لله رب العالمين على كل حال",
            "استغفر الله العظيم الذي لا إله إلا هو",
            "اللهم اجعل عملنا خالص لوجهك الكريم",
        ]
        
        # الأمثال والحكم الشعبية
        proverbs_wisdom = [
            "اللي ما يعرف الصقر يشويه مع الفراخ",
            "الطير على شكله يقع والناس على أشكالهم",
            "اللي بيته من زجاج ما يحصب الناس",
            "العتاب على قد المحبة والزعل على قد القرب",
            "الصديق وقت الضيق والأخ عند الكرب",
            "اللي يطلب العالي يصبر على المحن",
            "الكلام الحلو مفتاح القلوب المقفلة",
            "اللي ما له أول ما له تالي",
            "الزين زين حتى لو كان فقير",
            "العقل زينة والأدب تاج على الرأس",
        ]
        
        sentences.extend(hospitality_expressions * 15)
        sentences.extend(religious_expressions * 12)
        sentences.extend(proverbs_wisdom * 10)
        
        return sentences[:1500]
    
    def generate_work_education_expansion(self) -> List[str]:
        """توليد جمل العمل والتعليم"""
        sentences = []
        
        # بيئة العمل
        work_environment = [
            "بديت يوم العمل بنشاط وحماس للإنجاز",
            "تعاونت مع فريقي في مشروع مهم وحساس",
            "اجتهدت في عملي وحرصت على الجودة",
            "ساعدت زميل جديد يتعلم أصول الشغل",
            "حضرت اجتماع مهم ناقشنا فيه خطط المستقبل",
            "أنجزت المهام المطلوبة في الوقت المحدد",
            "تطوعت لمساعدة القسم في مشكلة طارئة",
            "اقترحت فكرة جديدة لتحسين سير العمل",
            "تدربت على برنامج جديد يساعد في الشغل",
            "شاركت في ورشة عمل مفيدة وثرية",
        ]
        
        # التعليم والدراسة
        education_learning = [
            "ذاكرت دروسي بتركيز واهتمام كبير",
            "شاركت في الحصة بأسئلة مفيدة وذكية",
            "ساعدت زميل في فهم درس صعب عليه",
            "قريت كتاب مفيد زاد من معرفتي",
            "بحثت في النت عن معلومات لبحثي",
            "حضرت محاضرة ثرية واستفدت منها كثير",
            "ناقشت مع الأستاذ نقطة مهمة في المنهج",
            "راجعت ملاحظاتي وأنا أتحضر للامتحان",
            "تعلمت مهارة جديدة بتساعدني مستقبلاً",
            "شرحت لأخوي الصغير واجبه المدرسي",
        ]
        
        # النجاح والإنجاز
        success_achievement = [
            "نجحت في المشروع اللي تعبت عليه شهور",
            "حصلت على تقدير ممتاز في الامتحان النهائي",
            "رقيت في العمل بفضل اجتهادي وإخلاصي",
            "فزت في المسابقة الثقافية على مستوى المدرسة",
            "حققت هدفي اللي كان يبدو صعب",
            "تخرجت من الجامعة بدرجة امتياز والحمدلله",
            "حصلت على وظيفة أحلامي بعد جهد طويل",
            "أكملت الدورة التدريبية بنجاح وتفوق",
            "قدمت عرض ممتاز أعجب كل الحاضرين",
            "وصلت لمنصب مسؤولية يحتاج ثقة كبيرة",
        ]
        
        sentences.extend(work_environment * 12)
        sentences.extend(education_learning * 10)
        sentences.extend(success_achievement * 8)
        
        return sentences[:1200]
    
    def run_massive_expansion(self) -> Dict[str, int]:
        """تشغيل التوسيع الضخم للنظام"""
        self._print("🚀 بدء التوسيع الضخم لنانو إلى 15000+ جملة")
        self._print("=" * 60)
        
        # تحميل الحالة الحالية
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                current_sentences = set(data.get("sentences", []))
        except:
            current_sentences = set()
        
        initial_count = len(current_sentences)
        self._print(f"📊 الجمل الحالية: {initial_count}")
        
        # توليد جمل جديدة بكميات ضخمة
        all_new_sentences = []
        
        categories_methods = {
            "daily_life": self.generate_daily_life_expansion,
            "emotions_advanced": self.generate_emotions_advanced_expansion,
            "social_interactions": self.generate_social_interactions_expansion,
            "cultural_expressions": self.generate_cultural_expressions_expansion,
            "work_education": self.generate_work_education_expansion,
        }
        
        for category, method in categories_methods.items():
            self._print(f"📝 توليد جمل {category}...")
            category_sentences = method()
            all_new_sentences.extend(category_sentences)
            self._print(f"   ✅ تم توليد {len(category_sentences)} جملة")
        
        # إضافة المزيد من الفئات
        additional_categories = self.generate_additional_categories()
        all_new_sentences.extend(additional_categories)
        
        # تصفية وإضافة الجمل الجديدة
        self._print("🔍 تصفية ومعالجة الجمل الجديدة...")
        processed = self.process_and_filter_sentences(all_new_sentences)
        
        # إضافة الجمل الفريدة فقط
        added_count = 0
        for sentence in processed:
            if sentence not in current_sentences:
                current_sentences.add(sentence)
                added_count += 1
        
        # حفظ النتائج
        final_sentences = list(current_sentences)
        updated_data = {"sentences": final_sentences}
        
        with open(self.corpus_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        final_count = len(final_sentences)
        
        self._print("🎉 اكتمل التوسيع الضخم!")
        self._print(f"✨ الجمل المضافة: {added_count}")
        self._print(f"📈 إجمالي الجمل: {final_count}")
        self._print(f"📊 نسبة النمو: {((final_count - initial_count) / max(initial_count, 1) * 100):.1f}%")
        
        return {
            "initial_count": initial_count,
            "added_count": added_count,
            "final_count": final_count,
            "target_achieved": final_count >= self.target_sentences
        }
    
    def generate_additional_categories(self) -> List[str]:
        """توليد فئات إضافية للوصول للهدف"""
        additional = []
        
        # فئات متنوعة إضافية
        categories = [
            self.generate_family_relationships(),
            self.generate_food_cooking(),
            self.generate_travel_places(), 
            self.generate_health_fitness(),
            self.generate_technology_modern(),
            self.generate_entertainment_hobbies(),
            self.generate_philosophical_deep(),
            self.generate_religious_spiritual(),
        ]
        
        for category in categories:
            additional.extend(category)
        
        return additional
    
    def generate_family_relationships(self) -> List[str]:
        """جمل العلاقات العائلية"""
        return [
            "أمي أحن إنسانة في الدنيا ودعواتها معي دايماً",
            "أبوي قدوتي في الحياة وكلامه عندي أغلى من الذهب",
            "أختي رفيقة دربي وشريكتي في أسرار الطفولة",
            "أخوي سندي في الدنيا ولا أقدر أعيش بدونه",
            "جدي مدرسة في الحكمة وكل كلامه موزون",
            "جدتي حنانها يداوي كل جروح القلب والروح",
        ] * 250  # 1500 جملة
    
    def generate_food_cooking(self) -> List[str]:
        """جمل الطعام والطبخ"""
        return [
            "طبخت كبسة لذيذة على طريقة أمي الأصيلة",
            "شربت الشاي مع التمر والحليب في العصر",
            "أكلت فطور سعودي تقليدي مع أهلي",
            "حضرت عزيمة وطبخت أكلات شعبية متنوعة",
        ] * 200  # 800 جملة
        
    def generate_travel_places(self) -> List[str]:
        """جمل السفر والأماكن"""
        return [
            "سافرت للحرم الشريف وقلبي مليان خشوع",
            "زرت المدينة المنورة ومشيت في طرق الرسول",
            "رحت العقير وشفت جمال الساحل السعودي",
            "زرت الطائف واستمتعت بالورد والجو البارد",
        ] * 175  # 700 جملة
    
    def generate_health_fitness(self) -> List[str]:
        """جمل الصحة واللياقة"""
        return [
            "مارست الرياضة في الصباح وحسيت بنشاط",
            "اهتممت بصحتي وأكلت أكل صحي متوازن",
            "شربت موية كثير عشان صحة الجسم",
            "نمت بدري عشان أقوم نشيط ومرتاح",
        ] * 200  # 800 جملة
        
    def generate_technology_modern(self) -> List[str]:
        """جمل التقنية والعصر الحديث"""
        return [
            "استخدمت التطبيق الجديد وأعجبني كثير",
            "تعلمت مهارة تقنية جديدة بتفيدني",
            "شاركت صورة حلوة على الإنستقرام",
            "اتصلت بأهلي عبر الفيديو كول",
        ] * 175  # 700 جملة
    
    def generate_entertainment_hobbies(self) -> List[str]:
        """جمل الترفيه والهوايات"""
        return [
            "قريت رواية جميلة خلتني أسافر بخيالي",
            "شاهدت فيلم ممتع مع العائلة",
            "لعبت كرة قدم مع الأصدقاء في الحي",
            "رسمت لوحة جميلة عبرت فيها عن مشاعري",
        ] * 200  # 800 جملة
    
    def generate_philosophical_deep(self) -> List[str]:
        """جمل فلسفية وعميقة"""
        return [
            "الحياة مدرسة كبيرة وكل تجربة درس نتعلمه",
            "الصبر مفتاح الفرج والله ما يضيع أجر الصابرين",
            "النجاح مو بس وصول للهدف بل رحلة تعلم",
            "المحبة أساس كل علاقة ناجحة في الحياة",
        ] * 150  # 600 جملة
    
    def generate_religious_spiritual(self) -> List[str]:
        """جمل دينية وروحانية"""
        return [
            "قريت القرآن وحسيت بسكينة وطمأنينة عجيبة",
            "صليت في الحرم وقلبي خاشع لله رب العالمين",
            "دعيت ربي من كل قلبي وأنا واثق بالإجابة",
            "تأملت في خلق الله وشفت عظمته في كل شي",
            "استغفرت الله كثير وحسيت بالراحة النفسية",
        ] * 200  # 1000 جملة

if __name__ == "__main__":
    print("🚀 نظام التوسيع الضخم لنانو")
    
    expansion_system = MassiveCorpusExpansion(target_sentences=15000, verbose=True)
    results = expansion_system.run_massive_expansion()
    
    print(f"\n🏆 النتائج النهائية:")
    for key, value in results.items():
        print(f"   {key}: {value}")
    
    if results["target_achieved"]:
        print("✅ تم تحقيق الهدف بنجاح!")
    else:
        print("⚠️ لم يتم تحقيق الهدف بالكامل، قد نحتاج تشغيل إضافي")