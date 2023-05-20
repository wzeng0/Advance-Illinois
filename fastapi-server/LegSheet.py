from datetime import datetime, timedelta
import pandas as pd
import uuid


class LegSheet:
    def __init__(self):
        self.expiration_time = datetime.now() + timedelta(minutes=5)
        self.leg_house_df = None
        self.leg_senate_df = None
        self.ga_house_df = None
        self.ga_senate_df = None
    
    def upload_leg(self, df):
        # Check for sheet_name 'House' or 'Senate'
        if 'House' in df.keys() and 'Senate' in df.keys():
            self.leg_house_df = df['House']
            self.leg_senate_df = df['Senate']
        else:
            raise Exception('Invalid Excel file: missing sheets "House" or "Senate"')
        
    def upload_ga(self, df):
        if '103rd House' in df.keys() and '103rd Senate' in df.keys():
            self.ga_house_df = df['103rd House']
            self.ga_senate_df = df['103rd Senate']
        else:
            raise Exception('Invalid Excel file: missing sheets "103rd House" or "103rd Senate"')
    
    '''
    def process(self, columns: list):
        try:
            # Rename the columns
            self.df = self.df[columns].rename(columns={"Type": "District"}).sort_values(by="District")
            for column in columns:
                data = self.df[column]
                print(data)
        except Exception as e:
            print(f'Error processing data: {e}')
            return
    '''

    def cleanup(self):
        # TODO: Implement cleanup logic
        pass


class SessionHandler:
    def __init__(self):
        self.session_data = {}

    def new_sheet(self):
        # Create a new LegSheet with a unique identifier
        new_uuid = uuid.uuid4()
        leg_sheet = LegSheet()
        self.session_data[str(new_uuid)] = leg_sheet
        return new_uuid
    
    def get_sheet(self, uuid: str):
        # Retrieve the LegSheet from memory
        leg_sheet = self.session_data.get(uuid)
        return leg_sheet

    def delete_sheet(self, uuid: str):
        # Delete the LegSheet from memory
        leg_sheet = self.session_data.get(uuid)
        if leg_sheet:
            del self.session_data[uuid]
