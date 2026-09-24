import streamlit as st
from google import genai

st.set_page_config(
    page_title="فِلْمَتي AI — صانع الأفلام",
    page_icon="🎬",
    layout="centered"
)

st.markdown("""
<style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stTextInput, .stTextArea, .stSelectbox, .stMultiSelect {
        direction: rtl;
    }
</style>
""", unsafe_allow_html=True)

st.title("فِلْمَتي AI 🎬")
st.markdown("### **من فكرة صغيرة... إلى فيلم كامل 🎬**")
st.write("اصنع قصتك، شخصياتك، ومقابض مشاهدك وفيلمك بالذكاء الاصطناعي بكل سهولة.")

st.sidebar.title("⚙️ الإعدادات")
api_key = st.sidebar.text_input("مفتاح Google AI Studio API Key:", type="password")
st.sidebar.markdown("---")
st.sidebar.info("هذه النسخة التجريبية الأولى (MVP) تركز على توليد القصة، الشخصيات، والمشاهد مع برومبتات جاهزة.")

st.divider()

st.subheader("الخطوة 1 — فكرة الفيلم والمواصفات")

idea = st.text_area(
    "✍️ اكتب فكرة فيلمك هنا...",
    placeholder="مثال: شاب يكتشف بئراً غامضاً في قرية جبلية يمنية، ويكتشف أن داخله سراً قديماً..."
)

col1, col2 = st.columns(2)
with col1:
    genres = st.multiselect(
        "نوع الفيلم:",
        ["مغامرة", "غموض", "رعب", "أكشن", "دراما", "رومانسي", "خيال", "كوميدي"],
        default=["غموض", "مغامرة"]
    )
with col2:
    duration = st.selectbox(
        "مدة الفيلم المقدرة:",
        ["1 دقيقة", "5 دقائق", "10 دقائق", "30 دقيقة", "60 دقيقة", "90 دقيقة"]
    )

aspect_ratio = st.selectbox(
    "نسبة الفيديو:",
    ["16:9 — YouTube / فيلم", "9:16 — TikTok / Shorts", "1:1 — Instagram"]
)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("🚀 ابدأ بناء الفيلم", type="primary", use_container_width=True):
    if not api_key:
        st.error("الرجاء إدخال مفتاح Google AI Studio API في الشريط الجانبي أولاً.")
    elif not idea.strip():
        st.warning("الرجاء كتابة فكرة الفيلم لنتمكن من البدء.")
    else:
        client = genai.Client(api_key=api_key)
        
        with st.spinner("🧠 غرفة الذكاء الاصطناعي تبدع الآن: يتم بناء القصة، الشخصيات، وتقسيم المشاهد..."):
            
            prompt_text = f"""
            أنت مخرج سينمائي وكاتب سيناريو محترف وخبير في الذكاء الاصطناعي التوليدي.
            بناءً على فكرة الفيلم التالية، قم بإنشاء مشروع متكامل باللغة العربية (مع توفير برومبتات بالإنجليزية للصور والفيديوهات):
            
            - الفكرة: {idea}
            - الأنواع: {', '.join(genres)}
            - المدة المستهدفة: {duration}
            - نسبة العرض: {aspect_ratio}

            قم بتنظيم الإجابة في الأقسام التالية بوضوح وبشكل منسق:
            
            ### 📖 1. ملخص القصة والحبكة
            (اكتب قصة شيقة ومفصلة مستوحاة من الفكرة).
            
            ### 👤 2. الشخصيات الرئيسية والمرجع البصري
            (اذكر اسم الشخصية، العمر، الوصف والملابس بتفصيل دقيق لضمان ثبات المظهر بصرياً).
            
            ### 🎬 3. مشاهد الفيلم الأولى (المشاهد الرئيسية)
            (قسّم بداية الفيلم إلى 3 إلى 5 مشاهد رئيسية، ولكل مشهد اكتب:
            - رقم المشهد والمكان/الوقت (مثلاً: المشهد 01 — القرية — الليل)
            - الوصف البصري الأحداث
            - الحوار بين الشخصيات
            - Prompt الصورة (باللغة الإنجليزية لكي يتم نسخه لأدوات توليد الصور)
            - Prompt الفيديو / الحركة (باللغة الإنجليزية))
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash
",
                    contents=prompt_text
                )
                
                st.success("🎉 تم إنشاء مشروع الفيلم بنجاح في غرفة الذكاء الاصطناعي!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
