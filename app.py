import os
import streamlit as st
import hmac


def authenticate():
    """Returns `True` if the user had the correct passcode."""

    def passcode_entered():
        """Checks whether a passcode entered by the user is correct."""
        if hmac.compare_digest(st.session_state["passcode"], st.secrets["passcode"]):
            st.session_state["passcode_correct"] = True
            del st.session_state["passcode"]  # Don't store the passcode.
        else:
            st.session_state["passcode_correct"] = False

    # Return True if the passcode is validated.
    if st.session_state.get("passcode_correct", False):
        return True

    # Show input for passcode.
    st.text_input(
        "Passcode", type="password", on_change=passcode_entered, key="passcode"
    )
    if "passcode_correct" in st.session_state:
        st.error("😕 Passcode incorrect!")
    return False

def delete_file(filename: str):
    if os.path.exists(filename):
        os.remove(filename)


def load_main_page():
    # Create data folder if not exist
    if not os.path.exists('data'):
        os.makedirs('data')

    st.title("File Server Application")

    # File upload section
    st.subheader("Upload file to server")
    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file:
        file_name = f"data/{uploaded_file.name}"
        with open(file_name, 'wb') as f:
            bytes_data = uploaded_file.getvalue()
            f.write(bytes_data)
        st.success(f"File uploaded successfully: File name: {uploaded_file.name}")

    st.divider()

    # List files section
    st.subheader("Uploaded files")
    files = os.listdir("data")

    if not files:
        st.info("No files found.")
    else:
        for file in files:
            col1, col2, col3 = st.columns([0.8, 0.1, 0.1])
            col1.write(f"{file}")
            file_path = f"data/{file}"
            with open(file_path, "rb") as f:
                col2.download_button(
                    label="⬇️",
                    data=f,
                    file_name=file
                )
            col3.button('❌', on_click=delete_file, args=[file_path], key=file)

    hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    # Set page config
    st.set_page_config(
        page_title="File Server",
        page_icon="💻",
    )

    auth = authenticate()
    if auth:
        load_main_page()

if __name__ == "__main__":
    main()
