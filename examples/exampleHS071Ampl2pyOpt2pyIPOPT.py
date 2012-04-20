'''
Solves problem number 71 from the Hock-Schittkowsky test suite from an AMPL
model, convert it to a pyOpt model and solve it with IPOPT

    min     x1*x4*(x1 + x2 + x3) + x3
    s.t.:
            x1**2 + x2**2 + x3**2 + x4**2 - 40 = 0
            x1*x2*x3*x4 - 25 >= 0
            0 <= xi <= 5,  i = 1,2,3,4


    x0 = [1, 5, 5, 1]    (Feasible)

    f* = 17.0140173
    x* = [1, 4.7429994, 3.8211503, 1.3794082]
'''

# =============================================================================
# Standard Python modules
# =============================================================================
import getopt, os, sys, time
import numpy
# =============================================================================
# Extension modules
# =============================================================================
from nlpy.model import AmplModel
from translatePyoptNLPy import *
from pyOpt import Optimization
from pyOpt import IPOPT


# =============================================================================
# 
# =============================================================================i
PROGNAME = sys.argv[0]

def commandline_err( msg ):
    sys.stderr.write( "%s: %s\n" % ( PROGNAME, msg ) )
    sys.exit( 1 )

def parse_cmdline( arglist ):
    if len( arglist ) != 1:
        commandline_err( 'Specify file name (look in data directory)' )
        return None

    try: options, fname = getopt.getopt( arglist, '' )

    except getopt.error, e:
        commandline_err( "%s" % str( e ) )
        return None

    return fname[0]

ProblemName = parse_cmdline(sys.argv[1:])

# Create a NLPy AmplModel

print 'Problem', ProblemName
nlp = AmplModel( ProblemName )

# Translate this NLPy - Ampl problem in a pyOpt problem
opt_prob = PyOpt_From_NLPModel(nlp)
print opt_prob

# Call the imported solver IPOPT
ipopt = IPOPT()


# Choose sensitivity type for computing gradients with :
#  'FD' : finite difference
#  opt_prob.grad_func : NLPy
# 
# As AMPL isn't handling complex values, we cannot use the complex step method
# to estimate the gradients

SensType = 'FD'

# Solve the opt_prob problem with SNOPT
ipopt(opt_prob, sens_type=SensType)

# Print solution
print opt_prob._solutions[0]


# Change the sensitivity type to finite difference and solve again
SensType = opt_prob.grad_func
ipopt(opt_prob, sens_type=SensType)
print opt_prob._solutions[1]

