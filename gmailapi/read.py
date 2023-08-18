
import os.path
import pickle
import base64
import pymysql
import quopri
from bs4 import BeautifulSoup
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import datetime

# Define the SCOPES. If modifying it, delete the token.pickle file.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify']

def authenticate():
    """Authenticates the user using OAuth 2.0 and returns the Gmail API service."""
    creds = None

    # The file token.pickle contains the user access token.
    # Check if it exists
    if os.path.exists('/home/placement/placementwebsite/gmailapi/token.pickle'):
        with open('/home/placement/placementwebsite/gmailapi/token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If credentials are not available or are invalid, ask the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('/home/placement/placementwebsite/gmailapi/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the access token in token.pickle file for the next run
        with open('/home/placement/placementwebsite/gmailapi/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Connect to the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    return service

def extract_text(part):
    part_data = part.get('body', {}).get('data', '')
    if part_data:
        byte_code = base64.urlsafe_b64decode(part_data)
        byte_code = quopri.decodestring(byte_code).decode('utf-8')
        return byte_code
    return ''

def process_parts(parts):
    """Recursively processes parts of an email."""
    body = ''

    for part in parts:
        if part.get('mimeType') == 'text/plain':
            body += extract_text(part)
        elif part.get('mimeType') == 'text/html':
            soup = BeautifulSoup(extract_text(part), 'html.parser')
            body += soup.get_text()
            # Handle the quoted text (gmail_quote)
            quoted_text = soup.find('div', class_='gmail_quote')
            if quoted_text:
                body += "\n\nQuoted Text:\n" + quoted_text.get_text()
        elif part.get('mimeType') == 'multipart/related':
            related_parts = part.get('parts', [])
            body += process_parts(related_parts)  # Recursively process related parts
        elif part.get('mimeType').startswith('image/'):
            # Handle image attachments here
            image_attachment = extract_text(part)
            # You can process or save the image attachment as needed

    return body


def get_message_body(message):
    """Extracts the message body from a Gmail API message object."""
    parts = message['payload']['parts']
    return process_parts(parts)

def get_emails():
    print("checl")

    """Fetches and prints a list of emails from the user's Gmail account."""
    try:
        service = authenticate()
        # Request a list of all the unread messages
        result = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = result.get('messages', [])

        # Iterate through all the unread messages
        for msg in messages:
            
            conn = pymysql.connect(
            host="localhost",
            user="placement",
            password="Suraj@2001",
            database="placement"
            )

# Create a cursor object to execute SQL commands
            cursor = conn.cursor()
            # Get the message from its id
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()

            # Get the subject and sender email from the headers
            subject = ''
            sender = ''
            for header in txt['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
                elif header['name'] == 'From':
                    sender = header['value']

            # Get the message body
            body = get_message_body(txt)

            # Printing the subject, sender's email, and message
            date = datetime.datetime.now()
            
            message = body
            if message == '' or message == ' ':
                message = 'Please refer your email'
# Sample data to insert into the table
            sample_data = [
            (subject, str(message), date),
            ]

# Insert data into the table
            insert_sql = 'INSERT INTO display_notifications (title, description, date) VALUES (%s, %s, %s)'
            cursor.executemany(insert_sql, sample_data)

# Commit the changes and close the connection
            conn.commit()
            conn.close()
            
            
            # print("Subject:", subject)
            # print("From:", sender)
            # print("Message:", body)
            # print('\n')

            # Mark the message as read
            service.users().messages().modify(userId='me', id=msg['id'], body={'removeLabelIds': ['UNREAD']}).execute()

    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    get_emails()





