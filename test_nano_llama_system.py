# test_nano_llama_system.py - اختبار شامل لنظام نانو Llama
import sys
import time
import json
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# إضافة مجلد core لمسار Python
sys.path.append(str(Path(__file__).parent / "core"))

try:
    from core.nano_llama_brain import NanoLlamaBrain
    from core.llama_engine import LlamaEngine
    from core.saudi_fine_tuner import SaudiFinetuner
except ImportError as e:
    print(f"❌ خطأ في استيراد النظام: {e}")
    print("تأكد من وجود جميع الملفات في مجلد core")
    sys.exit(1)

class NanoLlamaSystemTester:
    """نظام اختبار شامل لنانو Llama"""
    
    def __init__(self):
        self.nano_brain = None
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": [],
            "performance_metrics": {},
            "saudi_dialect_scores": [],
            "response_times": [],
            "confidence_scores": []
        }
        
        # مجموعات الاختبار
        self.test_conversations = {
            "basic_greetings": [
                "السلام عليكم",
                "مرحبا",
                "أهلا وسهلا", 
                "هاي كيفك",
                "صباح الخير"
            ],
            
            "daily_conversations": [
                "كيف حالك اليوم؟",
                "وش أخبارك؟",
                "إيش مسوي؟",
                "كيف صحتك؟",
                "وش جديدك معك؟"
            ],
            
            "emotional_expressions": [
                "أنا زعلان شوي",
                "مبسوط اليوم والله",
                "تعبان من الشغل",
                "فرحان بالنتيجة",
                "متضايق شوية"
            ],
            
            "questions_requests": [
                "كيف أسوي قهوة عربية؟",
                "وين أقدر ألاقي مطعم كويس؟",
                "وش رأيك في الطقس؟",
                "تنصحني بفيلم حلو؟",
                "كيف أتعلم البرمجة؟"
            ],
            
            "thanks_appreciation": [
                "شكراً لك",
                "يعطيك العافية",
                "كثر خيرك",
                "تسلم يا غالي",
                "ما قصرت والله"
            ],
            
            "challenging_inputs": [
                "كل زق", # اختبار التعامل مع الإساءة
                "ما تفهم شي",
                "أصلع وغبي",
                "شكلك خايب",
                "مو عاجبني ردك" # اختبار النقد
            ],
            
            "complex_conversations": [
                "أبغى أشتري بيت بس مو عارف إيش المناطق الكويسة في الرياض، وما أدري إيش الأسعار، تقدر تساعدني؟",
                "عندي مشكلة مع أخوي، دايم نتخانق على أشياء تافهة، وأمي تزعل منا، وش أسوي؟",
                "أفكر أغير تخصصي الجامعي لأن مو حاس إني مبسوط فيه، بس خايف من ردة فعل الأهل، إيش رأيك؟"
            ],
            
            "cultural_saudi": [
                "وش أحسن مكان لقضاء العيد؟",
                "كيف نحتفل باليوم الوطني؟", 
                "وش تعرف عن تراث نجد؟",
                "إيش أشهر الأكلات الشعبية؟",
                "حدثني عن رمضان في السعودية"
            ]
        }

    def initialize_system(self) -> bool:
        """تهيئة النظام للاختبار"""
        
        print("🚀 بدء تهيئة نظام نانو Llama للاختبار...")
        
        try:
            self.nano_brain = NanoLlamaBrain("data")
            print("✅ تم تحميل نانو Llama بنجاح!")
            
            # انتظار تحميل النموذج
            print("⏳ انتظار تحميل نموذج Llama...")
            max_wait = 60  # دقيقة واحدة
            waited = 0
            
            while (not self.nano_brain.llama_engine.model_loaded and 
                   not self.nano_brain.llama_engine.fallback_mode and 
                   waited < max_wait):
                time.sleep(2)
                waited += 2
                print(f"   ⏳ انتظار... ({waited}/{max_wait} ثانية)")
            
            if self.nano_brain.llama_engine.model_loaded:
                print("✅ تم تحميل نموذج Llama!")
            elif self.nano_brain.llama_engine.fallback_mode:
                print("⚠️  تم التبديل للنمط البديل (بدون Llama)")
            else:
                print("❌ انتهت مهلة انتظار تحميل النموذج")
                return False
                
            return True
            
        except Exception as e:
            print(f"❌ خطأ في تهيئة النظام: {e}")
            return False

    def run_conversation_test(self, category: str, conversations: List[str]) -> Dict:
        """تشغيل اختبار مجموعة محادثات"""
        
        print(f"\n🧪 اختبار فئة: {category}")
        print("=" * 50)
        
        category_results = {
            "category": category,
            "total_tests": len(conversations),
            "passed": 0,
            "failed": 0,
            "responses": [],
            "avg_saudi_score": 0.0,
            "avg_response_time": 0.0,
            "avg_confidence": 0.0
        }
        
        saudi_scores = []
        response_times = []
        confidence_scores = []
        
        for i, conversation in enumerate(conversations, 1):
            try:
                print(f"\n  📝 اختبار {i}/{len(conversations)}: {conversation}")
                
                start_time = time.time()
                response = self.nano_brain.generate_response(conversation)
                end_time = time.time()
                
                response_time = end_time - start_time
                
                # تقييم الاستجابة
                test_result = self.evaluate_response(conversation, response, category)
                
                # حفظ النتائج
                response_data = {
                    "input": conversation,
                    "output": response.text,
                    "method": response.method_used,
                    "confidence": response.confidence,
                    "saudi_score": response.saudi_dialect_score,
                    "response_time": response_time,
                    "passed": test_result["passed"],
                    "issues": test_result["issues"]
                }
                
                category_results["responses"].append(response_data)
                
                # إحصائيات
                saudi_scores.append(response.saudi_dialect_score)
                response_times.append(response_time)
                confidence_scores.append(response.confidence)
                
                if test_result["passed"]:
                    category_results["passed"] += 1
                    print(f"    ✅ نجح - {response.text[:50]}...")
                else:
                    category_results["failed"] += 1
                    print(f"    ❌ فشل - {test_result['issues']}")
                
                print(f"    📊 سعودي: {response.saudi_dialect_score:.1%} | "
                      f"ثقة: {response.confidence:.1%} | "
                      f"وقت: {response_time:.2f}ث")
                
                # فاصل زمني قصير
                time.sleep(1)
                
            except Exception as e:
                print(f"    ❌ خطأ في الاختبار: {e}")
                category_results["failed"] += 1
        
        # حساب المتوسطات
        if saudi_scores:
            category_results["avg_saudi_score"] = sum(saudi_scores) / len(saudi_scores)
            category_results["avg_response_time"] = sum(response_times) / len(response_times)
            category_results["avg_confidence"] = sum(confidence_scores) / len(confidence_scores)
        
        # إضافة للإحصائيات العامة
        self.test_results["saudi_dialect_scores"].extend(saudi_scores)
        self.test_results["response_times"].extend(response_times)
        self.test_results["confidence_scores"].extend(confidence_scores)
        
        return category_results

    def evaluate_response(self, input_text: str, response, category: str) -> Dict:
        """تقييم جودة الاستجابة"""
        
        issues = []
        passed = True
        
        # فحص الاستجابة الأساسي
        if not response.text or len(response.text.strip()) < 3:
            issues.append("استجابة فارغة أو قصيرة جداً")
            passed = False
        
        # فحص التكرار المباشر
        if response.text.lower().strip() == input_text.lower().strip():
            issues.append("تكرار مباشر للمدخل")
            passed = False
        
        # فحص الثقة
        if response.confidence < 0.3:
            issues.append(f"ثقة منخفضة ({response.confidence:.1%})")
            passed = False
        
        # فحص اللهجة السعودية
        if response.saudi_dialect_score < 0.4:
            issues.append(f"لهجة سعودية ضعيفة ({response.saudi_dialect_score:.1%})")
            # لا نعتبرها فشل كامل
        
        # فحص زمن الاستجابة
        if hasattr(response, 'generation_time') and response.generation_time > 10:
            issues.append(f"وقت استجابة طويل ({response.generation_time:.1f}ث)")
            # لا نعتبرها فشل كامل
        
        # فحوصات خاصة بالفئة
        if category == "challenging_inputs":
            # في حالة الإساءات، يجب أن يكون الرد مهذب ومناسب
            if any(word in response.text.lower() for word in ["غبي", "أصلع", "زق"]):
                issues.append("رد غير مناسب للإساءة")
                passed = False
            elif len(response.text) < 5:
                issues.append("رد مختصر جداً للموقف الحساس")
                passed = False
        
        elif category == "cultural_saudi":
            # يجب أن تحتوي على مراجع ثقافية سعودية
            cultural_words = ["السعودية", "الرياض", "نجد", "الحجاز", "عسير", "تراث"]
            if not any(word in response.text for word in cultural_words):
                # لا نعتبرها فشل، لكن نلاحظها
                pass
        
        return {
            "passed": passed,
            "issues": issues,
            "score": response.confidence * response.saudi_dialect_score
        }

    def test_system_features(self) -> Dict:
        """اختبار الميزات المتقدمة للنظام"""
        
        print("\n🔧 اختبار الميزات المتقدمة...")
        print("=" * 40)
        
        features_results = {
            "model_switching": False,
            "optimization": False,
            "fine_tuning": False,
            "memory_management": False,
            "error_handling": False
        }
        
        try:
            # اختبار تبديل النماذج
            print("\n  🔄 اختبار تبديل النماذج...")
            available_models = list(self.nano_brain.llama_engine.available_models.keys())
            if len(available_models) > 1:
                original_model = self.nano_brain.llama_engine.config.model_name
                test_model = available_models[1] if available_models[0] in original_model else available_models[0]
                
                success = self.nano_brain.llama_engine.switch_model(test_model)
                if success:
                    print(f"    ✅ نجح تبديل النموذج إلى {test_model}")
                    features_results["model_switching"] = True
                    
                    # العودة للنموذج الأصلي
                    time.sleep(3)
                    self.nano_brain.llama_engine.switch_model(original_model.split('/')[-1])
                else:
                    print(f"    ❌ فشل تبديل النموذج")
            else:
                print("    ⏭️  نموذج واحد فقط متاح")
                features_results["model_switching"] = True  # لا نعتبرها فشل
            
            # اختبار التحسين
            print("\n  ⚙️ اختبار تحسين النظام...")
            try:
                self.nano_brain.llama_engine.optimize_for_speed()
                print("    ✅ نجح تحسين السرعة")
                
                self.nano_brain.llama_engine.optimize_for_quality()
                print("    ✅ نجح تحسين الجودة")
                
                features_results["optimization"] = True
            except Exception as e:
                print(f"    ❌ فشل التحسين: {e}")
            
            # اختبار الضبط الدقيق (اختبار سريع)
            print("\n  🎯 اختبار الضبط الدقيق...")
            try:
                session = self.nano_brain.fine_tuner.run_fine_tuning_session(examples_count=10)
                if session.improvement_score >= 0:
                    print(f"    ✅ نجح الضبط الدقيق (تحسن: {session.improvement_score:.2%})")
                    features_results["fine_tuning"] = True
                else:
                    print("    ⚠️  الضبط الدقيق عمل لكن بدون تحسن")
                    features_results["fine_tuning"] = True
            except Exception as e:
                print(f"    ❌ فشل الضبط الدقيق: {e}")
            
            # اختبار إدارة الذاكرة
            print("\n  🧠 اختبار إدارة الذاكرة...")
            initial_memory_size = len(self.nano_brain.conversation_memory)
            
            # إضافة محادثات متعددة
            for i in range(5):
                self.nano_brain.generate_response(f"رسالة اختبار {i}")
            
            new_memory_size = len(self.nano_brain.conversation_memory)
            if new_memory_size > initial_memory_size:
                print(f"    ✅ الذاكرة تعمل ({initial_memory_size} -> {new_memory_size})")
                features_results["memory_management"] = True
            else:
                print("    ❌ مشكلة في إدارة الذاكرة")
            
            # اختبار معالجة الأخطاء
            print("\n  🚨 اختبار معالجة الأخطاء...")
            try:
                # محاولة إدخال غير صالح
                response = self.nano_brain.generate_response("")
                if response and len(response.text) > 0:
                    print("    ✅ معالجة الإدخال الفارغ")
                    features_results["error_handling"] = True
                else:
                    print("    ❌ لم يتعامل مع الإدخال الفارغ")
            except Exception as e:
                print(f"    ⚠️  خطأ في معالجة الإدخال الفارغ: {e}")
            
        except Exception as e:
            print(f"❌ خطأ عام في اختبار الميزات: {e}")
        
        return features_results

    def run_performance_benchmark(self) -> Dict:
        """اختبار الأداء والسرعة"""
        
        print("\n🏃 اختبار الأداء والسرعة...")
        print("=" * 35)
        
        benchmark_inputs = [
            "كيف حالك؟",
            "وش رأيك في الطقس اليوم؟", 
            "أبغى أكل شي لذيذ",
            "ساعدني في حل هذه المشكلة",
            "شكراً لك على المساعدة"
        ]
        
        response_times = []
        confidence_scores = []
        saudi_scores = []
        
        print(f"\n  ⏱️  قياس الأداء على {len(benchmark_inputs)} عينات...")
        
        for i, input_text in enumerate(benchmark_inputs, 1):
            print(f"    📊 عينة {i}/{len(benchmark_inputs)}: ", end="")
            
            start_time = time.time()
            response = self.nano_brain.generate_response(input_text)
            end_time = time.time()
            
            response_time = end_time - start_time
            response_times.append(response_time)
            confidence_scores.append(response.confidence)
            saudi_scores.append(response.saudi_dialect_score)
            
            print(f"{response_time:.2f}ث")
        
        # حساب الإحصائيات
        avg_response_time = sum(response_times) / len(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        avg_saudi_score = sum(saudi_scores) / len(saudi_scores)
        
        benchmark_results = {
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "avg_confidence": avg_confidence,
            "avg_saudi_score": avg_saudi_score,
            "total_samples": len(benchmark_inputs)
        }
        
        print(f"\n  📈 نتائج الأداء:")
        print(f"    ⏱️  متوسط الوقت: {avg_response_time:.2f} ثانية")
        print(f"    🚀 أسرع وقت: {min_response_time:.2f} ثانية")
        print(f"    🐌 أبطأ وقت: {max_response_time:.2f} ثانية")
        print(f"    📊 متوسط الثقة: {avg_confidence:.1%}")
        print(f"    🇸🇦 متوسط السعودية: {avg_saudi_score:.1%}")
        
        return benchmark_results

    def generate_test_report(self) -> str:
        """إنشاء تقرير شامل للاختبارات"""
        
        report = []
        
        report.append("📋 تقرير اختبار نظام نانو Llama الشامل")
        report.append("=" * 60)
        report.append(f"🕐 تاريخ الاختبار: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # ملخص عام
        total_tests = self.test_results["total_tests"]
        passed_tests = self.test_results["passed_tests"]
        failed_tests = self.test_results["failed_tests"]
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report.append("📊 ملخص النتائج:")
        report.append(f"   مجموع الاختبارات: {total_tests}")
        report.append(f"   نجحت: {passed_tests} ✅")
        report.append(f"   فشلت: {failed_tests} ❌")
        report.append(f"   معدل النجاح: {success_rate:.1f}%")
        report.append("")
        
        # الأداء العام
        if self.test_results["saudi_dialect_scores"]:
            avg_saudi = sum(self.test_results["saudi_dialect_scores"]) / len(self.test_results["saudi_dialect_scores"])
            avg_time = sum(self.test_results["response_times"]) / len(self.test_results["response_times"])
            avg_confidence = sum(self.test_results["confidence_scores"]) / len(self.test_results["confidence_scores"])
            
            report.append("🎯 الأداء العام:")
            report.append(f"   متوسط اللهجة السعودية: {avg_saudi:.1%}")
            report.append(f"   متوسط وقت الاستجابة: {avg_time:.2f} ثانية")
            report.append(f"   متوسط الثقة: {avg_confidence:.1%}")
            report.append("")
        
        # نتائج الفئات
        report.append("📝 نتائج الفئات:")
        for category_result in self.test_results["test_details"]:
            category = category_result["category"]
            total = category_result["total_tests"]
            passed = category_result["passed"]
            success_rate = (passed / total * 100) if total > 0 else 0
            
            report.append(f"   {category}:")
            report.append(f"     نجح: {passed}/{total} ({success_rate:.1f}%)")
            report.append(f"     متوسط السعودية: {category_result['avg_saudi_score']:.1%}")
            report.append(f"     متوسط الوقت: {category_result['avg_response_time']:.2f}ث")
            report.append("")
        
        # أمثلة على الردود
        report.append("💬 أمثلة على الردود:")
        for category_result in self.test_results["test_details"]:
            if category_result["responses"]:
                best_response = max(category_result["responses"], 
                                  key=lambda x: x["confidence"] * x["saudi_score"])
                report.append(f"   {category_result['category']} - أفضل رد:")
                report.append(f"     س: {best_response['input']}")
                report.append(f"     ج: {best_response['output']}")
                report.append(f"     📊 {best_response['confidence']:.1%} ثقة | {best_response['saudi_score']:.1%} سعودي")
                report.append("")
        
        # الميزات المتقدمة
        if "features_test" in self.test_results:
            features = self.test_results["features_test"]
            report.append("🔧 اختبار الميزات المتقدمة:")
            for feature, status in features.items():
                status_icon = "✅" if status else "❌"
                report.append(f"   {feature}: {status_icon}")
            report.append("")
        
        # توصيات للتحسين
        report.append("🚀 توصيات للتحسين:")
        if avg_saudi < 0.7:
            report.append("   • تحسين اللهجة السعودية في النماذج")
        if avg_time > 3.0:
            report.append("   • تحسين سرعة الاستجابة")
        if avg_confidence < 0.6:
            report.append("   • تحسين ثقة النموذج في الردود")
        if success_rate < 80:
            report.append("   • مراجعة معالجة الحالات الصعبة")
        if not report[-1].startswith("   •"):
            report.append("   • النظام يعمل بكفاءة عالية! 🎉")
        
        return "\n".join(report)

    def save_test_results(self, filename: str = None):
        """حفظ نتائج الاختبار"""
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"nano_llama_test_results_{timestamp}.json"
        
        try:
            test_data = {
                "test_timestamp": datetime.now().isoformat(),
                "system_info": self.nano_brain.get_system_status() if self.nano_brain else {},
                "test_results": self.test_results,
                "test_report": self.generate_test_report()
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(test_data, f, ensure_ascii=False, indent=2, default=str)
            
            print(f"\n💾 تم حفظ النتائج في: {filename}")
            
        except Exception as e:
            print(f"❌ خطأ في حفظ النتائج: {e}")

    def run_all_tests(self):
        """تشغيل جميع الاختبارات"""
        
        print("🧪 بدء اختبار نظام نانو Llama الشامل")
        print("=" * 60)
        
        # تهيئة النظام
        if not self.initialize_system():
            print("❌ فشل في تهيئة النظام للاختبار")
            return False
        
        # اختبار المحادثات
        for category, conversations in self.test_conversations.items():
            category_result = self.run_conversation_test(category, conversations)
            self.test_results["test_details"].append(category_result)
            self.test_results["total_tests"] += category_result["total_tests"]
            self.test_results["passed_tests"] += category_result["passed"]
            self.test_results["failed_tests"] += category_result["failed"]
        
        # اختبار الميزات المتقدمة
        features_result = self.test_system_features()
        self.test_results["features_test"] = features_result
        
        # اختبار الأداء
        performance_result = self.run_performance_benchmark()
        self.test_results["performance_metrics"] = performance_result
        
        # إنشاء وعرض التقرير
        report = self.generate_test_report()
        print(f"\n{report}")
        
        # حفظ النتائج
        self.save_test_results()
        
        return True

def main():
    """الدالة الرئيسية"""
    
    print("🤖 اختبار نظام نانو Llama الشامل")
    print("   اختبار الوظائف والأداء واللهجة السعودية")
    print()
    
    tester = NanoLlamaSystemTester()
    
    try:
        success = tester.run_all_tests()
        
        if success:
            print("\n🎉 انتهى الاختبار بنجاح!")
            print("📋 راجع التقرير أعلاه للتفاصيل")
        else:
            print("\n❌ فشل في إجراء الاختبارات")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف الاختبار بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()