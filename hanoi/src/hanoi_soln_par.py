#!/usr/bin/env python
''' This is the parallel recursive solution to the Tower of Hanoi and is copied
from the code written in the parallel/rebuilding-the-tower-of-hanoi/ page
of www.drdobbs.com.

The solution has been modified from drdobbs' solution to work with my limited
knowledge of mpi4py. If you use the sleep() functionality to add some dead
time into the loops - even a second will do - you'll start to see the
computation time decrease as the number of processes increases.
'''

from mpi4py import MPI
import sys
import time
import math
import pickle
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
name = MPI.Get_processor_name()


def tower(src, dest, temp, idx, offset, noofdiscs, plan):
    if (offset > 0):
        # Defines the level of recursion that we are at. It runs from 0 to
        # noofdiscs-1 throughout the calculation.
        level = noofdiscs - 2 - int(math.log(offset, 2))

        # This if statement splits the processes in half at each level of
        # recursion until only one process is evaluating each 'branch'.
        # From there it evaluates all subsequent sub-branches and moves.
        if (rank % 2**(level+1) < 2**(level) and 2**(level) < size):
            # Recursively call tower again. This is the left branch, so
            # we SUBTRACT offset from idx.
            tower(src, temp, dest, idx-offset, offset/2, noofdiscs, plan);

            # Add some dead time here.
            time.sleep(1)
            # Adds the src and dest poles of move to the plan array.
            plan[idx-1][0] = src;
            plan[idx-1][1] = dest;

        elif (rank % 2**(level+1) >= 2**(level) and 2**(level) < size):
            # Add some dead time here.
            time.sleep(1)
            # Adds the src and dest poles of move to the plan array.
            plan[idx-1][0] = src;
            plan[idx-1][1] = dest;

            # Recursively call tower again. This is the right branch, so
            # we ADD offset to idx.
            tower(temp, dest, src, idx+offset, offset/2, noofdiscs, plan);

        else:
            # Recursively call tower again. This is the left branch, so
            # we SUBTRACT offset from idx.
            tower(src, temp, dest, idx-offset, offset/2, noofdiscs, plan);

            # Add some dead time here.
            time.sleep(1)
            # Adds the src and dest poles of move to the plan array.
            plan[idx-1][0] = src;
            plan[idx-1][1] = dest;

            # Recursively call tower again. This is the right branch, so
            # we ADD offset to idx.
            tower(temp, dest, src, idx+offset, offset/2, noofdiscs, plan);

    else:
        # Add some dead time here.
        time.sleep(1)
        # Once offset reaches zero the algorithm stops recursively calling
        # tower. Hence all that is left to do is populate the last elements
        # of the plan list.
        plan[idx-1][0] = src;
        plan[idx-1][1] = dest;

    return plan


def main():
    # Initialise the number of discs and the list for containing plan.
    # Initially it is populated with pairs of zeroes [0, 0], s.t. the number
    # of pairs is equal to the number of moves.
    #print "The number of processes is", size, "and this is process", rank
    noofdiscs = int(sys.argv[1])
    plan_init = []
    for i in range(0,2**noofdiscs-1):
        plan_init.append([0, 0])
    # These two variables are used to keep track of the level of recursion
    # of the method.
    idx = 2**(noofdiscs - 1)
    offset = 2**(noofdiscs-2)

    # The plan - the set of moves that solves the tower of Hanoi problem -
    # is obtained by initialising the tower function, which recursively calls
    # ifself until the full solution is found. The solution will be
    # distributed across the processes used in the calculation.
    plan = tower(0, 2, 1, idx, offset, noofdiscs, plan_init)

    # Process 0 now gathers all the modified elements of data together into a
    # new list called allplans.
    allplans = comm.gather(plan,root=0)
    #print 'allplans:',allplans
    # The command gather has stuffed a bunch of mostly empty data lists into a
    # list. The first command essentially picks out all the non-trivial data
    # from each list returned from the processes and bundles it all into one
    # list, the solution.
    if rank == 0:
            plan=[max(i) for i in zip(*allplans)]
            #print 'master:',plan

            # We use pickle to make a moves file which we write the
            # plan list. We use pickle in main() to read the list again.
            outfile=open( "moves", "wb" )
            pickle.dump(plan, outfile)

main()
