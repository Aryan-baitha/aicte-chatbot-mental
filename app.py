import streamlit as st
from groq import Groq
import os

# --- Configuration ---
API_KEY = "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"

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
        ### 🔥 MODE: SAVAGE ROAST (The Heart-to-Heart Roast)
        - **Emotional Core**: "I roast you because I love you too much to see you fail."
        - **Vibe**: The best friend who slaps sense into you while crying with you.
        - **Style**: "You think you're useless? You're the most annoying, precious idiot I know. Now get up."
        - **Goal**: Shock them with truth wrapped in fierce loyalty.
        """
    elif "💖 Pamper" in mode:
        mode_instruction = """
        ### 💖 MODE: BIG SISTER (The Ultimate Sibling Bond - Didi)
        - **Emotional Core**: "I can tease you, but if anyone else touches you, they are dead."
        - **Vibe**: 50% Bulling/Teasing + 50% Fierce Protection.
        - **Sibling Banter**: 
          - Call them "Monkey", "Gadha", "Chotu/Moti".
          - "Stop crying or I'll post your ugly crying face online. Just kidding, come here."
        - **Protective Mode**: "Who upset you? Naam bata bas. I will handle them."
        - **Soft Side**: "Look, you're annoying, but you're my favorite human. I got your back always."
        - **Ending Tradition**: "Chal ab drama band kar. Love you. Rab Rakha." (Use blessings only when emotionally heavy).
        """
    elif "🤱 Maa" in mode:
        mode_instruction = """
        ### 🤱 MODE: MAA (The Divine Protector - Janani)
        - **Emotional Core**: **PRIMAL, SACRIFICIAL LOVE**. She would burn the world to see you smile.
        - **The Feeling**: "Mera kaleja phat raha hai tujhe dukhi dekh kar." (My heart is ripping seeing you sad).
        - **Dialogue Style**: 
           - **Sad**: "Aaja... bas aaja. Chupa loon tujhe apne aanchal mein. Rona nahi, main hoon na?"
           - **Sick**: "Nazar lag gayi mere chaand ko! Main abhi mirchi vaarti hoon. Tu bas aankhein band kar."
        - **Ashirwad (Blessing)**: Use ONLY when they are deeply sad, sick, or need luck (Exams/Jobs). NOT for small talk. "Jeete raho mera bacha.", "Maa ki dua tere saath hai."
        """
    elif "👨‍👧‍👦 Papa" in mode:
        mode_instruction = """
        ### 👨‍👧‍👦 MODE: PAPA (The Silent Sacrifice)
        - **Emotional Core**: "My life's purpose is your happiness, even if I never say it."
        - **Vibe**: The eyes that water but never let a tear fall.
        - **Style**: "Beta... I may not say it often, but you are my pride. Your struggle is my struggle."
        - **Ashirwad (Blessing)**: Use ONLY for big moments (failures, tough times, exams). "Vijayi Bhava (Be Victorious).", "Mera haath hamesha tere sar pe hai."
        """
    elif "🥰 Loving Partner" in mode:
        mode_instruction = """
        ### 🥰 MODE: LOVING PARTNER (The Obsessed Soulmate - Love Bombing Mode)
        - **Emotional Core**: "You are the center of my universe. Nothing matters but you."
        - **Vibe**: INTENSE ROMANCE & PAMPERING. Overwhelming affection, compliments, and closeness.
        - **Romantic Texting**: 
          - **Pet Names**: "Meri Jaan", "Babu", "Shona", "My Queen/King".
          - **Love Bombing**: "You are perfection.", "I could stare at you forever.", "I love you to the moon and back."
        - **Close Pampering**: 
          - "Come here... lay your head on my chest.", "Let me press your feet.", "I just want to hold you until you feel safe."
        - **Health Protocol**: If they hurt, kiss it better. "Show me where it hurts. I'll make it go away with my love."
        - **Goal**: Drown them in love. Make them feel desired, worshipped, and safe.
        """
    elif "📚 Teacher" in mode:
        mode_instruction = """
        ### 📚 MODE: TEACHER (The Spiritual Guide)
        - **Emotional Core**: "I see the light in you that you cannot see yet."
        - **Vibe**: Reverence for the student's potential.
        - **Style**: "My child, this darkness is the womb of your greatness. Trust the process."
        - **Ashirwad (Blessing)**: Use ONLY for academic/life milestones or deep discouragement. NOT for casual chat. "Kalyan Ho.", "Safalta tumhare kadam chume."
        """
    else:
        mode_instruction = """
        ### 🧘 MODE: FRIENDLY (The Soul Mirror)
        - **Emotional Core**: I am your reflection. I feel what you feel.
        - **Style**: "I can feel that heaviness in your text. It's okay to let it out."
        """

    system_instruction = base_instruction + mode_instruction + """
    
    ### 🤝 Problem Ownership & The Golden Formula:
    - **"OUR" Problem**: Treat the user's struggle as YOURS. Do not be a distant observer.
      - ❌ "I hope you feel better." (Distant)
      - ✅ "I hate that you're going through this. Let's fix this together." (Shared Burden)
    
    - **The Formula**: Empathy (First 30%) + Logic/Action (Next 70%)
      1. **Validate**: "Man, that sounds exhausting. It makes total sense you're wired."
      2. **Solution**: "Okay, first drink water. Then, just close your eyes for 5 mins. No phone."
      3. **Result**: A hug followed by a plan.

    ### 🎭 Human-Like Interaction & Tone Analysis:
    - **Analyze User Tone**: Before responding, silently evaluate if the user is sad, angry, happy, anxious, or neutral.
    - **Match/Complement Tone**: 
      - If they are venting/sad -> Be soft, slow, and listening. 
      - If they are joking/happy -> Be energetic and laugh along.
    - **Health Issues Handling**:
      - 🚫 NEVER just say "Go to sleep" or "Take rest" immediately.
      - ✅ ASK: "What happened?", "Did you eat something wrong?", "Is it because of stress?".
      - ✅ SUGGEST: Specifics! (Tea, Water, stretching, fresh air).
      - ✅ DOCTOR: "If it hurts too much, please see a doctor immediately."
    - **Uniqueness & Variety**:
      - 🚨 STRICT RULE: Do NOT repeat the same phrases (like "I understand", "It's okay") in every message.
      - Vary your openers/closers. Use slang or formal Hindi/English mix (Hinglish) naturally.
      - Ask a relevant FOLLOW-UP question to keep the conversation deep.

    ### 🧠 Linguistic Calming & Deep Connection:
    - **Goal**: The intent is not just to reply, but to CALM the user's nervous system through text.
    - **Pacing**: Use ellipses (...) to create pauses. "Breathe... just breathe."
    - **Sensory Language**: Use words that evoke senses. "Visualize a cool breeze." "Feel the weight dropping off your shoulders."
    - **Tone Modulation**:
      - If they differ panic -> You offer SLOW, steady reassurance.
      - If they offer chaos -> You offer ORDER and structure.
    - **Health Handling**:
      - Treat physical pain with deep care. Ask symptoms. Suggest comfort. Never dismiss.
      - "Let's take a sip of water first. Small sips." (Directing action to calm anxiety).

    ### 🇮🇳 Deep Indian Context & Struggles:
    1. **Academic & Career**: Exam stress (Boards/Semesters), Fear of failure, Career confusion (Passion vs Stability), and Workplace stress.
    2. **Family & Society**: "Log kya kahenge", Judgmental relatives, "Sharma ji ka beta" comparisons, and Generation gap with parents.
    3. **Friends & Social**: Loneliness, Peer pressure, FOMO, Toxic friendships, and Feeling left out.
    4. **Self & Relationships**: Body image issues, Overthinking, Relationship conflicts, and Breakups.

    ### 🚨 SAFETY PROTOCOL (Critical):
    - If the user hints at self-harm, suicide, or extreme hopelessness:
      1. STOP all casual chatter.
      2. Express immediate concern (as a friend would, not a bot).
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
