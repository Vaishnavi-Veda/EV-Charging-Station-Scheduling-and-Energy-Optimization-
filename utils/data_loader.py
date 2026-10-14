import csv
from pathlib import Path


def load_parking_data(
    file_path: str = "C:\\Users\\yoshi\\Downloads\\IIoT_Smart_Parking_Management.xlsx",
) -> list[dict[str, str]]:
    """Load parking data from CSV."""

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


if __name__ == "__main__":
    data = load_parking_data()

    print("=" * 50)
    print("SMART PARKING DATASET")
    print("=" * 50)
    print(f"Total records: {len(data)}")

    for row in data[:5]:
        print(
            row["parking_id"],
            row["spot_id"],
            row["vehicle_type"],
            row["occupancy_status"],
        )