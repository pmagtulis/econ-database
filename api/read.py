from googleapiclient.discovery import build
from google.oauth2 import service_account


SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)





# The ID of spreadsheet.
SAMPLE_SPREADSHEET_ID = '1ScmJ4rTC9DmHQjOdP-KiAD4cuP2UKfYrbhpdiEot82M'




service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Revenue growth!A1:D32").execute()
# values = result.get('values', [])
print(result)
