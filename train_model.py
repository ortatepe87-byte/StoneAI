from ultralytics import YOLO

model = YOLO("yolo11n-cls.pt")

model.train(
    data="dataset",
    epochs=50,
    imgsz=224,
    batch=16
)