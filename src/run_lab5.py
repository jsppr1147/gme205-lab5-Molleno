"""Thin runner: builds objects, runs them, writes JSON. No rule logic here."""
import json
from dataclasses import asdict
from pathlib import Path

from shapely.geometry import box, LineString

from spatial import Parcel, HazardZone, Road
from rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule, RoadAccessRule
from assessment import ParcelAssessment


def main():
    # 1. spatial objects
    parcel_a = Parcel("P-001", box(0, 0, 80, 90), "Residential", 7200)
    parcel_b = Parcel("P-002", box(120, 0, 190, 80), "Commercial", 5600)
    hazard = HazardZone("HZ-01", box(60, 50, 110, 100), "Flood", "High")
    road = Road("R-01", LineString([(0, -10), (190, -10)])) #updated spatial objects to include a road for the RoadAccessRule

    # 2. rule objects (stateless, so one list can serve every parcel)
    rules = [
        MinimumAreaRule(5000),
        AllowedZoneRule({"Residential", "Commercial"}),
        NoHazardOverlapRule(hazard),
        RoadAccessRule(road, 20),  # added RoadAccessRule to the rules list
    ]

    # 3-5. compose, evaluate, assemble JSON-ready dicts
    report = {"scenario": "parcel-development-assessment", "parcels": []}
    for parcel in (parcel_a, parcel_b):
        assessment = ParcelAssessment(parcel, rules)
        report["parcels"].append({
            "parcel_id": parcel.parcel_id,
            "passed": assessment.passed(),
            "results": [asdict(r) for r in assessment.evaluate()],
        })

    # 6. write output/lab5_report.json
    out_dir = Path(__file__).resolve().parent.parent / "output"
    out_dir.mkdir(exist_ok=True)
    out_file = out_dir / "lab5_report.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"Wrote {out_file}")


if __name__ == "__main__":
    main()