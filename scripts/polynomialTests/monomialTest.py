import numpy as np
import openGB.polynomials as polys

vars = ["x","y","z"]
monom1 = polys.Monomial(deg=np.array([1,2,0],dtype="int32"), coef=1, vars=vars)
monom11 = polys.Monomial(deg=np.array([1,2,0],dtype="int32"), coef=3, vars=vars)
monom2 = polys.Monomial(deg=np.array([2,3,0],dtype="int32"), coef=2, vars=vars)
monom3 = polys.Monomial(deg=np.array([0,3,0],dtype="int32"), coef=2, vars=vars)

print("__str__ TEST")
print("monom1:", monom1)
print("monom11:", monom11)
print("monom2:", monom2)

print("degree() TEST")
print("deg(monom1)=",monom1.degree())
print("deg(monom2)=",monom2.degree())

print("__call__ TEST")
print("x=1,y=2; monom1=",monom1(np.array([1,2])))
print("x=1,y=2; monom2=",monom2(np.array([1,2])))


print("__add__ TEST")
print("monom1+monom11=",monom1 + monom11)
print("monom2+monom11=",monom2 + monom11)

print("__sub__ TEST")
print("monom1-monom11=",monom1 - monom11)
print("monom2-monom11=",monom2 - monom11)

print("__mul__ TEST")
print("monom1*monom11=",monom1*monom11)
print("monom2*monom11=",monom2*monom11)


print("LexOrder TEST")
print("monom1:", monom1)
print("monom11:", monom11)
print("monom2:", monom2)
print("monom3:", monom3)
print("monom1==monom11=",monom1==monom11)
print("monom2>monom11=",monom2>monom11)
print("monom1<monom11=",monom1<monom11)
print("monom2>=monom11=",monom2>=monom11)
print("monom1<=monom11=",monom1<=monom11)
print("monom1==monom3=",monom1==monom3)
print("monom2>monom3=",monom2>monom3)
print("monom1<monom3=",monom1<monom3)
print("monom2>=monom3=",monom2>=monom3)
print("monom1<=monom3=",monom1<=monom3)