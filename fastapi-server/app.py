from typing import List, Dict, Any
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

app = FastAPI()

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    data = pd.read_excel(file.file)
    column_names = list(data.columns)
    return {"columnNames": column_names}

@app.post("/selectedColumns")
async def selected_columns(columns: List[str]):
    print(columns)
    return {"message": "Columns received"}
