from oauth2client.service_account import ServiceAccountCredentials
import gspread
import gspread_dataframe as gd
import pandas as pd

class AccessGoogleSheets:
    def __init__(self,sheet_id="",sheet_name="Sample Test Sheet",wk_name="Test Workframe",df=pd.DataFrame(),email= "anwit.jagtap@embibe.com"):
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.wk_name = wk_name
        self.df = df
        self.email_id = email
        scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('skilled-bonus-342212-486490d0e7e1.json', scope)
        client = gspread.authorize(creds)
        self.gc = gspread.service_account(filename='skilled-bonus-342212-486490d0e7e1.json')
        
    def sheet_to_df(self):
        sheet = self.gc.open_by_key(self.sheet_id)
        worksheet = sheet.worksheet(self.wk_name)
        df = pd.DataFrame(worksheet.get_all_records())
        return df
    
    def df_to_sheet(self):
        print(f"self.sheet_id:{self.sheet_id}")
        if self.sheet_id == "":
            new_spreadsheet = self.gc.create(self.sheet_name)
            self.sheet_id = new_spreadsheet.id
            print(f"New spreadsheet created with ID: {new_spreadsheet.url}")
            new_spreadsheet.share(self.email_id, perm_type='user', role='writer')
            try:
                worksheet = new_spreadsheet.worksheet(self.wk_name)
            except:
                worksheet = new_spreadsheet.worksheet("Sheet1")
                worksheet.update_title(self.wk_name)
        else:
            existing_sheet = self.gc.open_by_key(self.sheet_id)
            try:
                worksheet = existing_sheet.worksheet(self.wk_name)
                worksheet.clear()
            except:
                print(f"Given wk_name:{self.wk_name} does not exist. Creating new sheet")
                worksheet = existing_sheet.add_worksheet(self.wk_name, 100, 100)
        try:
            gd.set_with_dataframe(worksheet,self.df)
            print(f"{self.sheet_id}: {self.wk_name} is updated successfully")
        except Exception as e:
            print(e)
    
    def create_sheet(self):
        spreadsheet_name = self.wk_name
        new_spreadsheet = self.gc.create(spreadsheet_name)
        self.sheet_id = new_spreadsheet.id
        email_to_grant_access = self.email_id
        
        print(f"New spreadsheet created with ID: {new_spreadsheet.url}")
    
        new_spreadsheet.share(email_to_grant_access, perm_type='user', role='writer')
        new_spreadsheet.share("", perm_type="anyone", role="reader")
        
        print(f"Access granted to {email_to_grant_access} for the newly created spreadsheet.")

    def create_worksheet(self,worksheet_name = "Sheet2"):
        # new_sheet = self.sheet_id
        # new_spreadsheet = new_sheet.add_worksheet(title=worksheet_name, rows=100, cols=100)
        # self.wk_name = new_spreadsheet
        # self.df_to_sheet()
        print(f"In create_worksheet function,new spreadsheet {worksheet_name} created.")

        existing_sheet = self.gc.open_by_key(self.sheet_id)
        try:
            new_spreadsheet = existing_sheet.worksheet(worksheet_name)
            new_spreadsheet.clear()
        except:
            print(f"Given worksheet name: {worksheet_name} does not exist. Creating a new sheet.")
            new_spreadsheet = existing_sheet.add_worksheet(worksheet_name, 100, 100)

        self.wk_name = worksheet_name
        self.df_to_sheet()
        print(f"New worksheet '{worksheet_name}' created or updated.")
