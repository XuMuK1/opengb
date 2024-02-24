import numpy as np
from copy import deepcopy

import re

import fractions

class MonomialOrder:
    
    def __init__(self):
        pass
    
    def compare(self, a, b):
        raise NotImplementedError
        
        
class LexicographicOrder(MonomialOrder):
    
    def __init__(self, vars):
        super(LexicographicOrder,self).__init__()
        self.vars = vars
        
    def compare(self, a, b):
        if(a.deg.shape[0] == b.deg.shape[0]):
            dif = a.deg-b.deg
            res=dif[np.where(dif!=0)[0]]
            if(len(res)==0):
                return 0#eq
            elif(res[0]>0):
                return 1
            elif(res[0]<0):
                return -1
            else:
                return None
            
            
            
class Monomial:
    '''
        A monomial x^deg with deg represented as an integer array
    '''
    def __init__(self, deg, coef, order=None, vars = "xyzwtprsuv"):
        '''
        Parameters

        int[] deg -- a sequence of degrees (np.array)
        float coef -- a coefficient (assumed to be just real for now)
        list(str) vars -- variable literals to use (same size as deg)
        '''
        self.deg = deg 
        self.coef = coef
        self.order = LexicographicOrder(vars) if order is None else order
        self.vars = vars

    #Comparators
    def __eq__(self, other):
        '''
        A comparator x==y
        '''
        return (self.order.compare(self,other)==0)
    def __lt__(self, other):
        '''
        A comparator x<y
        '''
        return (self.order.compare(self,other)<0)
    def __le__(self, other):
        '''
        A comparator x<=y
        '''
        return (self.order.compare(self,other)<=0)
    def __gt__(self, other):
        '''
        A comparator x>y
        '''
        return (self.order.compare(self,other)>0)
    def __ge__(self, other):
        '''
        A comparator x>=y
        '''
        return (self.order.compare(self,other)>=0)

    #Operations
    def __neg__(self):
        return Monomial(deg=self.deg, coef = -self.coef, order=self.order, vars = self.vars)
    def __mul__(self,other):
        '''
        * operation, just adding degrees and multiplying coefs
        '''
        if(self.checkMulCompatibility(other)):
            return Monomial(deg=self.deg+other.deg, coef=self.coef*other.coef,  order=self.order, vars = self.vars)
        else:
            return None
    def __add__(self,other):
        '''
        + operation, just adding coefficients if the degrees are the same
        '''
        if(self.checkAddCompatibility(other)):
            newCoef = (self.coef+other.coef)
            return Monomial(deg=self.deg, coef=newCoef,  order=self.order, vars = self.vars)
        else:
            return Polynomial([deepcopy(self),deepcopy(other)])
    def __sub__(self,other):
        '''
        - operation, just subtracting coefficients if the degrees are the same
        '''
        if(self.checkAddCompatibility(other)):
            newCoef = (self.coef-other.coef)
            return Monomial(deg=self.deg, coef=newCoef,  order=self.order, vars = self.vars)
        else:
            return Polynomial([deepcopy(self),-deepcopy(other)])
    def checkAddCompatibility(self, other):
        '''
        Checks if add can be performed
        '''
        if(len(self.deg)==len(other.deg)):
            return np.all(self.deg==other.deg)
        else:
            return False
    def checkMulCompatibility(self, other):
        '''
        Checks if mul can be performed
        '''
        return (len(self.deg)==len(other.deg))

    #call as a function
    def __call__(self, x):
        '''
        Computes value at point x

        Parameters
        float[] x -- a batch (...,d) of points
        OR
        float[] x -- a point (d,)
        
        Returns
        float res
        OR
        float[] res of shape (<shape>)
        '''
        try:
            if(x.shape[-1]<self.deg.shape[0]):
                x=np.pad(x, (0,self.deg.shape[0]-x.shape[-1]))    
            return self.coef * np.prod(x**self.deg,axis=-1)
        except Exception as e:
            print(e)
            print("Returning as if x was just a number, not array", "x=", x)
            return self.coef * x**self.deg[0]


    def __str__(self):
        '''
        Gives a string representation of the form x^2y
        
        Returns
        str stringRepresentation -- result string
        '''
        return ("" if self.coefIsOne() and np.any(self.deg>0) 
                    else "1" if self.coefIsOne() 
                             else "-" if self.coefIsMOne() 
                                      else str(self.coef)) + \
            "".join([self.vars[i]+ ("^"+str(self.deg[i]) if (self.deg[i])>1 else "")
                        for i in np.arange(len(self.vars)) if self.deg[i]>0])

    def degree(self):
        '''
        Returns 
        int deg -- the degree of the polynomial
        '''
        return np.sum(self.deg)
    
    def isZero(self):
        '''
        Checks if it equals 0, needed for simplification
        
        Returns
        True if 0, False otherwise
        '''
        return np.abs(self.coef)<=1e-15
    
    def coefIsOne(self):
        '''
        Checks if the coef equals one (needed for fancy printing)
        True if coef=1, False otherwise
        '''
        return np.abs(self.coef-1)<=1e-15
    def coefIsMOne(self):
        '''
        Checks if the coef equals one (needed for fancy printing)
        True if coef=1, False otherwise
        '''
        return np.abs(self.coef+1)<=1e-15

    def toPolynomial(self):
        '''
        Gives a Polynomial equivalent of Monomial
        '''
        return Polynomial(monomials=[Monomial(deg=self.deg, coef=self.coef,
                                     order=self.order, vars=self.vars)], order =self.order, vars=self.vars)
        


