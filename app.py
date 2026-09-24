import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(
    page_title="فِلْمَتي AI - صانع الأفلام",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 فِلْمَتي AI")
st.markdown("### من فكرة صغيرة... إلى فيلم كامل")
st.markdown("اصنع قستك، شخصياتك، ومقابض مشاهدك وفيلمك بالذكاء الاصطناعي بكل سهولة.")

# الشريط الجانبي لإدخال المفتاح
st.sidebar.header("إعدادات الاتصال")
api_key = st.sidebar.text_input("أدخل مفتاح Google AI Studio API", type="password")

# المدخلات الرئيسية
st.markdown("### الخطوة 1 — فكرة الفيلم والمواصفات")
idea = st.text_area("اكتب فكرة فيلمك هنا...", placeholder="مثال: شاب يكتشف بئراً غامضاً في قرية جبلية يمنية، ويكتشف أن داخله سراً قديماً...")

genres = st.multiselect(
    "نوع الفيلم:",
    ["غموض", "مغامرة", "دراما", "أكشن", "رعب", "كوميدي", "خيال علمي"],
    default=["غموض", "دراما"]
)

duration = st.selectbox("مدة الفيلم المقدرة:", ["1 دقيقة", "3 دقائق", "5 دقائق", "10 دقائق"])
aspect_ratio = st.selectbox("نسبة الفيديو:", ["TikTok / Shorts — 9:16", "YouTube — 16:9"])

# زر التنفيذ
if st.button("🚀 ابدأ بناء الفيلم"):
    if not api_key:
        st.error("الرجاء إدخال مفتاح Google AI Studio API في الشريط الجانبي أولاً.")
    elif not idea:
        st.warning("الرجاء كتابة فكرة الفيلم أولاً.")
    else:
        try:
            # تهيئة مفتاح الاتصال بجيميني
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.6-flash")
            
            prompt = f"""
            أنت خبير ومحترف في صناعة الأفلام وكتابة السيناريو. قم بتحويل الفكرة التالية إلى خطة فيلم متكاملة ومفصلة:
            - فكرة الفيلم: {idea}
            - أنواع الفيلم: {', '.join(genres)}
            - المدة المقدرة: {duration}
            - نسبة الفيديو: {aspect_ratio}

            أعطني النتيجة باللغة العربية الفصحى وبشكل منسق واحترافي يتضمن:
            1. العنوان المقترح للفيلم
            2. الملخص الدرامي (Logline)
            3. الشخصيات الرئيسية مع وصف لكل شخصية
            4. تقسيم المشاهد (Scene Breakdown) مع الحوار والوصف البصري
            5. اقتراحات الهاشتاقات ووصف جذاب لنشر الفيديو على المنصات.
            """

            with st.spinner("جاري توليد السيناريو والقصة بالذكاء الاصطناعي... يرجى الانتظار ⏳"):
                response = model.generate_content(prompt)
                st.success("تم إنتاج الفيلم بنجاح! 🎉")
                st.markdown("---")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
