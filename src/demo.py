from shapely.geometry import box
from spatial import Parcel, HazardZone
from rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule
from assessment import ParcelAssessment

parcel = Parcel("P-001", box(0, 0, 20, 20), "Residential", 400)
hazard = HazardZone("H-01", box(15, 15, 30, 30), "Flood", "High") #should throw an error because the parcel intersects with the hazard zone

rules = [MinimumAreaRule(300), AllowedZoneRule({"Residential"}), NoHazardOverlapRule(hazard)]
assessment = ParcelAssessment(parcel, rules)

for r in assessment.evaluate():
    print(r)
print("Overall:", assessment.passed())