class Polynomial:
    '''
        A monomial x^deg with deg represented as an integer array
    '''
    def __init__(self, monomials, order=None, vars = "xyzwtprsuv"):
        '''
        Parameters

        Monomial[] -- a sequence of monomials
        MonomialOrder order -- a monomial order
        float coef -- a coefficient (assumed to be just real for now)
        '''
        self.monomials = monomials
        self.order = LexicographicOrder(vars) if order is None else order
        self.vars = vars
        self.sorted=False

    #Comparator eq
    def __eq__(self, other):
        '''
        A comparator x==y
        '''
        pass
    

    #Operations
    def __mul__(self,other):
        '''
        * operation, just adding degrees and multiplying coefs
        '''
        #todo: check same vars exception
        poly2 = Polynomial(monomials= [deepcopy(mon1)*deepcopy(mon2) for mon1 in self.monomials for mon2 in other.monomials],
                           order=self.order, vars=self.vars)
        poly2.simplify()
        return poly2
    def __add__(self,other):
        '''
        + operation, just adding coefficients if the degrees are the same
        '''
        #todo: check same vars exception
        poly2 = Polynomial(monomials=deepcopy(self.monomials) + deepcopy(other.monomials), order=self.order, vars=self.vars)
        poly2.simplify()
        return poly2
    def __radd__(self,other):
        '''
        A bit tricky thing for using python sum
        '''
        if(not other is Polynomial):
            ot1 = setConst(str(other),vars=self.vars,order=self.order)
            return self.__add__(ot1)
        else:
            return self.__add__(other)
        
        
    def __sub__(self,other):
        '''
        - operation, just subtracting coefficients if the degrees are the same
        '''
        #todo: check same vars exception
        poly2 = Polynomial(monomials=deepcopy(self.monomials) + [-deepcopy(mon2) for mon2 in other.monomials], order=self.order, vars=self.vars)
        poly2.simplify()
        return poly2
    
    def simplify(self):
        '''
        Simplifies the polynomial by coupling the same monomials and deleting those with zero coefficients
        '''
        dd = {}
        for mon in self.monomials:
            key= tuple(mon.deg)#Monomial(deg=mon.deg,coef=1,order=mon.order,vars=mon.vars)
            if key in dd.keys():
                dd[key].coef = dd[key].coef + mon.coef
            else:
                dd[key] = mon
        self.monomials = [mon for mon in dd.values() if not mon.isZero()] 
        

    #call as a function
    def __call__(self, x):
        '''
        Computes value at point x

        Parameters
        float[] x -- a batch (<shape>,d) of points
        OR
        float[] x -- a point (d,)

        Returns
        float (<shape>) or float
        '''
        return np.sum(
                np.concatenate(
                    [mon(x)[None,...] for mon in self.monomials], axis=0
                ),
            axis=0)


    #give a fancy string
    def __str__(self):
        '''
        Gives a string representation of the form x^2y +3z^3 -5
        
        Returns
        str stringRepresentation -- result string
        '''
        if(len(self.monomials)==0):
            return "0"
        else:
            return "".join( ["" if self.monomials[0].isZero() else str(self.monomials[0])] +
            [(" +" if self.monomials[i].coef>=0 else " ") + str(self.monomials[i]) for i in np.arange(1,len(self.monomials))] )

    def degree(self):
        '''
        Returns 
        int deg -- the degree of the polynomial
        '''
        return np.amax([mon.degree() for mon in self.monomials])

    def sort(self):
        '''
        Sorts the monomials in descending order
        '''
        self.monomials = sorted(self.monomials, reverse=True)
        self.sorted = True
        
    def inTerm(self):
        '''
        Gives the initial term with respect to the chosen order
        
        ------------------------------------
        Returns
        Monomial mon
        '''
        if(not self.sorted):
            self.sort()
            self.sorted=True
        return deepcopy(self.monomials[0])
    
    def isZero(self):
        '''
        Checks if a polynomial is zero

        Returns
        bool result
        '''
        if(len(self.monomials)==0):
            return True
        elif (np.all([mon.isZero() for mon in self.monomials])):
            return True
        else:
            return False



