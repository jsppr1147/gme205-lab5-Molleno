from shapely.geometry import box, LineString
from spatial import Parcel, HazardZone, Road
from rules import MinimumAreaRule, AllowedZoneRule, NoHazardOverlapRule, RoadAccessRule
from assessment import ParcelAssessment

parcel = Parcel("P-001", box(0, 0, 20, 20), "Residential", 400)
hazard = HazardZone("H-01", box(15, 15, 30, 30), "Flood", "High") #should throw an error because the parcel intersects with the hazard zone
near_road = Road("R-near", LineString([(0, -5), (20, -5)]))    # 5 units from the parcel
far_road = Road("R-far", LineString([(0, -50), (20, -50)]))    # 50 units from the parcel

print("--- Road rule alone (max distance 10) ---")
print(RoadAccessRule(near_road, 10).evaluate(parcel))   # expect passed=True
print(RoadAccessRule(far_road, 10).evaluate(parcel))    # expect passed=False

rules = [MinimumAreaRule(300), 
         AllowedZoneRule({"Residential"}), 
         NoHazardOverlapRule(hazard),
         RoadAccessRule(near_road, 10),] #Updated rules (before 3, current 4)



assessment = ParcelAssessment(parcel, rules)
for r in assessment.evaluate():
    print(r)
print("Overall:", assessment.passed())