from __future__ import print_function
import os.path
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SCOPES = [
  'https://www.googleapis.com/auth/admin.directory.user',
  'https://www.googleapis.com/auth/gmail.readonly',
  'https://www.googleapis.com/auth/gmail.settings.basic',
  'https://www.googleapis.com/auth/gmail.settings.sharing'
]

def main():
    """
    get users and update aliases
    """
    creds = None

    with open('delegates.csv', newline='') as csvfile:
        aliasreader = csv.reader(csvfile, delimiter=',')
        for row in aliasreader:
            to_adr = row[1].lower().strip()
            from_adr = row[0].lower().strip()
            print(f"Delegate from {from_adr} to {to_adr}")


            credentials = service_account.Credentials.from_service_account_file('credentials2.json')
            creds = credentials.with_scopes(SCOPES)
            creds = creds.with_subject(from_adr)
            service = build('gmail', 'v1', credentials=creds)

            result = service.users().settings().delegates().create(
              userId=from_adr,
              body={
                "delegateEmail": to_adr,
                "verificationStatus": "accepted"
              }
            ).execute()
            print(result)


if __name__ == '__main__':
    main()