def polyFromExpression(expression, vars, const="0", order=None):
    '''
    Converts a string (assuming correctness, i.e. no brackets and duplicates like xyx) to a Polynomial object

    Parameters
    str expression -- expression to convert
    str[] vars -- one-symbol variables
    str const -- 

    Returns
    Polynomial poly    
    '''
    coefGroup = "([0-9.]*)"
    varGroup = "((["+"".join(vars)+"])(\^([0-9]+)){0,1})"
    monRE = re.compile( coefGroup+"("+varGroup+"+)|([+-])" )
    
    opList = monRE.findall(expression)
    monStructs = [ (i,op[0],op[1]) if (not op[1]=="") else (i,op[-1]) for (i,op) in zip(range(len(opList)),opList)]
    monomials = [ constructMonomial(mon, order, vars) if (monStructs[id-1][1]=="+" or id==0) else -constructMonomial(mon, order, vars) 
                    for (id,mon) in zip(range(len(monStructs)),monStructs) if len(mon)>2]
    return Polynomial(monomials=monomials, order=order, vars=vars) + setConst(const,vars=vars,order=order)

def constructMonomial(monStruct, order, vars):
    '''
    Aux function to get monomial from parsed re
    '''
    varGroup = "((["+"".join(vars)+"])(\^([0-9]+)){0,1})"
    monLowLevelRE = re.compile(varGroup)
    monDetails = [(op[1],1 if op[-1]=="" else int(op[-1])) for op in monLowLevelRE.findall(monStruct[-1]) ]
    varDict = {var: id for (id,var) in zip(range(len(vars)),vars)}
    deg = np.zeros([len(vars)]).astype("int32")
    for i in range(len(monDetails)):
        deg[varDict[monDetails[i][0]]]=monDetails[i][1]
    if(monStruct[1]==""):
        coef=1
    else:
        if("." in monStruct[1]):
            coef=float(monStruct[1])
        else:
            coef=int(monStruct[1])
    coef = fractions.Fraction(coef)
    return Monomial(deg=deg, coef=coef, vars=vars, order=order)

def setConst(expr, vars, order=None):
    '''
    Given a string expression of number, construct a 0-degree monomial (const)
    '''
    if("." in expr):
        coef=float(expr)
    else:
        coef=int(expr)
    coef = fractions.Fraction(coef)
    return Polynomial(monomials=[Monomial(deg=np.zeros([len(vars)]).astype("int32"), coef=coef, vars=vars, order=order)], vars=vars, order=order)