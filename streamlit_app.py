import streamlit as st
from openai import OpenAI

# Show title and description with spacing.
st.title("💬 Ministério de Pequenos Grupos")

# Add descriptions with clear spacing using HTML.
st.markdown(
    """
    Querido líder de PG ou GD, você pode perguntar o que quiser a respeito de Grupos neste chat.<br>
    Todas as informações foram treinadas com dados públicos.<br>
    <br>
    Que Deus o abençoe :)
    """,
    unsafe_allow_html=True
)

# Ask user for their OpenAI API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    # Initialize OpenAI client with the provided API key.
    client = OpenAI(api_key=openai_api_key)

    # Initialize session state for storing chat messages.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display all previous messages.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user message.
    if prompt := st.chat_input("Digite sua pergunta aqui..."):

        # Store user's message in session state.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response from the OpenAI API.
        response = ""
        stream = client.chat_completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the assistant's response.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        # Store assistant's response in session state.
        st.session_state.messages.append({"role": "assistant", "content": response})
