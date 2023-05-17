from datetime import datetime, timedelta
import pandas as pd
import uuid


class LegSheet:
    def __init__(self, data_frame: pd.DataFrame):
        self.df = data_frame
        self.expiration_time = datetime.now() + timedelta(minutes=5)

    def read_columns(self):
        try:
            data = list(self.df.columns)
        except Exception as e:
            print(f'Error reading columns: {e}')
            return []
        
        return list(data)
    
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

    def cleanup(self):
        # TODO: Implement cleanup logic
        pass


class SessionHandler:
    def __init__(self):
        self.session_data = {}

    def new_sheet(self, data_frame: pd.DataFrame):
        # Create a new LegSheet with a unique identifier
        new_uuid = uuid.uuid4()
        leg_sheet = LegSheet(data_frame)
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
