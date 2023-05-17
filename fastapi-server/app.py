from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from LegSheet import SessionHandler
from LegSheet import LegSheet
import pandas as pd
import uvicorn
import os

app = FastAPI()

# Global dictionary to store LegSheet instances
leg_sheets = {}

# Configure CORS to allow requests from react-app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(file: UploadFile):
    # Ensure the uploaded file is an Excel spreadsheet
    if file.filename.endswith('.xlsx'):
        try:
            data_frame = pd.read_excel(await file.read(), sheet_name='House')
            uuid = session.new_sheet(data_frame)
            leg_sheet = session.get_sheet(str(uuid))
            column_names = leg_sheet.read_columns()
            return {"uuid": str(uuid), "columnNames": column_names}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse Excel file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an .xlsx file.")

@app.post("/process")
async def process_data(data: dict):
    try:
        uuid = data.get('uuid')
        columns = data.get('columns', [])
        
        # Retrieve the LegSheet object using the uuid provided by the user
        leg_sheet = session.get_sheet(uuid)
        if leg_sheet:
            leg_sheet.process(columns)
            session.delete_sheet(uuid)
            return {"message": "Data processed"}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process data.")


if __name__ == '__main__':
    session = SessionHandler()
    uvicorn.run(app, host='localhost', port=8000)