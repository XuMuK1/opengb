import re

vars = ["x","y","z"]
coefGroup = "([0-9.]*)"
varGroup = "((["+"".join(vars)+"])(\^([0-9]+)){0,1})"
monRE = re.compile( coefGroup+"("+varGroup+"+)|([+-])" )
print(monRE)
opList = monRE.findall("-2x^2 + 3yz^3 + 6z^2y-3z^4x^5y")
print(opList)
monStructs = [ (i,op[0],op[1]) if (not op[0]=="") else (i,op[-1]) for (i,op) in zip(range(len(opList)),opList)]
print(monStructs)


monLowLevelRE = re.compile(varGroup)
monDetails = [(op[1],1 if op[-1]=="" else int(op[-1])) for op in monLowLevelRE.findall(monStructs[-1][-1]) ]
print(monDetails)
#varsRE = re.compile( "["+"".join(vars)+"]+([^][0-9]+){0,1}" )