from googleapiclient.discovery import build
from google_utils import GoogleAPI, load_google_credentials
import pandas as pd


class GoogleSheetsAPI(GoogleAPI):
    def __init__(self, credentials):
        super().__init__(credentials)

        self.sheets = build('sheets', 'v4', credentials=credentials)

    def load_sheet_to_dataframe(self, spreadsheet_id, spreadsheet_range, column_types=None):
        spreadsheets = self.sheets.spreadsheets()

        result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range=spreadsheet_range).execute()
        values = result.get('values', [])

        if not values:
            return pd.DataFrame()

        df = pd.DataFrame(values[1:], columns=values[0])  # Use the first row as column names

        if column_types:
            for column, dtype in column_types.items():
                if column in df.columns:
                    df[column] = df[column].astype(dtype)

        return df


def example():
    scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    user_google_sheets_credentials_path = '../Credentials/google_sheets_user_token.json'
    google_credentials_path = '../Credentials/google_client.json'
    credentials = load_google_credentials(user_google_sheets_credentials_path, google_credentials_path, scope)

    google_sheets_api = GoogleSheetsAPI(credentials)
    # https://docs.google.com/spreadsheets/d/<spreadsheet_id>/edit
    # You will need your own, since it is account based
    spreadsheet_id = '1JFpTX7CfaQ-GYvUSiq6dA397tgVxM1v3x_s2vA_UIeQ'
    spreadsheet_range = 'Weekly Training!A1:X25'
    google_sheets_api.load_sheet_to_dataframe(spreadsheet_id, spreadsheet_range)


if __name__ == '__main__':
    example()