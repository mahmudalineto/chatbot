import streamlit as st
import openai

# Show title and description with spacing.
st.title("💬 Ministério de Pequenos Grupos")

st.markdown(
    """
    Querido líder de PG ou GD, você pode perguntar o que quiser a respeito de Grupos neste chat.<br>
    Todas as informações foram treinadas com dados públicos.<br>
    <br>
    Que Deus o abençoe :)
    """,
    unsafe_allow_html=True
)

# Use the API key from st.secrets
openai_api_key = st.secrets["openai_api_key"]
openai.api_key = openai_api_key

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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
        )

        response_content = response['choices'][0]['message']['content']
        with st.chat_message("assistant"):
            st.markdown(response_content)

        # Store assistant's response in session state.
        st.session_state.messages.append({"role": "assistant", "content": response_content})
    except Exception as e:
        st.error(f"Erro ao gerar resposta: {e}")
