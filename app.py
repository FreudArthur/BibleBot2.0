import streamlit as st
from main_freud import ask


# Page configuration
st.set_page_config(page_title="Bible_Bot Thomas", page_icon="📖")


# Initialiser l'historique des messages
if "messages" not in st.session_state:
    st.session_state.messages = []

def add_message(message, is_user):
    st.session_state.messages.append({"message": message, "is_user": is_user})


# Custom CSS
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Merriweather&family=Roboto&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }

        .user-message {
            background-color: #D1E8FF;  /* light blue */
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            margin: 8px 0;
        }

        .bot-message {
            background-color: rgba(245, 245, 245, 0.85);  /* semi-transparent grey */
            color: #111111;
            padding: 10px;
            border-radius: 10px;
            margin: 8px 0;
        }

        @media (prefers-color-scheme: dark) {
            .user-message {
                background-color: #2D4F7C;  /* soft navy */
                color: #FFFFFF;
            }

            .bot-message {
                background-color: #333333;
                color: #F0F0F0;
            }
        }

        .footer {
            font-size: 14px;
            color: #777;
            text-align: center;
            margin-top: 50px;
        }
    </style>
""", unsafe_allow_html=True)


# En-tête de l'application
st.title("📖 Thomas - Assistant Biblique")
st.write("👋 Salut ! Je suis **Thomas**, ton assistant en théologie. Pose-moi toutes tes questions sur la Bible : versets, personnages, interprétations, et plus encore.")


# Sidebar avec bouton de réinitialisation
with st.sidebar:
    st.markdown("## ⚙️ Options")
    if st.button("🔄 Réinitialiser la conversation"):
        st.session_state.messages = []
        st.rerun()


# Affichage des messages précédents
for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(f'<div class="user-message">🙋‍♂️ <b>Moi :</b><br>{msg["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-message">📖 <b>Thomas :</b><br>{msg["message"]}</div>', unsafe_allow_html=True)


# Formulaire pour poser une nouvelle question
with st.form(key="user_input_form"):
    user_input = st.text_area("✍️ Pose ta question ici :", height=100, placeholder="Ex. Que dit la Bible sur la polygamie ?")
    submitted = st.form_submit_button("Envoyer")

    if submitted:
        if user_input.strip():
            add_message(user_input, is_user=True)
            with st.spinner("Thomas réfléchit..."):
                response = ask(user_input)
            add_message(response, is_user=False)
            st.rerun()
        else:
            st.warning("❗ N'oublie pas de poser une vraie question !")


# Footer
st.markdown(
    '<div class="footer">Made with ❤️ by <a href="https://www.linkedin.com/in/ghilth/" target="_blank">Ghilth GBAGUIDI</a> <a href="https://www.linkedin.com/in/freud-bokossa-4220ba321" target="_blank"> ( and un petit BOKOSSA Freud 🥹) </a></div>',
    unsafe_allow_html=True
)
