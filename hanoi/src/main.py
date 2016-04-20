#!/usr/bin/env python

import os
import subprocess
import pickle
import sys
import math
#from hanoi_soln_par import hanoi_soln_par
from visualisation import visualisation

def main ():
    # The number of discs is hardcoded here for now.
    # We could add it as an argument at the command line or prompt for it.
    noofdiscs = 3
    # The code doesn't work if the number of discs equals 1, so we'll
    # sys.exit when noofdiscs == 1.
    if (noofdiscs == 1):
        sys.exit("Surely you can figure this solution out for yourself?")

    # The number of processes is defined here.
    noofprocs = 1
    # The solver doesn't work if the number of processes isn't a power
    # of 2, so we'll sys.exit when that isn't the case.
    poweroftwo=(math.log(noofprocs, 2)).is_integer()
    if (poweroftwo == False):
        sys.exit("ERROR: the number of processes must be a power of 2.")

    # Calls the hanoi parallel solver and runs it in parallel with the
    # number of processes specified. It also passes the number of discs
    # as an argument for the hanoi_soln_par.py script.
    os.system("mpiexec -n "
              + str(noofprocs)
              + " hanoi_soln_par.py"
              + " "
              + str(noofdiscs))

    # The solver script hanoi_soln_par.py write the solution to pickle
    # file 'moves'. These commands read the solution to the moves list.
    infile = open( "moves", "rb" )
    moves = pickle.load(infile)

    # Calls the visualisation script and gives it the number of discs
    # and the moves list as arguments.
    visualisation(noofdiscs, moves)

    # Now that we've finished with the moves file we'd better delete it
    os.system("rm moves")

main ()
