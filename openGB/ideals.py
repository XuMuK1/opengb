import numpy as np

import openGB.polynomials as polys



class IdealException(Exception):
    def __init__(self,msg):
        self.msg=msg
        
    def __str__(self):
        return "IdealException: " + self.msg
    
class IdealCoefficinentMismatchException(IdealException):
    def __init__(self,msg):
        super(IdealException, self).__init__(msg)
        
    def __str__(self):
        return "IdealCoefficinentMismatchException: " + self.msg
    

class Ideal:
    '''
    Ideals generated by set of polynomials    
    '''
    def __init__(self, polynomials, order):
        '''
        Parameters
        Polynomial[] polynomials -- a sequence of polynomials
        MonomialOrder order -- a monomial order applied to the polynomials
        '''
        self.polynomials = polynomials
        self.order = order
        self.isGB = False

    def sort(self):
        '''
        Sorts all monomials in polynomials
        '''
        for i in np.arange(len(self.polynomials)):
            self.polynomials[i].sort()
            
    def getInTerms(self):
        '''
        Gives a set of initial terms
        
        Returns
        Monomial[] mons
        '''
        return [poly.inTerm() for poly in self.polynomials]

    #a fancy-looking string representation
    def __str__(self):
        return "( "+",\n".join([str(poly) for poly in self.polynomials])+" )"
    
    def getComb(self,polys):
        '''
        Computes a polynomial combination
        
        Input
        Polynomial[] polys -- list of polynomial coefficients
        
        Returns
        Polynomial poly
        '''
        if(len(self.polynomials)==len(polys)):
            polyFinal = sum([polys[i]*self.polynomials[i] for i in np.arange(len(self.polynomials))])
            polyFinal.simplify()
        else:
            raise IdealCoefficinentMismatchException("Wrong number of coffiecients in polynomial combination")
        return polyFinal

    def checkGB(self):
        '''
        Checks if the set of polynomials forms a GB
        '''
        pass

    def computeGB(self):
        '''
        Computes a Groebner Basis using Buchberger algorithm
        '''
        pass
