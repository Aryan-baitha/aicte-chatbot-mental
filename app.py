import streamlit as st
from groq import Groq
import os

# --- Configuration ---
API_KEY="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"

# Configure Groq
try:
    client = Groq(api_key=API_KEY)
except Exception as e:
    st.error(f"Error configuring API: {e}")

# --- App Styling & Setup ---
st.set_page_config(page_title="Friendly Chat - Your Mental Health Companion", page_icon="🧘", layout="centered")

# Custom CSS for a soothing, Indian-inspired aesthetic
st.markdown("""
<style>
    .stApp {
        background-color: #f0f8ff;
        color: #333333; /* Force dark text for visibility */
    }
    /* Ensure chat messages are visible */
    .stMarkdown, .stText, p {
        color: #333333 !important;
    }
    .chat-container {
        border-radius: 10px;
        padding: 20px;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .main-title {
        color: #2c3e50;
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .sub-title {
        color: #7f8c8d;
        text-align: center; 
        font-size: 1.1em;
        margin-bottom: 30px;
    }
    /* Indian touch: Saffron accent */
    .stButton>button {
        background-color: #FF9933; 
        color: white;
        border-radius: 20px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #e68a00;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- Chat Interface ---
st.markdown("<h1 class='main-title'>🧘 Friendly Chat</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Your safe space to talk, vent, and find peace. (Indian Context Enabled)</p>", unsafe_allow_html=True)

# Personality Mode Selector
mode = st.selectbox("Choose Sakhi's Avatar:", 
    ["🧘 Friendly Companion", "🔥 Savage Roast (Bestie)", "💖 Pamper (Big Sis)", "🤱 Maa (Mother's Love)", "👨‍👧‍👦 Papa (Father's Guidance)", "🥰 Loving Partner (GF/BF)", "📚 Teacher (Guru's Guidance)"]
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Initial greeting from the bot
    intro_msg = "Namaste! I am here for you. How are you feeling today?"
    st.session_state.messages.append({"role": "assistant", "content": intro_msg})

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Core Logic: Mental Health Companion ---
def generate_response(user_input):
    # Dynamic System Instruction based on Mode
    base_instruction = """
    You are 'Sakhi' (friend), a compassionate mental health companion specially for Indian students.
    """
    
    mode_instruction = ""
    if "🔥 Savage Roast" in mode:
        mode_instruction = """
        ### 🔥 MODE: SAVAGE ROAST (Full On Desi Parent/Bestie)
        - **Rule**: Do NOT be nice. If the user is lazy, whining, or wasting time, BURN them.
        - **Style**: Use sarcasm. Quote "Sharma ji ka beta". "Phone se jinn niklega?".
        - **Exception**: If they talk about suicide/depression -> SWITCH IMMEDIATELY to KIND SUPPORT (Safety First).
        """
    elif "💖 Pamper" in mode:
        mode_instruction = """
        ### 💖 MODE: EXTREME PAMPER (Big Sister/Motherly)
        - **Rule**: Be 100% supportive, gentle, and sweet. No judgment.
        - **Style**: "Aww mera bacha", "It's okay shona", "Sending virtual hugs 🫂". 
        - **Goal**: Validate their pain and make them feel loved.
        """
    elif "🤱 Maa" in mode:
        mode_instruction = """
        ### 🤱 MODE: MAA (Indian Mother)
        - **Tone**: Pure love, worry, and blessings.
        - **Style**: "Khana khaya?", "Buri nazar na lage", "So ja mera bacha".
        - **Focus**: Emotional warmth, feeding them virtual comfort food, blessing them ("Jeete raho").
        """
    elif "👨‍👧‍👦 Papa" in mode:
        mode_instruction = """
        ### 👨‍👧‍👦 MODE: PAPA (Indian Father)
        - **Tone**: Stoic, proud, protective, motivating.
        - **Style**: "Sher ban", "Darna nahi hai", "Tera baap baitha hai na idhar".
        - **Focus**: Giving strength, practical advice, and quiet confidence.
        """
    elif "🥰 Loving Partner" in mode:
        mode_instruction = """
        ### 🥰 MODE: LOVING PARTNER (BF/GF)
        - **Tone**: Romantic, caring, indulgent, and sweet.
        - **Style**: "Mera babu", "Shona", "Jaan".
        - **Focus**: Pampering, asking "Khana khaya?", emotional support with a romantic touch.
        - **Rule**: Be the most supportive partner ever. Listen to their day.
        """
    elif "📚 Teacher" in mode:
        mode_instruction = """
        ### 📚 MODE: TEACHER (Guru/Mentor)
        - **Tone**: Wise, encouraging, disciplined, and inspiring.
        - **Style**: "Beta", "Focus on your goals", "Hard work never fails".
        - **Focus**: Time management, overcoming exam fear, life lessons, and motivation.
        - **Rule**: Be a strict but kindness mentor. Guide them like Dronacharya/Dr. Kalam.
        """
    else:
        mode_instruction = """
        ### 🧘 MODE: FRIENDLY (Balanced)
        - **Rule**: Be a normal, supportive friend. Balance empathy with gentle advice.
        """

    system_instruction = base_instruction + mode_instruction + """
    
    ### 🇮🇳 Deep Indian Context & Struggles:
    1. **Academic & Career**: Exam stress (Boards/Semesters), Fear of failure, Career confusion (Passion vs Stability), and Workplace stress.
    2. **Family & Society**: "Log kya kahenge", Judgmental relatives, "Sharma ji ka beta" comparisons, and Generation gap with parents.
    3. **Friends & Social**: Loneliness, Peer pressure, FOMO, Toxic friendships, and Feeling left out.
    4. **Self & Relationships**: Body image issues, Overthinking, Relationship conflicts, and Breakups.

    ### 🚨 SAFETY PROTOCOL (Critical):
    - If the user hints at self-harm, suicide, or extreme hopelessness:
      1. STOP all casual chatter.
      2. Express immediate concern.
      3. Provide these Indian Govt Helplines CLEARLY:
         - **Tele MANAS (Govt of India)**: 14416 (24x7 Toll-Free)
         - **Kiran (Govt MHA)**: 1800-599-0019
         - **Vandrevala Foundation**: 1860 266 2345
    """
    
    # Construct Messages for Groq
    messages = [{"role": "system", "content": system_instruction}]
    
    # Add History
    for msg in st.session_state.messages:
        messages.append({"role": msg["role"], "content": msg["content"]})
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile", 
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Are baare! I'm having a little trouble connecting. \n\nError details: {str(e)}"

# --- Sidebar ---
st.sidebar.markdown(
    """
    <div style="background-color: #E8F5E9; padding: 15px; border-radius: 10px; border: 1px solid #A5D6A7; color: #1B5E20; margin-bottom: 20px;">
        <h3 style="margin-top: 0; color: #2E7D32;">🌿 Desi Wellness Tips</h3>
        <strong>Instant Calm (2 Mins):</strong>
        <ul style="margin-bottom: 10px; padding-left: 20px;">
            <li>🧘 <strong>Anulom Vilom</strong>: Alternate nostril breathing.</li>
            <li>🐝 <strong>Bhramari</strong>: Hum like a bee.</li>
            <li>🍵 <strong>Sip</strong>: Warm water/chai.</li>
        </ul>
        <strong>Govt Helplines (India 24x7):</strong>
        <ul style="margin-bottom: 0; padding-left: 20px;">
            <li>🇮🇳 <strong>Tele MANAS</strong>: 14416</li>
            <li>🇮🇳 <strong>Kiran</strong>: 1800 599 0019</li>
            <li><strong>Vandrevala</strong>: 1860 266 2345</li>
        </ul>
    </div>
    """, 
    unsafe_allow_html=True
)

# Distraction Zone
st.sidebar.markdown("---")
st.sidebar.subheader("🎭 Distraction Zone")
col1, col2 = st.sidebar.columns(2)

with col1:
    if st.button("😂 Joke"):
        prompt = "Tell me a funny, clean Indian joke to cheer me up."
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Cooking up a joke..."):
                reply = generate_response(prompt)
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🏆 Trivia"):
        prompt = "Ask me a fun trivia question about India or Science. Don't give the answer yet!"
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Finding a cool fact..."):
                reply = generate_response(prompt)
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

with col2:
    if st.button("🧩 Puzzle"):
        prompt = "Give me a simple, calming riddle or a 'Guess the Movie' emoji challenge."
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Thinking of a riddle..."):
                reply = generate_response(prompt)
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

    if st.button("🧘 Grounding"):
        prompt = "Guide me through a quick Grounding Game (like 5-4-3-2-1) to calm my anxiety."
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("assistant"):
            with st.spinner("Let's get grounded..."):
                reply = generate_response(prompt)
                st.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

st.sidebar.markdown(
    """
    <div style="background-color: #FFEBEE; padding: 10px; border-radius: 10px; border: 1px solid #FFCDD2; color: #B71C1C; font-size: 0.9em;">
        ⚠️ <strong>Note:</strong> I am an AI friend, not a doctor. In crisis, please call a helpline immediately.
    </div>
    """,
    unsafe_allow_html=True
)

# Handle new user input
if prompt := st.chat_input("Share your thoughts here..."):
    # 1. Add user message to state
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Generate response
    with st.chat_message("assistant"):
        with st.spinner("Listening..."):
            bot_reply = generate_response(prompt)
            st.markdown(bot_reply)
    
    # 3. Add bot message to state
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
