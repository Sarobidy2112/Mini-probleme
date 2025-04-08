from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/process")
def process_data():
    try:
        data = pd.read_csv("data.csv")
        stats = {
            "columns": list(data.columns),
            "row_count": len(data),
            "mean_values": data.mean(numeric_only=True).to_dict(),
            "max_values": data.max(numeric_only=True).to_dict(),
            "min_values": data.min(numeric_only=True).to_dict(),
        }
        return {"result": "Statistiques calculées avec succès", "stats": stats}
    except Exception as e:
        return {"error": str(e)}

@app.get("/download")
def download_csv():
    return FileResponse("data.csv", media_type="text/csv", filename="data.csv")
