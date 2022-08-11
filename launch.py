from gsheet_df import Google
from scrapper import Scrapper
import time
import pandas as pd

# instantiate object from module
goo = Google()
scrap = Scrapper()

def launch_scrapper(start, end_before):
    """
    1. Setup a Google Sheet using JSON token from Google Cloud. 
    2. Extract the data from myProcurement. 
    3. Push into Google Sheet allocated. 
    """
    SPREADSHEET_NAME = ''
    SHEET_NAME = ''
    try:
        all_info = scrap.extract_info(start, end_before)

        # Google Sheet setup
        sh = goo.open_sheet(SPREADSHEET_NAME)
        #sh.add_worksheet(title='Tender', rows=100, cols=20) # add sheet
        worksheet = sh.worksheet(title=SHEET_NAME) # choose sheet

        # Dataframe setup
        df = pd.DataFrame(all_info)

        # push update to Google Sheet
        #worksheet.update(column_list + row_value)

        # append new row
        all_row = df.loc[0:].values.tolist()
        for val in all_row: 
            worksheet.append_row(val)

    except Exception as e1:
        print("E1 ERROR: ", e1)


if __name__ == '__main__':
    try:
        start_time = time.time()
        launch_scrapper(start=0, end_before=2)
        print('DONE!', f'\nEXE TIME:{(time.time()-start_time)/60} min(s)')
    except Exception as e:
        print(e)




