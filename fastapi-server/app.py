from fastapi import FastAPI, UploadFile, HTTPException, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from LegSheet import SessionHandler
from LegSheet import LegSheet
from pdf_creation.create_pdf import get_all_pdf
import pandas as pd
import uvicorn
import os

app = FastAPI()
session = SessionHandler()

# Configure CORS to allow requests from react-app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/new_form')
def new_form():
    # Create a new LegSheet with a unique identifier
    try:
        uuid = session.new_sheet()
        return {"uuid": str(uuid)}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to create new form.")


@app.post("/upload_leg")
async def upload(file: UploadFile = Form(...), sessionUuid: str = Form(...)):
    # Ensure the uploaded file is an Excel spreadsheet
    if file.filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(await file.read(), sheet_name=None)
            leg_sheet = session.get_sheet(sessionUuid)
            leg_sheet.upload_leg(df)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse Excel file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an .xlsx file.")
    

@app.post("/upload_ga")
async def upload(file: UploadFile = Form(...), sessionUuid: str = Form(...)):
    if file.filename.endswith('.xlsx'):
        try:
            df = pd.read_excel(await file.read(), sheet_name=None)
            ga_sheet = session.get_sheet(sessionUuid)
            ga_sheet.upload_ga(df)
            return {"status": "success"}
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse Excel file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an .xlsx file.")
    

@app.post("/process")
async def process_data(data: dict):
    try:
        sessionUuid = data.get('sessionUuid')
        columns = data.get('columns', [])
        
        # Retrieve the LegSheet object using the uuid provided by the user
        leg_sheet = session.get_sheet(sessionUuid)
        if leg_sheet:
            leg_sheet.process(columns)
            return {"status": "success"}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process data.")
    

@app.get("/download/{sessionUuid}")
async def download(sessionUuid: str):
    leg_sheet = session.get_sheet(sessionUuid)
    if leg_sheet:
        print('Legsheet found')
        pdf_data = leg_sheet.generate_pdf()

        # Create the zip file in memory.
        zip_io = get_all_pdf(leg_sheet.rep_dict)

        # Stream the zip file to the client.
        response = StreamingResponse(zip_io,
                                     media_type="application/zip",
                                     headers={"Content-Disposition": f'attachment; filename={sessionUuid}.zip'})

        session.delete_sheet(sessionUuid)
        return response
    else:
        raise HTTPException(status_code=404, detail='File not found.')


if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)