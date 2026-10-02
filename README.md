Laboratory Exercise 5: Object-Oriented Spatial Modeling with UML  
-----------------------------------------------------------------
Part A: Project setup and reproducible environment  
 - A directory for diagram, output, src, and tests are created.
 - gitignore, README.md, requirements.txt and pytest.ini is created.
 - Under the src, assessment.py, demo.py, rules.py, run_lab.py and spatial.py is created.
 - Under the tests, test_assessment.py, test_rules.py and test_spatial.py  
 - https://github.com/jsppr1147/gme205-lab5-Molleno.git is the repository.  

 Part B: OOAD Case Study: Parcel Development Assessment.
- This part shows how I breakdown the problem before creating the UML and the programming code itself.  
- From the problem statement, i extracted the candidate nouns and verbs to figure out what classes to make and to which do they belong. 
- This is the PROBLEM STATEMENT from my understanding.  

"The planning team needs a program that checks a parcel against several independent development rules. Each parcel has an ID, a geometry, a zone, and an area in sqm. Version 1 has three rules: minimum area, allowed zones, and no overlap with a mapped hazard zone. Every rule returns the same kind of result (rule name, pass/fail, short explanation). One assessment runs all the rules and gives a report. Later rules, such as road access, must be addable without rewriting the assessment loop."   

- I have attached a snap shot of the tables i used in my candidate nouns and candidate verbs and my rationale for putting it there.  
- The candidate noun for assessment rule shows the abstraction and polymorphism requried for this exercise since you can call a rule.screen(parcel) to evaluate the parcels based on rules depending on which object is running it.  
- Apart from the given in the lab manual, i added some candidate nouns like the "zoning classification" or "parcel assessment".  

Part C: Building the UML Model Step by Step  
- Based from the Part B tables created, the UML model is created one by one. 
- As for the relationships:
    1. the 3 rules "IS AN" AssessmentRule. It shows an inheritance type of relationship and Hollow Triangle symbol.  
    2. ParcelAssessment "Has A" Parcel. This shows the composition type of relationship. uses a Solid diamond symbol. It has a multiplicity symbol of 1 because it "HAS EXACTLY 1" parcel.  
    3. ParcelAssessment also "Has AN" AssessmentRule. Solid diamond symbol. However it has a "1..*" symbol which indicate that it must hold at least 1 rule to run, but it can also hold a lsit of many rules.  
    4. NoHazardOverlapRule "Has A" HazardZone. This shows a association type of relationship. Uses a plain line since the hazard exists independently of the rule. Also with multiplicity of 1 since it uses 1 hazard.  
    5. AssessmentRule "Uses A" RuleResults. this is a dependancy type of relationship. Uses a dashed arrow with no multiplicity value but there is a label 'returns' since it simply create and returns results but it doesnt store them. 
- A UML diagram was created based on Part B and the relationships mentioned.  

Part D: Forward Engineering: Convert the UML to Python
- This is the part where the design is translated in to a python code. 
- The laboratory manual already given the first few class structures for this part. 
- The HazardZone, AllowedZoneRule, and NoHazardOverlapRule were created based on the template of the MinimumAreaRule given in the laboratory exercise manual.  
- The spatial.py and rules.py were updated according to the parts objectives. 

Moving forward to Part E: Showing the Four Pillars in the Converted Code  
- After translating the design into code, it is important to show also the four pillar in OOP: the encapsulation, Abstraction, Inheritance, and Polymorphism.
- Part D already showed the encapsulation in the Parcel and HazardZone classes.
- Part D already showed the Abstraction in the AssessmentRule Class in rules.py.  
- Part D already showed the Inheritance in the 3 rules in the rules.py
- Part E now is tasked to implement the polymorphism to completely showcase the four pillars in OOP.
- The ParcelAssessment class in the assessment.py loop showcases polymorphism and composition relationship to the Parcel and Assessment Rule. 

