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
        self.cps_df = None
        self.rep_dict = {}
    
    def upload_leg(self, df):
        # Check for sheet_name 'House' or 'Senate'
        if 'House' in df.keys() and 'Senate' in df.keys():
            self.leg_house_df = df['House']
            self.leg_senate_df = df['Senate']
            self.cps_df = df['CPS Chart']
        else:
            raise Exception('Invalid Excel file: missing sheets "House" or "Senate"')
        
    def upload_ga(self, df):
        if '103rd House' in df.keys() and '103rd Senate' in df.keys():
            self.ga_house_df = df['103rd House']
            self.ga_senate_df = df['103rd Senate']
        else:
            raise Exception('Invalid Excel file: missing sheets "103rd House" or "103rd Senate"')
    
    def process(self, columns: list):
        try:
            # Rename 'Type' column to 'District' and sort by 'District'
            # Below integrated from CSV processing team

            # Rename 'New House Assignment' to 'District' and sort by 'District'
            self.leg_house_df = self.leg_house_df[columns + ['New House Assignment', 'SCHOOL DISTRICT', '% OF FULL \nFUNDING']]
            self.leg_house_df.rename(columns={'New House Assignment': 'District'}, inplace=True)
            self.leg_house_df.sort_values('District', inplace=True)

            self.ga_house_df = self.ga_house_df[['Representative', 'District']]
            house_names = self.ga_house_df['Representative'].values

            # Merge based on 'District', dropping duplicates
            house = pd.merge(self.leg_house_df, self.ga_house_df, on='District', how='inner').drop_duplicates()
            house.drop(columns=['District'], axis=1, inplace=True)

            
            # Senate
            self.leg_senate_df = self.leg_senate_df[columns + ['New Senate Assignment', 'SCHOOL DISTRICT', '% OF FULL \nFUNDING']]
            self.leg_senate_df.rename(columns={'New Senate Assignment': 'District'}, inplace=True)
            self.ga_senate_df = self.ga_senate_df[['Senator', 'District']]
            sen_names = self.ga_senate_df['Senator'].values

            senators = pd.merge(self.leg_senate_df, self.ga_senate_df, on='District', how='inner').drop_duplicates()
            senators.drop(columns=['District'], axis=1, inplace=True)


            # Modify Chicago Public Schools processing to only include districts that are entirely CITY OF CHICAGO SCHOOL DIST 299
            representatives = house['Representative'].unique()
            senators_unique = senators['Senator'].unique()

            drop_indices_rep = []
            drop_indices_sen = []

            for rep in representatives:
                rep_df = house[house['Representative'] == rep]
                if (rep_df['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299').all():
                    drop_indices_rep.extend(rep_df.index.tolist())
            
            for sen in senators_unique:
                sen_df = senators[senators['Senator'] == sen]
                if (sen_df['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299').all():
                    drop_indices_sen.extend(sen_df.index.tolist())

            house.drop(drop_indices_rep, inplace=True)
            senators.drop(drop_indices_sen, inplace=True)

            # Create dictionary of dataframes for each representative
            for rep in house_names:
                rep_df = house[house['Representative'] == rep].sort_values(by = ['% OF FULL \nFUNDING'], ascending = True)
                self.rep_dict[rep] = rep_df

            for sen in sen_names:
                sen_df = senators[senators['Senator'] == sen].sort_values(by = ['% OF FULL \nFUNDING'], ascending = True)
                self.rep_dict[sen] = sen_df

            # Add CPS representatives to rep_dict ONLY if their entire district is CITY OF CHICAGO SCHOOL DIST 299
            cps_representatives = [rep for rep in representatives if (house[house['Representative'] == rep]['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299').all()]
            cps_senators = [sen for sen in senators_unique if (senators[senators['Senator'] == sen]['SCHOOL DISTRICT'] == 'CITY OF CHICAGO SCHOOL DIST 299').all()]
            
            for rep in cps_representatives:
                self.rep_dict[rep] = self.cps_df

            for sen in cps_senators:
                self.rep_dict[sen] = self.cps_df

        except Exception as e:
            print(f'Error processing data: {e}')
            return
    
    def generate_pdf(self):
        try:
            # Create pdf using self.rep_dict here
            pass
        except Exception as e:
            print(f'Error generating PDF: {e}')
            return

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
