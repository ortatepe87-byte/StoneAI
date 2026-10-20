import os


class DatasetStats:

    @staticmethod
    def count_images(folder):

        if not os.path.exists(folder):
            return 0

        return len([
            f for f in os.listdir(folder)
            if f.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ])

    @staticmethod
    def get_stats():

        classes = [
            "granit",
            "bazalt",
            "kuvars",
            "kalker",
            "mermer",
            "bilinmeyen"
        ]

        stats = {}

        total = 0

        for cls in classes:

            count = DatasetStats.count_images(
                f"data/{cls}"
            )

            stats[cls] = count

            total += count

        stats["total"] = total

        return stats