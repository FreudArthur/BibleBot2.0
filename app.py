import time
import streamlit as st
from main_freud import ask

# Configuration page
st.set_page_config(
    page_title="Thomas - Assistant Biblique",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

def add_message(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})

def stream_response(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)

# CSS Amélioré avec animations
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        * {
            margin: 0;
            padding: 0;
        }

        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #FFFFFF 0%, #E8F4F8 50%, #FFF9E6 100%);
        }

        .main {
            background: linear-gradient(135deg, #FFFFFF 0%, #E8F4F8 50%, #FFF9E6 100%);
        }

        /* Header Animation */
        .header-container {
            background: linear-gradient(135deg, #0066CC 0%, #0099FF 50%, #FFD700 100%);
            padding: 30px 20px;
            border-radius: 15px;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 8px 20px rgba(0, 102, 204, 0.15);
            animation: slideDown 0.6s ease-out;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .header-container h1 {
            color: white;
            font-size: 48px;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.02); }
        }

        .header-container p {
            color: rgba(255, 255, 255, 0.95);
            font-size: 16px;
            font-weight: 300;
            line-height: 1.6;
        }

        /* Messages Container */
        .messages-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }

        /* User Message */
        .user-message {
            background: linear-gradient(135deg, #0066CC 0%, #0099FF 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 15px;
            margin: 15px 0;
            text-align: right;
            animation: slideInRight 0.4s ease-out;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.2);
            border-left: 5px solid #FFD700;
        }

        @keyframes slideInRight {
            from {
                opacity: 0;
                transform: translateX(50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .user-message b {
            font-weight: 600;
        }

        /* Bot Message */
        .bot-message {
            background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%);
            color: #1a1a1a;
            padding: 15px 20px;
            border-radius: 15px;
            margin: 15px 0;
            text-align: left;
            animation: slideInLeft 0.4s ease-out;
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.1);
            border-left: 5px solid #FFD700;
            line-height: 1.6;
        }

        @keyframes slideInLeft {
            from {
                opacity: 0;
                transform: translateX(-50px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }

        .bot-message b {
            color: #0066CC;
            font-weight: 600;
        }

        /* Input Section */
        .input-section {
            max-width: 900px;
            margin: 30px auto;
            padding: 20px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0, 102, 204, 0.1);
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 40px 20px;
            animation: fadeIn 0.6s ease-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        .empty-state h2 {
            color: #0066CC;
            font-size: 32px;
            margin-bottom: 15px;
        }

        .empty-state p {
            color: #666;
            font-size: 16px;
            line-height: 1.6;
            margin-bottom: 20px;
        }

        /* Suggestions */
        .suggestions {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }

        .suggestion-btn {
            background: linear-gradient(135deg, #0099FF 0%, #0066CC 100%);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            border: none;
            cursor: pointer;
            font-size: 12px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 8px rgba(0, 102, 204, 0.2);
        }

        .suggestion-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 102, 204, 0.4);
        }

        /* Sidebar */
        .sidebar-btn {
            background: linear-gradient(135deg, #FFD700 0%, #FFC700 100%);
            color: #0066CC;
            padding: 12px 20px;
            border-radius: 8px;
            border: 2px solid #0066CC;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            width: 100%;
            margin: 10px 0;
        }

        .sidebar-btn:hover {
            background: linear-gradient(135deg, #FFC700 0%, #FFB700 100%);
            transform: scale(1.05);
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            padding: 30px 20px;
            color: #0066CC;
            font-size: 13px;
            animation: fadeIn 1s ease-out;
        }

        .footer a {
            color: #0099FF;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
        }

        .footer a:hover {
            color: #FFD700;
        }



        /* Responsive */
        @media (max-width: 768px) {
            .header-container h1 {
                font-size: 32px;
            }
            
            .messages-container {
                padding: 10px;
            }
        }
    </style>
""", unsafe_allow_html=True)

# Header with animation
st.markdown("""
    <div class="header-container">
        <h1>📖 Thomas</h1>
        <p>✨ Ton Assistant Biblique Intelligent ✨</p>
        <p style="margin-top: 10px; font-size: 14px;">Explore la sagesse biblique en posant tes questions sur les versets, les personnages, et les enseignements</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Options")
    
    if st.button("🔄 Réinitialiser la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📚 À propos")
    st.write("""
    **Thomas** est un assistant biblique alimenté par l'IA.
    
    Il te aide à :
    - 🔍 Trouver des versets
    - 👥 Découvrir les personnages bibliques
    - 💭 Comprendre les concepts théologiques
    - 📖 Explorer le contexte historique
    """)

# Messages display
if len(st.session_state.messages) > 0:
    st.markdown('<div class="messages-container">', unsafe_allow_html=True)
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-message">🙋‍♂️ <b>Toi :</b><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bot-message">📖 <b>Thomas :</b><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # Empty state
    st.markdown("""
        <div class="empty-state">
            <h2>👋 Bienvenue !</h2>
            <p>Je suis <b>Thomas</b>, ton compagnon pour explorer la Bible.</p>
            <p>Pose-moi une question et je t'aiderai à découvrir les réponses bibliques.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Suggestions
    st.markdown('<div class="suggestions">', unsafe_allow_html=True)
    suggestions = [
        "Qui est David ?",
        "Que dit la Bible sur l'amour ?",
        "Explique Jean 3:16",
        "Raconte l'histoire de Ruth"
    ]
    for suggestion in suggestions:
        st.markdown(f'<span class="suggestion-btn">{suggestion}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="input-section">', unsafe_allow_html=True)
prompt = st.chat_input("✨ Pose ta question biblique ici... (Ex: Que dit la Bible sur la miséricorde ?)")
st.markdown('</div>', unsafe_allow_html=True)

if prompt:
    add_message("user", prompt)
    st.markdown(
        f'<div class="user-message">🙋‍♂️ <b>Toi :</b><br>{prompt}</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("⏳ Thomas médite ta question..."):
        try:
            response = ask(prompt)
            streamed_response = st.write_stream(stream_response(response))
        except Exception as e:
            response = "❌ Désolé, une erreur s'est produite. Veuillez réessayer."
            streamed_response = response

    if streamed_response is None:
        streamed_response = response

    add_message("assistant", streamed_response)
    st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <p>Made with ❤️ by <a href="https://www.linkedin.com/in/freud-bokossa-4220ba321" target="_blank">BOKOSSA Freud</a></p>
        <p style="margin-top: 10px; font-size: 12px;">🙏 <i>"Cherchez et vous trouverez" - Matthieu 7:7</i></p>
    </div>
""", unsafe_allow_html=True)
