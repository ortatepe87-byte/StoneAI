from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
import tempfile

app = FastAPI()

model = YOLO("models/stone_v1.pt")

STONE_DATABASE = {
    "Granit": {
        "hardness": "6-7",
        "value": "Orta",
        "usage": "Yapı taşı, mezar taşı, mutfak tezgahı",
        "description": "Magmatik kökenli çok dayanıklı kayaç."
    },
    "Bazalt": {
        "hardness": "6",
        "value": "Orta",
        "usage": "Yol yapımı, parke taşı, inşaat",
        "description": "Volkanik kökenli koyu renkli kayaç."
    },
    "Kuvars": {
        "hardness": "7",
        "value": "Orta-Yüksek",
        "usage": "Cam, elektronik, takı",
        "description": "Yüksek silis oranına sahip sert mineral."
    },
    "Kalker": {
        "hardness": "3",
        "value": "Düşük",
        "usage": "Çimento, kireç, yapı malzemesi",
        "description": "Sedimanter kökenli kalsiyum karbonat kayaç."
    },
    "Mermer": {
        "hardness": "3-4",
        "value": "Yüksek",
        "usage": "Kaplama, dekorasyon, heykel",
        "description": "Metamorfik kökenli dekoratif kayaç."
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

    info = STONE_DATABASE[stone]

    return {
        "stone": stone,
        "confidence": confidence,
        "hardness": info["hardness"],
        "value": info["value"],
        "usage": info["usage"],
        "description": info["description"]
    }