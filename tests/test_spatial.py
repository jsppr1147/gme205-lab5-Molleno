import pytest
from shapely.geometry import box
from spatial import Parcel, HazardZone


def test_parcel_exposes_valid_state():
    geom = box(0, 0, 10, 10)
    p = Parcel("P-1", geom, "Residential", 100)
    assert p.parcel_id == "P-1"
    assert p.zone == "Residential"
    assert p.area_sqm == 100.0
    assert p.geometry is geom


@pytest.mark.parametrize("pid, zone, area", [
    ("", "Residential", 100),    # missing ID
    ("P-1", "", 100),            # blank zone
    ("P-1", "Residential", 0),   # zero area
    ("P-1", "Residential", -5),  # negative area
])
def test_parcel_rejects_invalid_input(pid, zone, area):
    with pytest.raises(ValueError):
        Parcel(pid, box(0, 0, 10, 10), zone, area)


def test_parcel_intersects_delegates_to_geometry():
    parcel = Parcel("P-1", box(0, 0, 10, 10), "Residential", 100)
    overlapping = HazardZone("H-1", box(5, 5, 15, 15), "Flood", "High")
    far_away = HazardZone("H-2", box(50, 50, 60, 60), "Flood", "High")
    assert parcel.intersects(overlapping)
    assert not parcel.intersects(far_away)


def test_hazard_zone_stores_state_and_rejects_missing_id():
    hz = HazardZone("H-1", box(0, 0, 1, 1), "Flood", "High")
    assert hz.zone_id == "H-1"
    assert hz.hazard_type == "Flood"
    assert hz.severity == "High"
    with pytest.raises(ValueError):
        HazardZone("", box(0, 0, 1, 1), "Flood", "High")