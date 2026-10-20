from ultralytics import YOLO

model = YOLO("models/stone_v1.pt")

results = model("test.jpg")

print(results[0].probs)