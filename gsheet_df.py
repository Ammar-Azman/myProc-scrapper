import gspread
import pandas as pd
import pathlib

class Google:
    def get_service_account(self):
        myProc_path = pathlib.Path('./jsonfile/jsonFromGoogle.json')
        gc = gspread.service_account(filename=myProc_path)
        return gc

    def open_sheet(self, sheet_name:str):
        gc = self.get_service_account()
        sh = gc.open(sheet_name)
        return sh
