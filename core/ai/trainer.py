import os


class Trainer:

    @staticmethod
    def dataset_health():

        classes = [
            "granit",
            "bazalt",
            "kuvars",
            "kalker",
            "mermer"
        ]

        counts = {}

        total = 0

        for cls in classes:

            path = os.path.join(
                "data",
                cls
            )

            count = len([
                f for f in os.listdir(path)
                if f.lower().endswith(
                    (".jpg", ".jpeg", ".png")
                )
            ])

            counts[cls] = count

            total += count

        score = min(
            int((total / 500) * 100),
            100
        )

        return score, counts