Part F: Running a fix spatial scenario.
- For this part, I created the runner script for the verification if the model works properly.
- A shared scenario for the parcel A, parcel B, and HazardZone was created to test if the algorithm works.
- asdict(r) turns the RuleResult dataclass into a plain dict with exactly the keys the required JSON shape asks for (rule_name, passed, message)
- The Shapely geometry also never enters the JSON. Only the id, booleans, and the strings do.
- There's also no visible responsibility leaks like there are no "DECISION" logic (i.e. area > 5000) showing in the runner script.
- One rule list is also shared by both parcels since the rules only hold the configuration (threshold, zoneset, hazard ) and no parcel state.
- Upon checking, using the scenario from the manual yields the P-001 as passed: false and P-002 as passed : true  

Part G: UML-to-Code Consistency Review  
- For this part, the diagram was compared again to the current version of the code.
- First is checking if all the UML class exists: 
    - spatial.py: has the Parcel and HazardZone classes : check!
    - rules.py: has Abstract(AssessmentRule), 3 rules, and RuleResult : check!
    - assessment.py: has the ParcelAssessment: check!
- All classes in UML exist.
- Second is to check if the __init__ or attributes sit right in their respective classes:
    - all good and it is not displayed in demo.py and runner_lab5.py
- Third is to check if the operations in each class match:
    - intersects in Parcel : check!
    - evaluate in each rule : check!
    - passed in ParcelAssessment : check!
- Fourth is to check if the Inheritance is matching properly:
    - 3 rules (AssessmentRule) : check!
- Fifth is to check if Composition is matching properly:
    - ParcelAssessment.__init__ gets the self.parcel and self.rules : check!
- Sixth is the Multiplicity listed if it match:
    - "if not rules : raise ValueError" : check!
- Lastly for the polymorphism if properly displayed:
    - in ParcelAssessment.evaluate, it calls the rule.evaluate(self.parcel) without the isinstance.

Part H: Testing the Model, Not Just the Output 
- similar to the previos lab exercise, the test were created to verify if the UML and interfaces were working as intended.
- test_spatial.py employs 7 tests:
    1. for exposing valid state: passed
    2. for rejecting invalid input (no id): passed
    3. for rejecting invalid input (no zone): passed
    4. for rejecting invalid input (zero area): passed
    5. for rejecting invalid input (negative area): passed
    6. for checking if parcel intersects delegate to geometry: passed
    7. for testing if hazard zone stores state and rejects missing id: passed  
- test_rules.py employs 6 tests:
    1. for rule not be instantiated: passed 
    2. for minimum area passing and failing: passed
    3. for allowed zone accepting and rejecting: passed
    4. for allowed zone rejecting empty set: passed
    5. for no hazard overlap fails when intersecting: passed
    6. for no hazard overlap passing when apart: passed 
- test_assessment.py employs 4 tests:
    1. for accepting mixed rule subclasses: passed
    2. for assessment requiring at least 1 rule: passed
    3. for p001 failing only in hazard rule: passed #scenario specific
    4. for p002 passing all rules: passed

- test_spatial.py protects the encapsulation, meaning that invalid parcels can't exist.
- test_rules.py to check that each rule work on its own.
- test_assessment.py to protect the coordinator (ParcelAssessment) and polymorphism. the placed isinstance in this code checks the results shape and doesnt choose a rule implementation.

Part I: Adding the required extension (RoadAccessRule)
- Before adding the RoadAccessRule and the Road class, the UML for these classes were created. The UMLdiagram_v0 was updated to UMLdiagram_v1.
- UMLdiagram_v1 shows that the RoadAccessRule "IS AN" AssessmentRule. It shows an inheritance type of relationship and Hollow Triangle symbol.
- It also shows that the RoadAccessRule "Has A" Road. This shows a association type of relationship. Uses a plain line too since the road exists independently of the rule. Also with multiplicity of 1 since it uses 1 road.
- I didn't remove the v0 to simply show the change in the current commit. will remove if necessary.
- Then i translated the UML similar to the steps before. Road was created under the spatial.py and RoadAccessRule was added to rules.py
- I checked if it works by adding the rule in the demo.py (added Road scenario for a near and far road).
- Updated the runner script to include the Road scenario and RoadAccessRule.
- Updated test_rules.py for checking if RoadAccessRule passes when it's close and failing when it's far.
- Updated test_assessment.py for checking if the new rule shows polymorphism too.
- the tests updates both passed.

