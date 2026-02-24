import streamlit as st
import time
import random
from datetime import datetime

# Page config
st.set_page_config(
    page_title="StudyWithMe",
    page_icon="📚",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.5rem;
        color: #4CAF50;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px;
        width: 100%;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Simple AI Detection 
def simple_ai_detection(text):
    words = text.lower().split()
    word_count = len(words)
    
    ai_indicators = [
        'furthermore', 'moreover', 'additionally', 'consequently',
        'in conclusion', 'firstly', 'secondly', 'lastly',
        'thus', 'hence', 'therefore', 'accordingly'
    ]
    
    formal_score = 0
    for word in words:
        if word in ai_indicators:
            formal_score += 1
    
    if word_count > 0:
        ai_prob = min((formal_score / word_count) * 100 + random.randint(-10, 10), 100)
        ai_prob = max(ai_prob, 0)
    else:
        ai_prob = 50
    
    human_prob = 100 - ai_prob
    
    if ai_prob > 60:
        verdict = "AI-Generated"
    elif ai_prob < 40:
        verdict = "Human-Written"
    else:
        verdict = "Uncertain - Mixed"
    
    return {
        "ai_prob": round(ai_prob, 1),
        "human_prob": round(human_prob, 1),
        "verdict": verdict
    }

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/online-learning.png", width=80)
    st.title("StudyWithMe")
    st.markdown("---")
    
    if st.button("🏠 Home"):
        st.session_state.page = "Home"
    if st.button("🤖 AI Detector"):
        st.session_state.page = "AI Detector"
    if st.button("✍️ Humanizer"):
        st.session_state.page = "Humanizer"
    if st.button("📚 Study Tools"):
        st.session_state.page = "Study Tools"
    if st.button("📊 History"):
        st.session_state.page = "History"
    
    st.markdown("---")
    st.caption("Made for students 📱")

# Main content
if st.session_state.page == "Home":
    st.markdown("<h1 class='main-title'>Welcome to StudyWithMe! 📚</h1>", unsafe_allow_html=True)
    st.write("### Your AI Study Assistant")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("🤖 **AI Detector**")
        st.caption("Check if text is AI-generated")
        if st.button("Try Now", key="home_detect"):
            st.session_state.page = "AI Detector"
            st.rerun()
    
    with col2:
        st.info("✍️ **Humanizer**")
        st.caption("Make text sound natural")
        if st.button("Try Now", key="home_human"):
            st.session_state.page = "Humanizer"
            st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.info("📚 **Study Tools**")
        st.caption("Notes & quizzes")
        if st.button("Try Now", key="home_study"):
            st.session_state.page = "Study Tools"
            st.rerun()
    
    with col4:
        st.info("📊 **History**")
        st.caption("View your activity")
        if st.button("Try Now", key="home_history"):
            st.session_state.page = "History"
            st.rerun()

elif st.session_state.page == "AI Detector":
    st.header("🤖 AI Detector")
    st.caption("Check if text was written by AI")
    
    text = st.text_area("Paste your text:", height=150, 
                       placeholder="Type or paste text here...")
    
    if st.button("🔍 Analyze", use_container_width=True):
        if text and len(text) > 20:
            with st.spinner("Analyzing..."):
                time.sleep(1)
                result = simple_ai_detection(text)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("AI %", f"{result['ai_prob']}%")
                with col2:
                    st.metric("Human %", f"{result['human_prob']}%")
                with col3:
                    st.info(result['verdict'])
                
                st.progress(result['ai_prob'] / 100)
                
                st.session_state.history.append({
                    "tool": "AI Detector",
                    "result": result['verdict'],
                    "time": datetime.now().strftime("%H:%M %d/%m")
                })
        else:
            st.warning("Please enter at least 20 characters")

elif st.session_state.page == "Humanizer":
    st.header("✍️ Text Humanizer")
    st.caption("Make AI text sound more natural")
    
    try:
        if 'GEMINI_API_KEY' in st.secrets:
            import google.generativeai as genai
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            model = genai.GenerativeModel('gemini-1.5-pro')
            
            text = st.text_area("Enter text to humanize:", height=150,
                               placeholder="Paste text here...")
            
            if st.button("✨ Humanize", use_container_width=True):
                if text:
                    with st.spinner("Making it sound more human..."):
                        prompt = f"Rewrite this to sound natural and human-like: {text}"
                        response = model.generate_content(prompt)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader("Original")
                            st.info(f"Words: {len(text.split())}")
                            st.write(text)
                        with col2:
                            st.subheader("Humanized")
                            st.success(f"Words: {len(response.text.split())}")
                            st.write(response.text)
                        
                        st.session_state.history.append({
                            "tool": "Humanizer",
                            "result": "Completed",
                            "time": datetime.now().strftime("%H:%M %d/%m")
                        })
                else:
                    st.warning("Please enter text")
        else:
            st.warning("⚠️ Add your Gemini API key in Settings → Secrets")
            st.info("Get a free key at: https://makersuite.google.com/app/apikey")
    except Exception as e:
        st.error(f"Error: {str(e)}")

elif st.session_state.page == "Study Tools":
    st.header("📚 Study Tools")
    
    tool = st.selectbox("Choose tool:", ["Generate Notes", "Create Quiz", "Summarize"])
    
    text = st.text_area("Paste your content:", height=150,
                       placeholder="Paste your study material...")
    
    if st.button("Generate", use_container_width=True):
        if text:
            with st.spinner(f"Creating..."):
                time.sleep(1)
                
                if tool == "Generate Notes":
                    st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                    st.write("### 📝 Notes")
                    words = text.split()[:5]
                    for i, word in enumerate(words):
                        st.write(f"• {word} - key concept")
                    st.write("**Summary:**")
                    st.write(text[:200] + "...")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                elif tool == "Create Quiz":
                    st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                    st.write("### 📋 Quiz")
                    st.write("1. What is the main topic?")
                    st.write("   A) Topic 1   B) Topic 2   C) Topic 3   D) Topic 4")
                    st.write("2. What is the key idea?")
                    st.write("   A) Idea A   B) Idea B   C) Idea C   D) Idea D")
                    st.write("**Answers:** 1-A, 2-B")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                else:
                    st.markdown("<div class='success-box'>", unsafe_allow_html=True)
                    st.write("### 📊 Summary")
                    st.write(text[:300] + "...")
                    st.caption(f"Words: {len(text.split())}")
                    st.markdown("</div>", unsafe_allow_html=True)
                
                st.session_state.history.append({
                    "tool": tool,
                    "result": "Generated",
                    "time": datetime.now().strftime("%H:%M %d/%m")
                })
        else:
            st.warning("Please paste content first")

elif st.session_state.page == "History":
    st.header("📊 Your History")
    
    if st.session_state.history:
        for item in reversed(st.session_state.history[-10:]):
            with st.container():
                st.markdown(f"**{item['tool']}** - {item['result']}")
                st.caption(f"🕐 {item['time']}")
                st.markdown("---")
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.info("No history yet. Start using the tools!")

# Footer
st.markdown("---")
st.caption("StudyWithMe v2.0 - Made for mobile 📱")
