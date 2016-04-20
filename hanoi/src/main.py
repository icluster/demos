#!/usr/bin/env python

import os
import subprocess
from hanoi_soln_par import hanoi_soln_par
from visualisation import visualisation

def main ():
    noofdiscs = 3
    # Calls the hanoi parallel solver and stores the returned solution
    # as moves.
    moves=hanoi_soln_par(noofdiscs)

    # Calls the visualisation script and gives it the number of discs
    # and the moves list as arguments.
    visualisation(noofdiscs, moves)

main ()
