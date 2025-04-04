import streamlit as st
from openai import OpenAI
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock
import httpx

from settings import settings


def check_password():
    def password_entered():
        if st.session_state["password"] == settings.streamlit_system.PASSWORD:
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input(settings.streamlit_texts.PASSWORD_REQUEST, type="password", on_change=password_entered, key="password")
        return False
    
    elif not st.session_state["password_correct"]:
        st.text_input(settings.streamlit_texts.PASSWORD_REQUEST, type="password", on_change=password_entered, key="password")
        st.error(settings.streamlit_texts.PASSWORD_INCORRECT)
        return False
    
    else:
        return True
    

@st.cache_resource(show_spinner=False)
def get_openai_client(api_key: str, proxy_url: str = None):
    """
    Function to initialize the OpenAI client with the API key and optional proxy URL.
    """
    return OpenAI(
        api_key=api_key,
        http_client=httpx.Client(proxy=proxy_url),
    )


@st.cache_resource(show_spinner=False)
def get_openai_assistant(_openai_client: OpenAI, assistant_id: str):
    """
    Function to retrieve the assistant using the OpenAI client.
    """
    return _openai_client.beta.assistants.retrieve(assistant_id=assistant_id)
    

# Check if the user has entered the correct password
if check_password():
    # Set the page title and layout
    st.title(settings.streamlit_texts.TITLE)

    # Initialize the OpenAI client, and retrieve the assistant
    client = get_openai_client(api_key=settings.openai.API_KEY, proxy_url=settings.openai.PROXY_URL)
    assistant = client.beta.assistants.retrieve(assistant_id=settings.openai.ASSISTANT_ID)

    # Initialise session state to store conversation history locally to display on UI
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Display messages in chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Textbox and streaming process
    if user_query := st.chat_input(settings.streamlit_texts.CHAT_INPUT):
        # Create a new thread if it does not exist
        if "thread_id" not in st.session_state:
            thread = client.beta.threads.create()
            st.session_state.thread_id = thread.id

        # Display the user's query
        with st.chat_message("user"):
            st.markdown(user_query)

        # Store the user's query into the history
        st.session_state.chat_history.append({"role": "user", "content": user_query})

        # Add user query to the thread
        client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_query
        )

        # Stream the assistant's reply
        with st.chat_message("assistant"):
            stream = client.beta.threads.runs.create(
                thread_id=st.session_state.thread_id,
                assistant_id=settings.openai.ASSISTANT_ID,
                stream=True
            )

            # Empty container to display the assistant's reply
            assistant_reply_box = st.empty()

            # A blank string to store the assistant's reply
            assistant_reply = ""

            # Iterate through the stream
            for event in stream:
                # Here, we only consider if there's a delta text
                if isinstance(event, ThreadMessageDelta):
                    if isinstance(event.data.delta.content[0], TextDeltaBlock):
                        # empty the container
                        assistant_reply_box.empty()
                        # add the new text
                        assistant_reply += event.data.delta.content[0].text.value
                        # display the new text
                        assistant_reply_box.markdown(assistant_reply)

            # Once the stream is over, update chat history
            st.session_state.chat_history.append({"role": "assistant", "content": assistant_reply})
