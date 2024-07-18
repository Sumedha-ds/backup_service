from __future__ import print_function
import os
import pickle
import time
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def create_folder(service, folder_name):
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    return file.get('id')

def main():
    """Shows basic usage of the Drive v3 API."""
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0, headless=True)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('drive', 'v3', credentials=creds)

    # Create a folder in Google Drive
    folder_id = create_folder(service, 'BackupFolder')
    
    # Folder to backup
    folder_to_backup = 'C:\\Users\\sumed\\OneDrive\\Desktop\\backupData'

    for filename in os.listdir(folder_to_backup):
        file_path = os.path.join(folder_to_backup, filename)
        if os.path.isfile(file_path):
            file_metadata = {'name': filename, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, mimetype='application/octet-stream')
            file = service.files().create(body=file_metadata,
                                          media_body=media,
                                          fields='id').execute()
            logging.info(f'File {filename} uploaded with ID: {file.get("id")}')

if __name__ == '__main__':
    while True:
        main()
        time.sleep(86400)  # Sleep for 1 day
