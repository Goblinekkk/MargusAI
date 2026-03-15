import streamlit as st
from openai import OpenAI
import os

# 1. Nastavení vzhledu
st.set_page_config(page_title="Margus AI", page_icon="🤖")
st.title("🤖 Margus AI")
st.markdown("Vítejte v rozhraní Margus AI poháněném NVIDIA technologií.")

# 2. Načtení klíče (bude schovaný v nastavení Streamlitu)
api_key = os.getenv("NVIDIA_API_KEY")

# 3. Propojení s NVIDIA API
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key
)

# 4. Paměť chatu
if "messages" not in st.session_state:
    st.session_state.messages = []

# Zobrazení zpráv
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Samotné chatování
if prompt := st.chat_input("Napiš Margus AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=st.session_state.messages,
            temperature=0.5
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
