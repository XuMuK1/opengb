import openGB.polynomials as polys

vars = ["x","y","z"]
poly1 = polys.polyFromExpression("2.4x^2y^3z -z^2x + yx", const="5", vars=vars)
print(poly1)

print("MONOMIALS")
print([ str(mon) for mon in poly1.monomials])
print([ mon.coef for mon in poly1.monomials])
print([ mon.deg for mon in poly1.monomials])