from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import pandas as pd
import io

app = FastAPI()

# Configure CORS to allow requests from react-app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def read_excel(file: UploadFile):
    # Ensure the uploaded file is an Excel spreadsheet
    if file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
        contents = await file.read()
        try:
            data = pd.read_excel(io.BytesIO(contents), sheet_name='House')
            return data
        except Exception as e:
            raise HTTPException(status_code=400, detail="Failed to parse Excel file.")
    else:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an Excel file.")


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = await read_excel(file)
    column_names = list(data.columns)
    return {"columnNames": column_names}

@app.post("/selectedColumns")
async def selected_columns(columns: List[str]):
    print(columns)
    return {"message": "Columns received"}
