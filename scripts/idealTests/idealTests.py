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
print("Ideal ", id1)
p1 = polys.polyFromExpression("x^2-y", vars=vars)
print(id1.baseReduce(p1))

print("Spolys test")
poly3 = polys.polyFromExpression("xy -y", vars=vars)
id2 = ideals.Ideal([poly1,poly2,poly3], order=poly1.order, vars=vars)
print("Ideal ", id2)
inds = [(0,1),(0,2),(1,2)]
spolys = id2.genSPolys(inds)
for i in np.arange(len(spolys)):
    print(f"S({inds[i][0]},{inds[i][1]})=",spolys[i])

print("GB Check")
print(id2.checkGB())
print()
spolys = id2.genSPolys(inds)
print("Reduction results:")
for i in np.arange(len(spolys)):
    print(f"S({inds[i][0]},{inds[i][1]})->",id2.baseReduce(spolys[i],debugVerbose=True) )
