from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from LegSheet import SessionHandler
from LegSheet import LegSheet
from pdf_creation.create_pdf import get_all_pdf_bytes
import pandas as pd
import uvicorn
import os
import zipfile

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
        # df = pd.read_excel(await file.read(), sheet_name=None)
        # leg_sheet = session.get_sheet(sessionUuid)
        # leg_sheet.upload_leg(df)
        # return {"status": "success"}
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
    

# @app.post("/process")
# async def process_data(data: dict):
#     try:
#         sessionUuid = data.get('sessionUuid')
#         columns = data.get('columns', [])
        
#         # Retrieve the LegSheet object using the uuid provided by the user
#         leg_sheet = session.get_sheet(sessionUuid)
#         if leg_sheet:
#             leg_sheet.process(columns)
#             session.delete_sheet(sessionUuid)
#             return {"status": "success"}
#         else:
#             raise HTTPException(status_code=404, detail="File not found.")
#     except Exception as e:
#         raise HTTPException(status_code=400, detail="Failed to process data.")
    

@app.post("/process")
async def process_data(data: dict, response: Response):
    try:
        sessionUuid = data.get('sessionUuid')
        columns = data.get('columns', [])
        
        # Retrieve the LegSheet object using the uuid provided by the user
        leg_sheet = session.get_sheet(sessionUuid)
        if leg_sheet:
            full_dict = leg_sheet.process(columns)
            pdf_data_list = get_all_pdf_bytes(full_dict)
            output_directory = "/pdf"

            # Create a temporary zip file to store the PDFs
            zip_file_path = "/pdf_batch.zip"

            # Generate individual PDFs
            for i, pdf_data in enumerate(pdf_data_list):
                output_path = os.path.join(output_directory, f"pdf_{i}.pdf")
                generate_pdf(pdf_data, output_path)

            # Create a zip archive containing all the PDF files
            with zipfile.ZipFile(zip_file_path, "w") as zipf:
                for i in range(len(pdf_data_list)):
                    pdf_path = os.path.join(output_directory, f"pdf_{i}.pdf")
                    zipf.write(pdf_path, arcname=f"pdf_{i}.pdf")
            
            # Set the response headers for file download
            response.headers["Content-Disposition"] = 'attachment; filename="pdf_batch.zip"'
            response.headers["Content-Type"] = "application/zip"

            # Stream the zip file to the response
            with open(zip_file_path, "rb") as file:
                content = file.read()
                response.body = content

            # Clean up the temporary zip file and individual PDFs
            os.remove(zip_file_path)
            for i in range(len(pdf_data_list)):
                pdf_path = os.path.join(output_directory, f"pdf_{i}.pdf")
                os.remove(pdf_path)

            session.delete_sheet(sessionUuid)
            return {"status": "success"}
        else:
            raise HTTPException(status_code=404, detail="File not found.")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Failed to process data.")


def generate_pdf(pdf_data, output_path):
    with open(output_path, "wb") as file: 
        file.write(pdf_data.getvalue()) 

if __name__ == '__main__':
    uvicorn.run('app:app', host='localhost', port=8000, reload=True)