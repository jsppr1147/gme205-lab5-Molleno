from abc import ABC, abstractmethod 
from dataclasses import dataclass 
 
@dataclass(frozen=True) 
class RuleResult:
    '''Translation for RuleResult: This data class represents the result of evaluating an assessment rule. 
    It contains the name of the rule, a boolean indicating whether the rule passed or failed, 
    and a message providing additional context or information about the evaluation.''' 
    rule_name: str 
    passed: bool 
    message: str 
 
class AssessmentRule(ABC):
    '''Translation for AssessmentRule: This is an abstract base class that defines the structure for assessment rules. 
    It requires subclasses to implement the evaluate method, which assesses a given parcel and returns a RuleResult 
    indicating whether the rule passed or failed, along with a message.'''
    def __init__(self, name: str): 
        self._name = name 
 
    @property 
    def name(self) -> str: 
        return self._name 
 
    @abstractmethod 
    def evaluate(self, parcel) -> RuleResult: 
        pass



class MinimumAreaRule(AssessmentRule): 
    def __init__(self, min_area): 
        super().__init__("Minimum parcel area") 
        self._min_area = float(min_area) 
 
    def evaluate(self, parcel): 
        passed = parcel.area_sqm >= self._min_area 
        message = ( 
            f"{parcel.area_sqm:.0f} m² >= {self._min_area:.0f} m²" 
            if passed 
            else f"{parcel.area_sqm:.0f} m² < {self._min_area:.0f} m²" 
        ) 
        return RuleResult(self.name, passed, message)


class AllowedZoneRule(AssessmentRule):
    def __init__(self, allowed_zones):
        super().__init__("Allowed zone")
        self._allowed_zones = set(allowed_zones)
        if not self._allowed_zones:
            raise ValueError("allowed_zones cannot be empty")

    def evaluate(self, parcel):
        passed = parcel.zone in self._allowed_zones
        message = (
            f"Zone {parcel.zone} is allowed"
            if passed
            else f"Zone {parcel.zone} not in {sorted(self._allowed_zones)}"
        )
        return RuleResult(self.name, passed, message)