from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import tempfile

app = FastAPI()

model = YOLO("models/stone_v1.pt")

STONE_DATABASE = {
    "Granit": {
        "hardness": "6-7",
        "value": "5 - 30 TL",
        "rarity": "Dusuk",
        "usage": "Yapi tasi, mezar tasi, mutfak tezgahi",
        "description": "Magmatik kokenli cok dayanikli kayac."
    },

    "Bazalt": {
        "hardness": "6",
        "value": "3 - 25 TL",
        "rarity": "Dusuk",
        "usage": "Yol yapimi, parke tasi, insaat",
        "description": "Volkanik kokenli koyu renkli kayac."
    },

    "Kuvars": {
        "hardness": "7",
        "value": "50 - 500 TL",
        "rarity": "Yuksek",
        "usage": "Cam, elektronik, taki",
        "description": "Yuksek silis oranina sahip sert mineral."
    },

    "Kalker": {
        "hardness": "3",
        "value": "1 - 15 TL",
        "rarity": "Dusuk",
        "usage": "Cimento, kirec, yapi malzemesi",
        "description": "Sedimanter kokenli kalsiyum karbonat kayac."
    },

    "Mermer": {
        "hardness": "3-4",
        "value": "20 - 250 TL",
        "rarity": "Orta",
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

    info = STONE_DATABASE[stone]

    return {
        "stone": stone,
        "confidence": confidence,
        "hardness": info["hardness"],
        "value": info["value"],
        "rarity": info["rarity"],
        "usage": info["usage"],
        "description": info["description"],
        "quality_score": quality_score
    }