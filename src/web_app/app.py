import streamlit as st

from src.agents.agent import create_session, process_message

st.set_page_config(
    page_title="SmartDesk AI Demo",
    page_icon="💼",
    layout="centered",
)

if "started" not in st.session_state:
    st.session_state.started = False

if "session" not in st.session_state:
    st.session_state.session = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "demo_ended" not in st.session_state:
    st.session_state.demo_ended = False

st.title("SmartDesk AI")
st.subheader("IT and HR Support Assistant")

st.markdown(
    "Ask about password reset, VPN, leave policy, reimbursement, "
    "or check support ticket status."
)

with st.sidebar:
    st.markdown("### Demo Controls")
    confirm_shutdown = st.checkbox("I understand this will end the current demo session")
    if st.button("Shutdown Demo", type="secondary", use_container_width=True):
        if confirm_shutdown:
            st.session_state.started = False
            st.session_state.session = None
            st.session_state.messages = []
            st.session_state.demo_ended = True
            st.rerun()
        st.info("Please tick the confirmation box before shutting down.")

if st.session_state.demo_ended:
    st.success("Demo session ended successfully.")
    st.info("No server disconnect occurred. Click Start SmartDesk to begin a new session.")

if not st.session_state.started:
    if st.button("Start SmartDesk", type="primary", use_container_width=True):
        st.session_state.started = True
        st.session_state.demo_ended = False
        st.session_state.session = create_session()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello! I can help with IT and HR questions. What can I help you with today?",
            }
        ]
        st.rerun()
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("Type your question...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    try:
        reply = process_message(user_input, st.session_state.session)
    except Exception as error:
        reply = f"I hit an error while processing your request: {error}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
