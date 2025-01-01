import streamlit as st
import openai
import random
from datetime import datetime
from streamlit.logger import get_logger
from streamlit.components.v1 import html

st.set_page_config(page_title="sulu-AI",initial_sidebar_state="collapsed",layout="wide")
# st.write(st.query_params)
iframe_check_code = """
<script>
    const isInIframe = window.self !== window.top;
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('iframe', isInIframe);
    const newUrl = `${window.location.pathname}?${queryParams.toString()}`;
    window.history.replaceState(null, '', newUrl);  // Modify the URL
</script>
"""

# Embed JavaScript
html(iframe_check_code, height=0)
query_params = st.query_params
# st.write(query_params)
is_in_iframe = query_params.get("iframe", ["false"])[0] == "true"

if False :
    
    
    
    st.subheader('')
    st.latex(r'''
        \textsf{\Huge \textbf {jingax-AI}}
             ''')
    # st.title("jingax-AI")
    html_string = '''
      <center style="color:#bfbfbf;"> by aastik </center>
     '''
    st.markdown(html_string, unsafe_allow_html=True)
else:
    pass
    # st.write('<style>div.block-container{padding-top:-2rem;}</style>', unsafe_allow_html=True)
q_count =10
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.logger = get_logger(__name__)
    st.session_state.curr_id = f"{random.randint(10000, 99999)}-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    st.session_state.logger.info(f"New INIT : {st.session_state.curr_id}")
    about_me = f = open("about_me.txt", "r").read()
    st.session_state.use_count = 0
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant that knows detailed information about Suyesha. Try to be as brief as possible in your responses, be quirky and fun"},
        {"role": "system", "content": about_me},
        {"role": "assistant", "content": "Hi, I am sulu-AI! Suyesha's AI assistant. You can ask me anything about Suyesha"},
    ]
    
    st.session_state.client = openai.OpenAI(api_key = st.secrets['api']['openai'])



# Display chat messages from history on app rerun
for message in st.session_state.messages[2:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

 


def chat_with_bot(user_message):
    # Append user query to the message history
    # st.session_state.messages.append({"role": "user", "content": user_message})
    
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
    # st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    st.session_state.use_count += 1
    return assistant_reply



# React to user input



if prompt := st.chat_input("Ask me anything about Suyesha",disabled=st.session_state.use_count>q_count):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.logger.info(f"{st.session_state.curr_id}::user:: {prompt}")
    if st.session_state.use_count <q_count :
        response = chat_with_bot(prompt)
    else:
        response = f"You get to ask only {q_count} questions!"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.logger.info(f"{st.session_state.curr_id}::jinga-ai:: {response}")
# st.write(st.session_state.messages)
