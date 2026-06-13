import streamlit as st
import requests

st.set_page_config(page_title="Legal PDF AI Assistant", page_icon="⚖️", layout="centered")

st.title("⚖️ Legal PDF AI Assistant")
st.write("Ask a question.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Ask a question about the document..."):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing document database context..."):
            try:
                backend_url = "http://127.0.0.1:8000/chat"
                payload = {"question": user_input, "temperature": 0.2}
                
                response = requests.post(backend_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    report = data.get("agent_final_report", {})
                    
                    final_answer = f"**Summary:** {report.get('summary')}\n\n{report.get('detailed_answer')}"
                    
                    st.markdown(final_answer)
                    st.session_state.messages.append({"role": "assistant", "content": final_answer})
                else:
                    st.error(f"Backend returned an operational error: {response.status_code}")
                    
            except requests.exceptions.ConnectionError:
                st.error("CRITICAL: Could not connect to the FastAPI backend server. Ensure uvicorn main:app is running in another terminal window!")