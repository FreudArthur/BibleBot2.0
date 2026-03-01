import time

import streamlit as st

from main_freud import ask


st.set_page_config(page_title="Bible_Bot Thomas", page_icon="📖")


if "messages" not in st.session_state:
    st.session_state.messages = []


def add_message(role: str, content: str) -> None:
    st.session_state.messages.append({"role": role, "content": content})


def stream_response(text: str):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)


st.markdown(
    """
    <link href="https://fonts.googleapis.com/css2?family=Merriweather&family=Roboto&display=swap" rel="stylesheet">
    <style>
        html, body, [class*="css"] {
            font-family: 'Roboto', sans-serif;
        }

        .user-message {
            background-color: #D1E8FF;
            color: #000000;
            padding: 10px;
            border-radius: 10px;
            margin: 8px 0;
        }

        .bot-message {
            background-color: rgba(245, 245, 245, 0.85);
            color: #111111;
            padding: 10px;
            border-radius: 10px;
            margin: 8px 0;
        }

        @media (prefers-color-scheme: dark) {
            .user-message {
                background-color: #2D4F7C;
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
""",
    unsafe_allow_html=True,
)


st.title("📖 Thomas - Assistant Biblique")
st.write(
    "👋 Salut ! Je suis **Thomas**, ton assistant en théologie. Pose-moi toutes tes questions sur la Bible : versets, personnages, interprétations, et plus encore."
)


with st.sidebar:
    st.markdown("## ⚙️ Options")
    if st.button("🔄 Réinitialiser la conversation"):
        st.session_state.messages = []
        st.rerun()

if len(st.session_state.messages) != 0 :
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f'<div class="user-message">🙋‍♂️ <b>Moi :</b><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="bot-message">📖 <b>Thomas :</b><br>{msg["content"]}</div>',
                unsafe_allow_html=True,
            )


prompt = st.chat_input("✍️ Pose ta question ici : (Ex. Que dit la Bible sur la polygamie ?)")

if prompt:
    add_message("user", prompt)
    st.markdown(
        f'<div class="user-message">🙋‍♂️ <b>Moi :</b><br>{prompt}</div>',
        unsafe_allow_html=True,
    )

    with st.spinner("Thomas réfléchit..."):
        try :
            response = ask(prompt)
            streamed_response = st.write_stream(stream_response(response))
        except Exception as e:
            response = "Désolé une erreur s'est produite durant la génération du message. Veuillez réessayez"

    if streamed_response is None:
        streamed_response = response

    add_message("assistant", streamed_response)


st.markdown(
    '<div class="footer">Made with ❤️ by <a href="https://www.linkedin.com/in/freud-bokossa-4220ba321" target="_blank"> BOKOSSA Freud </a></div>',
    unsafe_allow_html=True,
)
