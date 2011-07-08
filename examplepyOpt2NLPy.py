#
# Example of conversion between an pyOpt model
# and a NLPy model
#
'''
Solves the following linear problem.

    min     -6*x1 + x2
    s.t.:   8*x1 - 2*x2 + x3 = 15
            4*x1 + 5*x2 + x4 = 36
            xi <= 10,  i = 1,2,3,4
'''

import numpy
from pyOpt_optimization import Optimization
from nlpy.optimize.solvers.lbfgs import LBFGSFramework
from TranslatePyOptNLPy import *

# Define a pyOpt model
# First define a function containing objective 
# and constraints function   

def objfunc(x):

    f = -6*x[0] + x[1]
    g = [0.0]*2
    g[0] = 8*x[0] - 2.*x[1] + x[2]
    g[1] = 4*x[0] + 5.*x[1] + x[3]

    fail = 0
    return f,g, fail 

def gradfunc(x,f,g):

    g_obj = numpy.zeros([4])
    g_obj[0] = -6.
    g_obj[1] = 1.
    g_obj[2] = 0.
    g_obj[3] = 0.

    g_con = numpy.zeros([2,4])
    g_con[0,0] = 8.
    g_con[0,1] = -2.
    g_con[0,2] = 1.
    g_con[0,3] = 1.
    g_con[1,0] = 4.
    g_con[1,1] = 5.
    g_con[1,2] = 1.
    g_con[1,3] = 1.

    print g_con
    fail = 0

    return g_obj, g_con, fail


# Instantiate a pyOpt model
opt_prob = Optimization('simple LP',objfunc)

# Add variables
opt_prob.addVar('x1','c',lower=0.0,upper=numpy.inf,value=10.0)
opt_prob.addVar('x2','c',lower=0.0,upper=numpy.inf,value=10.0)
opt_prob.addVar('x3','c',lower=0.0,upper=numpy.inf,value=10.0)
opt_prob.addVar('x4','c',lower=0.0,upper=numpy.inf,value=10.0)

# Add objective name
opt_prob.addObj('f')

# Add constraints
opt_prob.addCon('g1','e',equal=15.0)
opt_prob.addCon('g2','e',equal=36.0)

# print all above info 
print opt_prob

# Choose a sensitivity type
sens_type = gradfunc

# Convert the pyOpt model to a NLPy model
nlp = NLPModel_From_PyOpt(opt_prob, sens_type)

# Need to design a solver for that problem.
