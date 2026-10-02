import pytest
from shapely.geometry import box
from spatial import Parcel, HazardZone
from rules import (RuleResult, AssessmentRule, MinimumAreaRule,
                   AllowedZoneRule, NoHazardOverlapRule)


@pytest.fixture
def parcel():
    return Parcel("P-1", box(0, 0, 10, 10), "Residential", 100)


def test_assessment_rule_cannot_be_instantiated():
    with pytest.raises(TypeError):
        AssessmentRule("x")


def test_minimum_area_passes_and_fails(parcel):
    ok = MinimumAreaRule(50).evaluate(parcel)
    bad = MinimumAreaRule(500).evaluate(parcel)
    assert isinstance(ok, RuleResult) and ok.passed
    assert isinstance(bad, RuleResult) and not bad.passed


def test_allowed_zone_accepts_and_rejects(parcel):
    assert AllowedZoneRule({"Residential"}).evaluate(parcel).passed
    assert not AllowedZoneRule({"Commercial"}).evaluate(parcel).passed


def test_allowed_zone_rejects_empty_set():
    with pytest.raises(ValueError):
        AllowedZoneRule(set())


def test_no_hazard_overlap_fails_when_intersecting(parcel):
    hazard = HazardZone("H-1", box(5, 5, 15, 15), "Flood", "High")
    assert not NoHazardOverlapRule(hazard).evaluate(parcel).passed


def test_no_hazard_overlap_passes_when_apart(parcel):
    hazard = HazardZone("H-2", box(50, 50, 60, 60), "Flood", "High")
    assert NoHazardOverlapRule(hazard).evaluate(parcel).passed