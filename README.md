Laboratory Exercise 5: Object-Oriented Spatial Modeling with UML  
-----------------------------------------------------------------
Part A: Project setup and reproducible environment
 -A directory for diagram, output, src, and tests are created.
 -gitignore, README.md, requirements.txt and pytest.ini is created.
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
- apart from the given in the lab manual, i added some candidate nouns like the "zoning classification" or "parcel assessment".  
