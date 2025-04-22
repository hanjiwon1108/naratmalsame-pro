import streamlit as st
import requests
import time
import json
import os  

API_ENDPOINT = st.secrets["API_ENDPOINT"]
API_KEY = st.secrets["API_KEY"]


st.write("Streamlit loves LLMs! 🤖 [Build your own chat app](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps) in minutes, then make it powerful by adding images, dataframes, or even input widgets to the chat.")

st.caption(
  "Note that this demo app is now connected to an LLM API!")

# Initialize chat history and conversation_id
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Let's start chatting! 👇"}
    ]
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = "577d050b-1a40-45f3-9705-82218bd9b775"  # 초기 conversation_id 설정

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call the API to get assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            response = requests.post(
                API_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": {},
                    "query": prompt,
                    "response_mode": "streaming",
                    "conversation_id": st.session_state.conversation_id,  # 유지된 conversation_id 사용
                    "user": "abc-123"
                },
                stream=True
            )

            # Process streaming response
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:
                    if chunk.startswith("data: "):
                        chunk = chunk[len("data: "):]  # "data: " 부분 제거
                    try:
                        data = json.loads(chunk)  # JSON 파싱
                        event = data.get("event")
                        print(f"Event: {event}, Data: {data}")  # 이벤트와 데이터 출력

                        # Process "message" events
                        if event == "message":
                            answer = data.get("answer", "")
                            full_response += answer
                            message_placeholder.markdown(full_response + "▌")
                            time.sleep(0.05)  # Simulate typing effect

                        # Update conversation_id if provided in the response
                        if "conversation_id" in data:
                            st.session_state.conversation_id = data["conversation_id"]

                    except json.JSONDecodeError:
                        print(f"Invalid JSON received: {chunk}")  # 문제 있는 청크 출력
                        continue 
        except Exception as e:
            full_response = "Sorry, there was an error connecting to the API."
            message_placeholder.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append(
        {"role": "assistant", "content": full_response.strip()}
    )
