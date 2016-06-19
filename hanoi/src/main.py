#!/usr/bin/env python

import os
import pickle
import sys
import math
from visualisation import visualisation
import time


def main ():
    # Prompts user for the number of discs.
    noofdiscs = raw_input("Please enter the number of discs: ")
    # Checks if noofdiscs is an integer. Terminates program if not.
    if (noofdiscs.isdigit() == False):
        sys.exit("ERROR: number of discs must be a positive integer.")
    # Checks if noofdiscs is positive. Terminates program if not.
    if (int(noofdiscs) <= 0):
        sys.exit("ERROR: number of discs must be a positive integer.")
    # The code doesn't work if the number of discs equals 1, so we'll
    # sys.exit when noofdiscs == 1.
    if (noofdiscs == 1):
        sys.exit("Surely you can figure this solution out for yourself?")
    # Make sure noofdiscs is an integer.
    noofdiscs = int(noofdiscs)

    # Prompts user for the number of processes.
    noofprocs = raw_input("Please enter the number of processes: ")
    # Checks if noofprocs is an integer. Terminates program if not.
    if (noofprocs.isdigit() == False):
        sys.exit("ERROR: number of processes must be a positive integer.")
    # Checks if noofprocs is positive. Terminates program if not.
    if (float(noofprocs) <= 0):
        sys.exit("ERROR: number of processess must be a positive integer.")
    # The solver doesn't work if the number of processes isn't a power
    # of 2, so we'll sys.exit when that isn't the case.
    poweroftwo=(math.log(float(noofprocs), 2)).is_integer()
    if (poweroftwo == False):
        sys.exit("ERROR: the number of processes must be a power of 2.")

    # Check if there is a hostlist file. If there is read the list of hosts
    # and use those hosts to run the solver. If the file is empty or missing
    # then run the solver without a list of hosts.
    try:
        if os.stat('hostlist').st_size > 0:
            # Reads the hostlist file
            hostlist = [line.strip('\n') for line in open('hostlist')]
            # Prints out a list of the hosts and the processes they will run.
            noofprocs = int(noofprocs)
            for i in range(0, noofprocs):
                print hostlist[i],'is running process',i+1
            # Prepares the hostlist for the mpiexec command.
            hostlist = ",".join(hostlist)
            tick = time.time()
            os.system("mpiexec -n "
                      + str(noofprocs)
                      + " -host " + hostlist
                      + " hanoi_soln_par.py"
                      + " "
                      + str(noofdiscs))
        else:
            tick = time.time()
            os.system("mpiexec -n "
                      + str(noofprocs)
                      + " hanoi_soln_par.py"
                      + " "
                      + str(noofdiscs))
    except OSError:
        tick = time.time()
        os.system("mpiexec -n "
                      + str(noofprocs)
                      + " hanoi_soln_par.py"
                      + " "
                      + str(noofdiscs))
    print "The time the solver took was", time.time()-tick, "seconds"

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
