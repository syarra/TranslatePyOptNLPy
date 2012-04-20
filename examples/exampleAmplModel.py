##################################
# Use an amplpy model into pyOpt #
##################################
"""

 Use :

    >>>python exampleAmplModel.py data/rosenbrock

 Represents a NLP as AmplModel Class and convert it to a pyOpt problem.

 Example :

 	 min     100 (x1 - x2^2)^2 + (1 - x1)^2
   x1,x2

      s.t.  -200000 <= x1 x2 <= 200000
"""


import getopt, sys
import numpy

from nlpy.model import AmplModel
from translatePyoptNLPy import *

# Import a solver from the pyOpt package
from pyOpt import SNOPT

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
nlp = AmplModel( ProblemName ) #amplpy.AmplModel( ProblemName )


# Translate this NLPy - Ampl problem in a pyOpt problem

nlp.Uvar = numpy.inf * numpy.ones(9)

opt_prob = PyOpt_From_NLPModel(nlp)
print opt_prob

# Call the imported solver SNOPT
snopt = SNOPT()


# Choose sensitivity type for computing gradients with :
#  'FD' : finite difference
#  opt_prob.grad_func : NLPy
# 
# As AMPL isn't handling complex values, we cannot use the complex step method
# to estimate the gradients

SensType = 'FD'

# Solve the opt_prob problem with SNOPT
snopt(opt_prob, sens_type=SensType)

# Print solution
print opt_prob._solutions[0]


# Change the sensitivity type to finite difference and solve again
SensType = opt_prob.grad_func
snopt(opt_prob, sens_type=SensType)
print opt_prob._solutions[1]
