import numpy as np
import openGB.polynomials as polys

vars = ["x","y","z"]
monom1 = -polys.Monomial(deg=np.array([1,2,0],dtype="int32"), coef=1, vars=vars)
monom11 = polys.Monomial(deg=np.array([1,2,0],dtype="int32"), coef=3, vars=vars)
monom2 = -polys.Monomial(deg=np.array([2,3,0],dtype="int32"), coef=2, vars=vars)
monom3 = polys.Monomial(deg=np.array([0,3,0],dtype="int32"), coef=2, vars=vars)

poly1 = polys.Polynomial([monom1,monom2], vars = vars)
poly2 = polys.Polynomial([monom1,monom3, monom2], vars = vars)
poly3 = polys.Polynomial([monom3], vars = vars)

print("__str__ TEST")
print("poly1:", poly1)
print("poly2:",poly2)
print("poly3:", poly3)

print("degree() TEST")
print("poly1:", poly1.degree())
print("poly2:",poly2.degree())
print("poly3:", poly3.degree())

print("sort TEST")
poly1.sort()
poly2.sort()
poly3.sort()
print("poly1:", poly1)
print("poly2:",poly2)
print("poly3:", poly3)
#todo

print("__call__ TEST")
print("x=1,y=2; poly1=",poly1(np.array([1,2])))
print("x=1,y=2; poly2=",poly2(np.array([1,2])))
print("x=1,y=2; poly3=",poly3(np.array([1,2])))


print("__add__ TEST")
#todo

print("__sub__ TEST")
#todo

print("__mul__ TEST")
#todo

