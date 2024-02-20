import openGB.polynomials as polys
import openGB.ideals as ideals

import numpy as np

vars = ["x","y","z"]
poly1 = polys.polyFromExpression("x^3 - y^3", const="0", vars=vars)
poly2 = polys.polyFromExpression("x-y", vars=vars)
print(poly1)
print(poly2)

print("Setting up an ideal test")
id1 = ideals.Ideal([poly1,poly2], order=poly1.order, vars=vars)
print(id1)

print("Sorting test")
id1.sort()
print(id1)

print("InTerms test")
print([str(inTerm) for inTerm in id1.getInTerms()])

print("Poly Combs test")
print(id1)
p1=polys.polyFromExpression("x+y", vars=vars)
p2=polys.polyFromExpression("y", const="2", vars=vars)
print("coefs: ", p1,", ", p2)
print("result:",id1.getComb([p1, p2]))

print("Reduction test")
p1 = polys.polyFromExpression("x^2-y", vars=vars)
print(id1.baseReduce(p1))

