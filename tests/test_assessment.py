import pytest
from shapely.geometry import box, LineString
from spatial import Parcel, HazardZone, Road
from rules import (RuleResult, MinimumAreaRule, AllowedZoneRule, RoadAccessRule,
                   NoHazardOverlapRule)
from assessment import ParcelAssessment


@pytest.fixture
def scenario():
    parcel_a = Parcel("P-001", box(0, 0, 80, 90), "Residential", 7200)
    parcel_b = Parcel("P-002", box(120, 0, 190, 80), "Commercial", 5600)
    hazard = HazardZone("HZ-01", box(60, 50, 110, 100), "Flood", "High")
    rules = [
        MinimumAreaRule(5000),
        AllowedZoneRule({"Residential", "Commercial"}),
        NoHazardOverlapRule(hazard),
    ]
    return parcel_a, parcel_b, rules


def test_assessment_accepts_mixed_rule_subclasses(scenario):
    _, parcel_b, rules = scenario
    results = ParcelAssessment(parcel_b, rules).evaluate()
    assert len(results) == 3
    assert all(isinstance(r, RuleResult) for r in results)


def test_assessment_requires_at_least_one_rule(scenario):
    parcel_a, _, _ = scenario
    with pytest.raises(ValueError):
        ParcelAssessment(parcel_a, [])


def test_p001_fails_only_hazard_rule(scenario):
    parcel_a, _, rules = scenario
    assessment = ParcelAssessment(parcel_a, rules)
    failed = [r.rule_name for r in assessment.evaluate() if not r.passed]
    assert failed == ["No hazard overlap"]
    assert not assessment.passed()


def test_p002_passes_all_rules(scenario):
    _, parcel_b, rules = scenario
    assessment = ParcelAssessment(parcel_b, rules)
    assert all(r.passed for r in assessment.evaluate())
    assert assessment.passed()

def test_assessment_handles_new_rule_without_changes(scenario):
    parcel_a, _, rules = scenario
    road = Road("R-1", LineString([(0, -10), (190, -10)]))
    extended = rules + [RoadAccessRule(road, 20)]
    results = ParcelAssessment(parcel_a, extended).evaluate()
    assert len(results) == 4