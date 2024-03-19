import openGB.polynomials as polys
import openGB.ideals as ideals

import numpy as np

import time

import galois

#-----------------------------var5
#1
print("**********************Problem 1************************")
vars = ["x"]
GF = galois.GF(5)
poly1 = polys.polyFromExpression("x^2+3x ", const="2", vars=vars,coefConstructor=polys.GFpConstructor, GF = GF)
poly2 = polys.polyFromExpression("x^2  ", const="1", vars=vars,coefConstructor=polys.GFpConstructor, GF = GF)
easyId = ideals.Ideal([poly2,poly1], order=poly1.order, vars=vars)

print([str(mon) for mon in poly1.monomials])
print([str(mon) for mon in poly2.monomials])


print(easyId)
print("*********")
print(easyId.checkGB())
print(easyId.existsIntersection(poly1,poly2))
easyId.computeGB(debugVerbose=False,minGB=True)
print("GB Result")
print(easyId)

print("Result:",easyId.baseReduce(poly1))