Short section: Extension without coordinator rewrite
- Before: 3 rules: (in demo.py before)  
rules = [
    MinimumAreaRule(300),
    AllowedZoneRule({"Residential"}),
    NoHazardOverlapRule(hazard),
    ]
- Now: 4 rules (in demo.py current)  
rules = [
    MinimumAreaRule(300), 
    AllowedZoneRule({"Residential"}), 
    NoHazardOverlapRule(hazard),
    RoadAccessRule(near_road, 10),
    ]  
- ParcelAssessment is unchanged. (in assessment.py)
def evaluate(self): 
    results = [] 
    for rule in self._rules: 
        result = rule.evaluate(self._parcel) 
        results.append(result) 
    return results 

- Why this is different from adding an elif branch?:
The coordinator only calls rule.evaluate(parcel), which is the contract defined by AssessmentRule. It doesn't need to know what kind of rule it holds, so a new rule that honors the contract works with no changes to the loop. Only the code that creates the rule (the runner) knows RoadAccessRule exists.

- Explain why this is a "WEAK" alternative.

if rule_type == "minimum_area":   
...   
elif rule_type == "allowed_zone":   
...   
elif rule_type == "hazard_overlap":   
...   
elif rule_type == "road_access":   
...  # every new type edits the coordinator again    
  
With this design the coordinator must know every rule type. Each new rule means editing code that already works, which risks breaking the existing rules, and the if/elif chain grows with every rule. The polymorphic design extends the model by adding a class instead of modifying the loop.  
  

Part J: ReadME Reflections

1. OOAD: what changed in my thinking when I modeled first?  
I used to start by writing code and fixing the structure as I went (like writing it on the go, listing all methods then trial and erro like a prcedural workflow). Breaking the problem statement into nouns and verbs first showed me which things deserve to be classes and which object should own each action. For example, passed() belongs in ParcelAssessment because only it sees all the results. Deciding this on paper was a bit easier than discovering it while coding.

2. Candidate classes: a noun I did not make a class.  
Zoning classification. It is only a value a parcel carries (a string such as "Residential"), with no behavior or identity of its own, so it is an attribute of Parcel. I also kept "report" as a plain dictionary/JSON instead of a class, since it owns no behavior.

3. Encapsulation.  
Parcel keeps parcel_id, zone, area_sqm, and geometry in private attributes, exposed only through read-only properties. The constructor prevents a missing ID, a blank zone, and a non-positive area, so an invalid parcel can never exist.

4. Abstraction.  
AssessmentRule promises that every rule has a name and an evaluate(parcel) method that returns a RuleResult. It says nothing about how any particular rule decides.  

5. Inheritance.  
The concrete rules share the base class' constructor, which stores the name, and the name property. They also share the contract of evaluate(parcel) returning a RuleResult. Each subclass adds only its own configuration (a threshold, a zone set, or a hazard zone) and its own decision logic.  

6. Polymorphism.  
ParcelAssessment calls rule.evaluate(self._parcel) on every rule through the base-class contract. Every concrete rule fulfils that contract, so the coordinator doesn't need to know which kind of rule it has. Each object responds with its own behavior.  

7. Composition.  
A ParcelAssessment is not a parcel and is not a rule. It *uses* one parcel and a list of rules, so it stores them as members (has-a). Inheriting would claim a relationship that isn't true and would lock the design into one parcel and one rule type. Composition also lets me swap parcels and rule lists freely.  

8. Extension.  
I added a Road class and a RoadAccessRule (a new subclass), and added one new object to the rules list. I did not change ParcelAssessment.evaluate() or any of the existing rules.  

9. UML-to-code consistency.  
When I wasn't sure where passed() should live, i just based it on my diagram: the overall decision needs all results, so it appears in the ParcelAssessment box and not in AssessmentRule. The code was brought in line with that placement.  