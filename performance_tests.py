import time
import pandas as pd

DATA_FILE = "data/parking_data.csv"
RESULT_FILE = "data/performance_results.csv"

data = pd.read_csv(DATA_FILE)

print("=" * 60)
print("SMART PARKING SYSTEM PERFORMANCE TEST")
print("=" * 60)
print("Total records :", len(data))
print("Total columns :", len(data.columns))
print()

results = []

for size in [100, 250, 500, 750, 1000]:

    test_data = data.head(size)

    start = time.perf_counter()
    test_data.copy()
    parking_time = time.perf_counter() - start

    start = time.perf_counter()
    test_data.iloc[0]
    search_time = time.perf_counter() - start

    start = time.perf_counter()
    test_data.select_dtypes(include="number").mean()
    occupancy_time = time.perf_counter() - start

    total_time = parking_time + search_time + occupancy_time

    results.append({
        "Records": size,
        "Parking_Time_ms": parking_time * 1000,
        "Search_Time_ms": search_time * 1000,
        "Occupancy_Time_ms": occupancy_time * 1000,
        "Total_Time_ms": total_time * 1000
    })

    print(
        f"{size} records | "
        f"Parking: {parking_time * 1000:.4f} ms | "
        f"Search: {search_time * 1000:.4f} ms | "
        f"Occupancy: {occupancy_time * 1000:.4f} ms | "
        f"Total: {total_time * 1000:.4f} ms"
    )

pd.DataFrame(results).to_csv(
    RESULT_FILE,
    index=False
)

print()
print("Performance results saved to:", RESULT_FILE)