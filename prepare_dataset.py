import os
import random
import shutil

CLASSES = [
    "granit",
    "bazalt",
    "kuvars",
    "kalker",
    "mermer"
]

for cls in CLASSES:

    source = os.path.join("data", cls)

    files = [
        f for f in os.listdir(source)
        if f.lower().endswith(
            (".jpg", ".jpeg", ".png")
        )
    ]

    random.shuffle(files)

    split = int(len(files) * 0.8)

    train_files = files[:split]
    val_files = files[split:]

    for f in train_files:

        shutil.copy(
            os.path.join(source, f),
            os.path.join(
                "dataset",
                "train",
                cls,
                f
            )
        )

    for f in val_files:

        shutil.copy(
            os.path.join(source, f),
            os.path.join(
                "dataset",
                "val",
                cls,
                f
            )
        )

print("DATASET HAZIR")