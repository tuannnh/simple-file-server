import os
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

from requests import Request

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def authenticate():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds


def upload_file(service, file_path):
    file_metadata = {'name': os.path.basename(file_path)}
    print(f"File path: {file_path}")
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file['id']


def list_files(service):
    results = service.files().list().execute()
    files = results.get('files', [])
    return files


def download_file(service, file_id):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while done is False:
        status, done = downloader.next_chunk()

    return fh.getvalue()


def delete_file(filename: str):
    if os.path.exists(filename):
        os.remove(filename)


def main():
    # Set page config
    st.set_page_config(
        page_title="Server file upload app",
        page_icon="💻",
    )

    # Create data folder if not exist
    if not os.path.exists('data'):
        os.makedirs('data')

    st.title("Server File Upload App")

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


if __name__ == "__main__":
    main()
