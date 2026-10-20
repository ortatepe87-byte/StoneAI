from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import tempfile

app = FastAPI()

model = YOLO("models/stone_v1.pt")

STONE_DATABASE = {
    "Granit": {
        "hardness": "6-7",
        "value": "1200-2500 TL/Ton",
        "usage": "Yapı taşı, mezar taşı, mutfak tezgahi",
        "description": "Magmatik kökenli cok dayanikli kayac."
    },

    "Bazalt": {
        "hardness": "6",
        "value": "900-1800 TL/Ton",
        "usage": "Yol yapimi, parke tasi, insaat",
        "description": "Volkanik kokenli koyu renkli kayac."
    },

    "Kuvars": {
        "hardness": "7",
        "value": "3000-12000 TL/Ton",
        "usage": "Cam, elektronik, taki",
        "description": "Yuksek silis oranina sahip sert mineral."
    },

    "Kalker": {
        "hardness": "3",
        "value": "300-900 TL/Ton",
        "usage": "Cimento, kirec, yapi malzemesi",
        "description": "Sedimanter kokenli kalsiyum karbonat kayac."
    },

    "Mermer": {
        "hardness": "3-4",
        "value": "2500-15000 TL/Ton",
        "usage": "Kaplama, dekorasyon, heykel",
        "description": "Metamorfik kokenli dekoratif kayac."
    }
}
STONE_NAMES = {
    0: "Granit",
    1: "Bazalt",
    2: "Kuvars",
    3: "Kalker",
    4: "Mermer"
}

@app.get("/")
def home():
    return {
        "status": "StoneAI API OK"
    }

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".jpg"
    ) as tmp:

        tmp.write(await file.read())
        image_path = tmp.name

    result = model(image_path)

    probs = result[0].probs

    stone = STONE_NAMES[int(probs.top1)]
    confidence = round(
        float(probs.top1conf) * 100,
        2
    )
    quality_score = min(
        100,
        round(confidence * 0.9)
    )
    PRICE_TABLE = {
        "Granit": 1800,
        "Bazalt": 1200,
        "Kuvars": 8000,
        "Kalker": 600,
        "Mermer": 5000
    }

    base_price = PRICE_TABLE.get(
        stone,
        1000
    )

    estimated_price = round(
        base_price *
        (quality_score / 100),
        0
    )
    info = STONE_DATABASE[stone]

    return {
        "stone": stone,
        "confidence": confidence,
        "hardness": info["hardness"],
        "value": info["value"],
        "usage": info["usage"],
        "description": info["description"]
        "quality_score": quality_score,
        "estimated_price": estimated_price,
    }