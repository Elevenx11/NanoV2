# massive_expansion_improved.py - نظام التوسيع الضخم المحسن لنانو
import json
import random
import itertools
from typing import List, Dict, Set
from continuous_learning import ContinuousLearningSystem

class ImprovedMassiveExpansion(ContinuousLearningSystem):
    """نظام التوسيع الضخم المحسن للوصول إلى 15000+ جملة فريدة"""
    
    def __init__(self, target_sentences: int = 15000, verbose: bool = True):
        super().__init__(verbose=verbose)
        self.target_sentences = target_sentences
        
    def generate_smart_variations(self, base_sentences: List[str], target_count: int) -> List[str]:
        """توليد تنويعات ذكية ومتطورة من الجمل الأساسية"""
        variations = set()  # استخدام set لضمان عدم التكرار
        
        # مكونات التنويع الذكي
        time_variations = ["اليوم", "امبارح", "بكرة", "الصبح", "المسا", "العصر", "الفجر", "المغرب", "الضحى", "العشر", "الليل"]
        emotion_variations = ["مبسوط", "فرحان", "سعيد", "مرتاح", "هادي", "مطمئن", "راضي", "منشرح", "مبهور", "معجب", "متحمس"]
        family_variations = ["أمي", "أبوي", "أختي", "أخوي", "جدي", "جدتي", "العائلة", "الأهل", "الولد", "البنت", "العم", "الخال"]
        place_variations = ["البيت", "المسجد", "الشارع", "الحي", "السوق", "الجامعة", "المدرسة", "العمل", "الحديقة", "المكتب"]
        
        # تنويعات البدايات والنهايات
        prefixes = [
            "", "الحمدلله ", "والله ", "أحمد الله ", "بصراحة ", "صدقني ", 
            "أقسم بالله ", "من قلبي ", "بكل أمانة ", "والله العظيم ",
            "إن شاء الله ", "بإذن الله ", "يا رب ", "اللهم "
        ]
        
        suffixes = [
            "", " والحمدلله", " إن شاء الله", " بإذن الله", " ربي يكرمك", 
            " الله يعطيك العافية", " جزاك الله خير", " ما قصرت", 
            " تسلم إيدك", " بارك الله فيك", " كثر خيرك", " زادك الله نور"
        ]
        
        # توليد التنويعات المتقدمة
        for base in base_sentences:
            # تنويعات مباشرة أولى
            for _ in range(target_count // len(base_sentences) + 5):
                varied = base
                
                # استبدالات ذكية متعددة المستويات
                for old_word, replacements in [
                    ("اليوم", time_variations),
                    ("فرحان", emotion_variations), 
                    ("مبسوط", emotion_variations),
                    ("أمي", family_variations),
                    ("البيت", place_variations)
                ]:
                    if old_word in varied:
                        varied = varied.replace(old_word, random.choice(replacements))
                
                # إضافة تنويعات في المقدمة والخاتمة
                prefix = random.choice(prefixes)
                suffix = random.choice(suffixes)
                final_variation = prefix + varied + suffix
                
                variations.add(final_variation.strip())
                
                # تنويعات إضافية بتغييرات هيكلية
                if len(variations) < target_count:
                    # تنويع في الصيغة
                    if "قمت" in varied:
                        structural_var = varied.replace("قمت", random.choice(["صحيت", "فقت", "قعدت من النوم"]))
                        variations.add(prefix + structural_var + suffix)
                    
                    if "سويت" in varied:
                        structural_var = varied.replace("سويت", random.choice(["عملت", "قمت بـ", "أنجزت"]))
                        variations.add(prefix + structural_var + suffix)
                    
                    if "حسيت" in varied:
                        structural_var = varied.replace("حسيت", random.choice(["شعرت", "أحسست", "لقيت نفسي"]))
                        variations.add(prefix + structural_var + suffix)
                
                if len(variations) >= target_count:
                    break
            
            if len(variations) >= target_count:
                break
        
        return list(variations)[:target_count]
    
    def generate_daily_life_massive(self) -> List[str]:
        """توليد جمل الحياة اليومية الضخمة"""
        base_daily = [
            "قمت من النوم على صوت الأذان", "شربت قهوتي العربية وأنا أشوف الطيور",
            "الفجر اليوم كان جميل والجو منعش", "بديت يومي بالبسملة", "صليت الفجر في المسجد",
            "المغرب اليوم كان هادي", "سهرت مع الأهل وقضينا وقت حلو", "نمت مبكر عشان أقوم نشيط",
            "استغفرت قبل النوم", "اشتغلت في البيت ونظفت", "طبخت وجبة لذيذة لعائلتي",
            "غسلت الملابس وكويتها", "سقيت النباتات وعتنيت بالحديقة", "رتبت المكتبة وقريت كتاب",
            "شاهدت برنامج مفيد", "لعبت مع الأطفال وضحكنا", "استمعت للقرآن", "اتصلت بصديق قديم",
            "تمشيت في الحي وسلمت على الجيران", "حسيت بالامتنان لنعم الله", "فرحت لأن يومي كان حلو",
            "تعبت شوي بس مرتاح", "حسيت بالرضا", "استمتعت بالوقت", "شعرت بالطمأنينة",
            "حمدت الله على الصحة", "سعدت لأن تعلمت شي جديد", "أعجبني كلام حلو سمعته",
            "تأثرت من قصة مؤثرة", "مارست الرياضة في الصباح", "أكلت فطور صحي ولذيذ",
            "زرت الأقارب وقضيت معهم وقت جميل", "ساعدت جاري في موضوع", "تسوقت من السوق الشعبي",
            "جلست في البلكونة أتأمل الطبيعة", "رتبت أوراقي ومستنداتي", "نظفت السيارة ولمعتها",
            "سمعت أخبار حلوة فرحت لها", "شربت شاي مع النعناع", "قريت في الجوال أشياء مفيدة"
        ]
        return self.generate_smart_variations(base_daily, 2500)
    
    def generate_emotions_massive(self) -> List[str]:
        """توليد المشاعر المتقدمة الضخمة"""
        base_emotions = [
            "فرحان وحزين في نفس الوقت", "خايف ومتحمس للتحدي الجديد", "مشتاق لأهلي وراضي عن قراري",
            "متضايق من الموقف بس فاهم الحكمة", "محتار بين خيارين", "مبسوط من الداخل رغم التعب",
            "حاسس بالوحدة رغم إني مع ناس", "هادي من برا بس جواي عاصفة", "متفائل بالمستقبل رغم الصعوبة",
            "محب للحياة رغم المشاكل", "شعرت بحنين خفيف للطفولة", "حسيت بفخر صامت", "تأثرت من كرم شخص غريب",
            "استاء من طريقة الكلام", "أعجبت بالهدوء في العيون", "انتابني شعور غريب بالحنين", "شعرت بالخجل من الثناء",
            "تملكني إحساس بالمسؤولية", "شعرت بالضعف أمام عظمة الخلق", "أحسست بالطمأنينة في المصاعب",
            "بكيت من الفرح لما سمعت الخبر", "ضحكت من قلبي أول مرة من زمان", "صرخت من الخوف", "سكت كثير وأنا أفكر",
            "عضيت على شفتي من الغضب", "غمضت عيني وتنهدت", "ابتسمت ابتسامة حزينة", "هزيت راسي بالموافقة",
            "حبست دمعتي عشان ما أبكي", "فتحت عيني بدهشة", "امتلأ قلبي بالرحمة", "شعرت بالذنب على تقصيري",
            "حسيت بالندم على كلام قلته", "فخرت بإنجاز حققته", "خجلت من مدح كثير", "انبسطت من مفاجأة حلوة",
            "حزنت على فراق عزيز", "غضبت من ظلم شفته", "خفت من المستقبل المجهول", "اطمأننت بعد قلق طويل"
        ]
        return self.generate_smart_variations(base_emotions, 2000)
    
    def generate_social_massive(self) -> List[str]:
        """توليد التفاعلات الاجتماعية الضخمة"""
        base_social = [
            "جلست مع صديقي نتكلم عن أحلامنا", "ناقشت مع أبوي موضوع مهم", "تبادلت الآراء مع زملائي",
            "استمعت لقصة جدي عن الماضي", "شاركت تجربتي مع شخص", "طلبت نصيحة من أمي", "أعطيت رأيي بصراحة",
            "تعلمت شي جديد من محادثة", "شرحت وجهة نظري", "استفدت من تجارب الآخرين", "رحبت بالضيوف بحفاوة",
            "شكرت الشخص اللي ساعدني", "اعتذرت عن خطئي بصدق", "باركت لصديقي إنجازه", "عزيت جاري في فقدانه",
            "هنأت زميلي بترقيته", "قدمت واجب العزاء", "زرت مريض وطمأنت على صحته", "دعيت صديق لحضور مناسبة",
            "شاركت في فرحة قريب", "تدخلت بحكمة في مشكلة", "صالحت بين أخوين", "حليت خلاف في العمل",
            "وقفت موقف عادل", "اقترحت حل وسط", "تنازلت عن حقي لأجل السلام", "اعترفت بخطئي وطلبت السماح",
            "سامحت شخص أذاني", "تجاهلت كلام جارح", "دعوت للهدوء والتفاهم", "نصحت شخص بحكمة",
            "استشرت أهل الخبرة في موضوع", "احترمت رأي يخالف رأيي", "قدرت ظروف شخص صعبة", "وقفت مع المظلوم",
            "دافعت عن الحق بأدب", "أكرمت ضيف في بيتي", "قدمت خدمة لمحتاج", "ساندت صديق في أزمة"
        ]
        return self.generate_smart_variations(base_social, 2500)
    
    def generate_cultural_massive(self) -> List[str]:
        """توليد التعبيرات الثقافية الضخمة"""
        base_cultural = [
            "بيتنا بيتك وكل اللي عندنا لك", "أهلاً وسهلاً بك يا أهل وفين", "على الرحب والسعة يا غالي",
            "حياك الله وزادك رفعة", "الله يعطيك العافية والقوة", "بارك الله فيك وفي أهلك", "الله يجعله في ميزان حسناتك",
            "بعد إذنك إن شاء الله", "يا هلا باللي نور المكان", "كثر خيرك وقل شرك", "زادك الله من فضله وكرمه",
            "على بركة الرحمن يا رب", "ما قصرت يا خوي جزاك الله خير", "والله يعطيك على قد نيتك",
            "يعطيك العافية في قلبك ودينك", "الحمدلله اللي جمعنا على خير", "ما شاء الله تبارك الرحمن",
            "سبحان الله وبحمده رب العالمين", "الله م حد عليه وأجيح الخالق", "قدرنا عندك وإن قل زادنا شرف",
            "عينك علينا باردة يا غالي", "عساك على القوة يا هل الطيب", "الله يوفقك لكل خير", "من جد وجد ومن زرع حصد",
            "الصبر مفتاح الفرج بإذن الله", "الحمدلله رب العالمين على كل النعم", "لا إله إلا الله محمد رسول الله",
            "اللهم اعز الإسلام والمسلمين", "تقبل الله منا ومنكم صالح الأعمال", "ما نخليك تروح إلا بعد العشا",
            "الضيف عزيز وله كل التقدير", "أهلاً وسهلاً مية مرحبا فيك", "نورت البيت بوجودك الكريم",
            "تفضل اجعل نفسك في بيتك", "عساك على القوة وما قصرت", "الله يكرمك زي ما كرمتنا بالزيارة"
        ]
        return self.generate_smart_variations(base_cultural, 2000)
    
    def generate_work_education_massive(self) -> List[str]:
        """توليد جمل العمل والتعليم الضخمة"""
        base_work = [
            "حضرت اجتماع مهم في الشركة", "أنجزت مشروعي في الجامعة", "تعلمت مهارة جديدة", "درست لامتحان مهم",
            "عملت بجد واجتهاد", "شاركت في دورة تدريبية", "تعاونت مع زملائي في العمل", "قدمت عرض للمدير",
            "نجحت في الامتحان", "تخرجت من الجامعة", "حصلت على شهادة", "بدأت وظيفة جديدة", "ترقيت في العمل",
            "أكملت بحثي", "حاضرت مؤتمر علمي", "ذاكرت دروسي بتركيز", "شاركت في الحصة بفعالية", "ساعدت زميل يتعلم",
            "قريت كتاب مفيد زاد معرفتي", "بحثت عن معلومات لمشروعي", "حضرت محاضرة ثرية", "ناقشت مع الأستاذ",
            "راجعت ملاحظاتي للامتحان", "تعلمت مهارة تقنية جديدة", "شرحت لطالب صغير واجبه", "نجحت في مشروع صعب",
            "حصلت على تقدير ممتاز", "رقيت بسبب اجتهادي", "فزت في مسابقة ثقافية", "حققت هدف كان صعب",
            "تخرجت بدرجة امتياز", "حصلت على وظيفة أحلامي", "أكملت الدورة بنجاح", "قدمت عرض أعجب الجميع"
        ]
        return self.generate_smart_variations(base_work, 1500)
    
    def generate_family_massive(self) -> List[str]:
        """توليد جمل العلاقات العائلية الضخمة"""
        base_family = [
            "أمي أحن إنسانة في الدنيا", "أبوي قدوتي في الحياة", "أختي رفيقة دربي", "أخوي سندي في الدنيا",
            "جدي مدرسة في الحكمة", "جدتي حنانها يداوي الجروح", "العائلة هي أهم شي في حياتي", "أحب أهلي أكثر من روحي",
            "زرت أهلي وقضينا وقت حلو", "تعلمت من تجارب الأهل", "فخور بعائلتي وأصلي", "دعوات الوالدين بركة",
            "بر الوالدين طريق الجنة", "أختي شريكتي في كل شي", "أخوي ما يقصر معي أبداً", "جدي يحكي قصص الماضي الحلو",
            "جدتي تطبخ أحلى أكل", "العيلة تجتمع في المناسبات", "أهلي يسعدون لنجاحي", "أساند أهلي في كل الظروف",
            "أخوي الصغير ذكي وحبوب", "أختي تساعدني في كل شي", "أمي تدعي لي كل يوم", "أبوي يعطيني نصائح حكيمة",
            "أحضن أمي وأقول لها أحبك", "أساعد أبوي في شغل البيت", "أعطي أخوي من مصروفي", "أقضي وقت مع أهلي",
            "أستشير أهلي في قراراتي", "أفرح أهلي بنجاحاتي", "أبر والديا وأطيعهما", "أكرم أهلي وأحترمهم"
        ]
        return self.generate_smart_variations(base_family, 2000)
    
    def generate_additional_categories(self) -> List[str]:
        """توليد فئات إضافية متنوعة"""
        # الطعام والطبخ
        food_base = [
            "طبخت كبسة لذيذة على طريقة أمي", "شربت الشاي مع التمر والحليب", "أكلت فطور سعودي تقليدي",
            "حضرت عزيمة وطبخت أكلات شعبية", "دعيت الأصدقاء على غداء بيتي", "جربت وصفة جديدة من النت"
        ]
        
        # السفر والأماكن
        travel_base = [
            "سافرت للحرم الشريف وقلبي مليان خشوع", "زرت المدينة المنورة ومشيت في طرق الرسول",
            "رحت العقير وشفت جمال الساحل", "زرت الطائف واستمتعت بالورد", "سافرت لبلد جديد وتعلمت ثقافتهم"
        ]
        
        # الصحة واللياقة  
        health_base = [
            "مارست الرياضة في الصباح وحسيت بنشاط", "اهتممت بصحتي وأكلت أكل صحي", "شربت موية كثير عشان الصحة",
            "نمت بدري عشان أقوم نشيط", "مشيت في الحي عشان أتحرك", "لعبت كرة قدم مع الأصدقاء"
        ]
        
        # التقنية والعصر الحديث
        tech_base = [
            "استخدمت التطبيق الجديد وأعجبني", "تعلمت مهارة تقنية جديدة", "شاركت صورة حلوة على الإنستقرام",
            "اتصلت بأهلي عبر الفيديو كول", "قريت كتاب إلكتروني مفيد", "تعلمت من فيديو تعليمي على اليوتيوب"
        ]
        
        # الترفيه والهوايات
        entertainment_base = [
            "قريت رواية جميلة خلتني أسافر بخيالي", "شاهدت فيلم ممتع مع العائلة", "لعبت كرة قدم مع الأصدقاء",
            "رسمت لوحة جميلة عبرت فيها عن مشاعري", "سمعت موسيقى هادئة ترخي الأعصاب", "لعبت ألعاب الطاولة مع الأهل"
        ]
        
        # الدين والروحانيات
        religious_base = [
            "قريت القرآن وحسيت بسكينة عجيبة", "صليت في الحرم وقلبي خاشع لله", "دعيت ربي من كل قلبي",
            "تأملت في خلق الله وشفت عظمته", "استغفرت الله كثير وحسيت بالراحة", "حفظت سورة جديدة من القرآن",
            "صليت قيام الليل وناجيت ربي", "قريت في كتب التفسير", "سمعت خطبة مؤثرة في الجمعة"
        ]
        
        additional = []
        additional.extend(self.generate_smart_variations(food_base, 800))
        additional.extend(self.generate_smart_variations(travel_base, 700))
        additional.extend(self.generate_smart_variations(health_base, 800))
        additional.extend(self.generate_smart_variations(tech_base, 700))
        additional.extend(self.generate_smart_variations(entertainment_base, 800))
        additional.extend(self.generate_smart_variations(religious_base, 1200))
        
        return additional
    
    def run_improved_massive_expansion(self) -> Dict[str, int]:
        """تشغيل التوسيع الضخم المحسن"""
        self._print("🚀 بدء التوسيع الضخم المحسن لنانو إلى 15000+ جملة فريدة")
        self._print("=" * 70)
        
        # تحميل الحالة الحالية
        try:
            with open(self.corpus_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                current_sentences = set(data.get("sentences", []))
        except:
            current_sentences = set()
        
        initial_count = len(current_sentences)
        self._print(f"📊 الجمل الحالية: {initial_count}")
        
        # توليد جمل جديدة متقدمة
        all_new_sentences = []
        
        categories = [
            ("الحياة اليومية", self.generate_daily_life_massive),
            ("المشاعر المتقدمة", self.generate_emotions_massive), 
            ("التفاعلات الاجتماعية", self.generate_social_massive),
            ("التعبيرات الثقافية", self.generate_cultural_massive),
            ("العمل والتعليم", self.generate_work_education_massive),
            ("العلاقات العائلية", self.generate_family_massive)
        ]
        
        for category_name, method in categories:
            self._print(f"📝 توليد جمل {category_name}...")
            category_sentences = method()
            all_new_sentences.extend(category_sentences)
            self._print(f"   ✅ تم توليد {len(category_sentences)} جملة")
        
        # إضافة الفئات الإضافية
        self._print("📝 توليد الفئات الإضافية...")
        additional_sentences = self.generate_additional_categories()
        all_new_sentences.extend(additional_sentences)
        self._print(f"   ✅ تم توليد {len(additional_sentences)} جملة إضافية")
        
        # تصفية ومعالجة الجمل
        self._print("🔍 تصفية ومعالجة الجمل الجديدة...")
        processed = self.process_and_filter_sentences(all_new_sentences)
        
        # إضافة الجمل الفريدة فقط
        added_count = 0
        for sentence in processed:
            if sentence not in current_sentences and len(sentence.strip()) > 5:
                current_sentences.add(sentence.strip())
                added_count += 1
        
        # حفظ النتائج
        final_sentences = list(current_sentences)
        updated_data = {"sentences": final_sentences}
        
        with open(self.corpus_path, 'w', encoding='utf-8') as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=2)
        
        final_count = len(final_sentences)
        
        self._print("🎉 اكتمل التوسيع الضخم المحسن!")
        self._print(f"✨ الجمل المضافة الجديدة: {added_count}")
        self._print(f"📈 إجمالي الجمل: {final_count}")
        self._print(f"📊 نسبة النمو: {((final_count - initial_count) / max(initial_count, 1) * 100):.1f}%")
        
        if final_count >= self.target_sentences:
            self._print("✅ تم تحقيق الهدف بنجاح!")
        else:
            remaining = self.target_sentences - final_count
            self._print(f"⚡ متبقي {remaining} جملة لتحقيق الهدف الكامل")
        
        return {
            "initial_count": initial_count,
            "added_count": added_count,
            "final_count": final_count,
            "target_achieved": final_count >= self.target_sentences,
            "growth_percentage": ((final_count - initial_count) / max(initial_count, 1) * 100)
        }

if __name__ == "__main__":
    print("🚀 نظام التوسيع الضخم المحسن لنانو")
    print("=" * 50)
    
    expansion_system = ImprovedMassiveExpansion(target_sentences=15000, verbose=True)
    results = expansion_system.run_improved_massive_expansion()
    
    print(f"\n🏆 النتائج النهائية:")
    for key, value in results.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.1f}")
        else:
            print(f"   {key}: {value}")
    
    if results["target_achieved"]:
        print("\n🎊 مبروك! تم تحقيق الهدف بنجاح!")
        print("🔥 نانو الآن لديه أكثر من 15000 جملة تدريبية عالية الجودة!")
    else:
        print(f"\n⚡ إنجاز رائع! تم إضافة {results['added_count']} جملة جديدة")
        print("🔄 يمكن تشغيل النظام مرة أخرى لإضافة المزيد")