#
# Example of conversion between an pyOpt model
# and a NLPy model
#
'''
Solves the following linear problem.

    min      x1**2 + x2**2
'''

import numpy
from pyOpt.pyOpt_optimization import Optimization
from nlpy.optimize.solvers.lbfgs import LBFGSFramework
from translatePyoptNLPy import *

# Define a pyOpt model
# First define a function containing objective 
# and constraints function   

def objfunc(x):

    f = x[0]**2 + x[1]**2
    g = None

    fail = 0
    return f,g, fail

def gradfunc(x,f,g):

    g_obj = [0.0]*2
    g_obj[0] = 2.*x[0]
    g_obj[1] = 2.*x[1]

    g_con = None

    fail = 0
    return g_obj, g_con, fail


# Instantiate a pyOpt model
opt_prob = Optimization('simple QP',objfunc)

# Add variables
opt_prob.addVar('x1','c',lower=-numpy.inf,upper=numpy.inf,value=10.0)
opt_prob.addVar('x2','c',lower=-numpy.inf,upper=numpy.inf,value=10.0)

# Add objective name
opt_prob.addObj('f')

# print all above info 
print opt_prob

# Choose a sensitivity type
sens_type = gradfunc

# Convert the pyOpt model to a NLPy model
nlp = NLPModel_From_PyOpt(opt_prob, sens_type)

# Solve this NLPy problem with L-BFGS.
lbfgs = LBFGSFramework(nlp)

lbfgs.solve()

print
print 'Final variables:', lbfgs.x
print
print '-------------------------------'
print 'LBFGS: End of Execution'
print '  Problem                     : %-s' % nlp.name
print '  Dimension                   : %-d' % nlp.n
print '  Number of (s,y) pairs stored: %-d' % lbfgs.npairs
print '  Converged to optimality     : %-s' % repr(lbfgs.converged)
print '  Initial/Final Objective     : %-g/%-g' % (lbfgs.f0, lbfgs.f)
print '  Initial/Final Gradient Norm : %-g/%-g' % (lbfgs.g0,lbfgs.gnorm)
print '  Number of iterations        : %-d' % lbfgs.iter
print '  Scaling                     : %-s' % repr(lbfgs.lbfgs.scaling)
print '  Setup/Solve time            : %-gs' % lbfgs.tsolve
print '  Total time                  : %-gs' % lbfgs.tsolve
print '-------------------------------'

