class ParcelAssessment: 
    def __init__(self, parcel, rules): 
        if not rules: 
            raise ValueError("At least one rule is required") 
        self._parcel = parcel 
        self._rules = list(rules) 
 
    def evaluate(self): 
        results = [] 
        for rule in self._rules: 
            result = rule.evaluate(self._parcel) 
            results.append(result) 
        return results 

    def passed(self): #cleaner returns true if all rules passed, false at the first failure
        return all(result.passed for result in self.evaluate())