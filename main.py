import streamlit as st
import openai

st.write('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)
q_count =10
# Initialize chat history
if "messages" not in st.session_state:
    about_me = f = open("about_me.txt", "r").read()
    st.session_state.use_count = 0
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that knows detailed information about Aastik. Try to be as brief as possible in your responses, be quirky and fun"},
        {"role": "system", "content": about_me},
        {"role": "assistant", "content": "Hi, I am jingaxAI! Aastik's AI assistant. You can ask me anything about Aastik"},
    ]
    
    st.session_state.client = openai.OpenAI(api_key = st.secrets['api']['openai'])



# Display chat messages from history on app rerun
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

 


def chat_with_bot(user_message):
    # Append user query to the message history
    st.session_state.messages.append({"role": "user", "content": user_message})
    
    # Call the OpenAI API
    response = st.session_state.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state.messages,
        temperature=0.7,
    )
    
    # Get the assistant's reply
    # print(response)
    assistant_reply = response.choices[0].message.content
    
    # Add the assistant's reply to the message history
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.use_count += 1
    return assistant_reply



# React to user input



if prompt := st.chat_input("Ask me anything about Aastik",disabled=st.session_state.use_count>q_count):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.use_count <q_count :
        response = chat_with_bot(prompt)
    else:
        response = f"You get to ask only {q_count} questions!"
    # Display assistant response in chat message container
    # with st.chat_message("assistant"):
        # st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
