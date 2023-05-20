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
        self.house = None
        self.senators = None
    
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
    
    def process(self, columns: list):
        print('processing')
        try:
            # Rename 'Type' column to 'District' and sort by 'District'
            # Below integrated from CSV processing team
            columns = columns + ['Type', 'SCHOOL DISTRICT']
            self.leg_house_df = self.leg_house_df[columns].rename(columns={"Type": "District"}).sort_values(by="District")
            self.ga_house_df = self.ga_house_df[['Representative', 'District']]

            house_names = self.ga_house_df['Representative'].values

            self.house = pd.merge(self.ga_house_df, self.leg_house_df, on='District')
            self.house = self.house.drop(['District'], axis=1).drop_duplicates()

            cps_house = self.house.loc[self.house['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299']
            cps_house_index = self.house.loc[self.house['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299'].index
            cps_house_df = cps_house
            self.house = self.house.drop(cps_house_index)

            house_df_list = []
            for name in house_names:
                empty_df = pd.DataFrame({})
                empty_df = self.house_df(name)
                house_df_list.append(empty_df)

            self.leg_senate_df = self.leg_senate_df[columns].rename(columns={"Type": "District"}).sort_values(by="District")
            self.ga_senate_df = self.ga_senate_df[['Senator', 'District']]
            sen_names = self.ga_senate_df['Senator'].values
            self.senators = pd.merge(self.ga_senate_df, self.leg_senate_df, on='District')
            self.senators = self.senators.drop(['District'], axis=1).drop_duplicates()

            cps_senators = self.senators.loc[self.senators['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299']
            cps_senators_index = self.senators.loc[self.senators['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299'].index
            cps_senators_df = cps_senators
            self.senators = self.senators.drop(cps_senators_index)

            sen_df_list = []
            for name in sen_names:
                empty_df = pd.DataFrame({})
                empty_df = self.sen_df(name)
                sen_df_list.append(empty_df)

            chicago_sen = cps_senators_df['Senator'].values[0]
            chicago_combined = cps_house_df
            chicago_combined['Senator'] = chicago_sen
            print(chicago_combined)

        except Exception as e:
            print(f'Error processing data: {e}')
            return
        
    def house_df(self, name):
        '''takes representative name and returns their info from house dataframe'''
        return self.house.loc[self.house['Representative'] == name]
    
    def sen_df(self, name):
        '''takes senator name and returns their info from senate dataframe'''
        return self.senators.loc[self.senators['Senator'] == name]

    def cleanup(self):
        # TODO: Implement cleanup logic
        print('cleaning up')
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
