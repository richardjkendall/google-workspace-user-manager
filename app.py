from __future__ import print_function
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def main():
    """
    get users and update aliases
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('admin', 'directory_v1', credentials=creds)

    with open('aliases.csv', newline='') as csvfile:
        aliasreader = csv.reader(csvfile, delimiter=',')
        for row in aliasreader:
            to_adr = row[0].lower().strip()
            from_adr = row[1].lower().strip()
            print(f"Alias for {from_adr} to {to_adr}")

            result = service.users().aliases().insert(userKey=to_adr, body={
                "alias": from_adr
            }).execute()
            print(result)


if __name__ == '__main__':
    main()
