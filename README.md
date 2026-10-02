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