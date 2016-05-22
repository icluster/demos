#!/usr/bin/env python

''' The graphics.py module I use is the one found in this link:

    http://anh.cs.luc.edu/python/hands-on/3.1/index.html

 To get it download the zip file called 'Zip file' and you'll find it in the
 examples folder. We need this particular version of graphics.py to run the
 function yUp.
'''

import sys
import time
from graphics import *


class pole:
    ''' This is the pole class as it stands. It initialises by drawing all the discs
    that are on its disc list upon initialisation. It has one function called
    update that add/deletes discs according to their size and position in
    the disc list.
    '''

    def __init__(self, xres, yres,
                 noofdiscs, posx, posy,
                 disclist, win):
        ''' Initisalises the pole by drawing the pole and the disc configuration
        given by disclist.
        '''

        # Graphics window win associated with pole s.t. it doesn't need to be
        # called every time a method is used.
        self.win = win

        # Pole attributes
        self.poleh = yres/2
        self.polew = xres/20
        self.posx = posx
        self.posy = posy

        # Disc attributes
        self.disclist = disclist
        self.noofdiscs = noofdiscs
        self.discx = [0] * self.noofdiscs
        # This loop defines the disc sizes in terms of the noofdiscs and
        # the x/y window resolution.
        for i in range(1, self.noofdiscs+1):
            self.discx[i-1] = xres/4 - \
                              float(i-1)/(self.noofdiscs-1)*float(xres)/8
            self.discy = float(yres)/(3*self.noofdiscs)

        # Specify the bottom-left/top-right corners of the pole.
        point_bl = Point(self.posx-self.polew/2,
                         self.posy-self.poleh/2)
        point_tr = Point(self.posx+self.polew/2,
                         self.posy+self.poleh/2)
        # Define the pole, then colour it brown, then draw it.
        pole_rect = Rectangle(point_bl, point_tr)
        pole_rect.setFill('brown')
        pole_rect.draw(self.win)

        # We'll need a list of disc objects so we'll initialise one
        # full of zeroes here.
        self.discs = [0] * len(self.disclist)
        # This loop puts discs onto the pole according to their
        # position and size in the list called discs.
        for i in range(0, len(self.disclist)):
            for j in range(1, self.noofdiscs+1):
                if self.disclist[i] == j:
                    self.discs[i] = draw_disc(self, self.discx[j-1], i+1,
                                              self.discy, self.win)

    def update(self, newdisclist):
        ''' This method looks at the discs list and updates the discs on the
        pole. If it finds an old disc there it deletes it, then draws the
        new one. If no change occurs it does nothing.
        '''

        # Loop over the elements of disclist
        for i in range(0, self.noofdiscs):
            # If i'th disclist element of pole and global differ, then..
            if self.disclist[i] != newdisclist[i]:
                # Make sure that the slot is filled before undrawing.
                if self.disclist[i] != 0:
                    # Undraw the disc there
                    self.discs[i].undraw()

            # Loop over the disc sizes. Find the right size of disc to draw.
            for j in range(1, self.noofdiscs+1):
                # If pole's disclist element is size j and slot empty then..
                if newdisclist[i] == j and self.disclist[i] == 0:
                    # .. Then draw the new disc of size discx[j-1]
                    self.discs[i] = draw_disc(self, self.discx[j-1], i+1,
                                              self.discy, self.win)

            # Now that all the drawing's done update the pole's disclist slot.
            self.disclist[i] = newdisclist[i]


def draw_disc(pole, discsize, discslot, discy, win):
    ''' Draws a disc on a given pole. It requires the disc's size along the
    x-axis, along the y-axis, and the slot on the pole where it will be
    drawn.
    '''

    # Specify the bottom-left/top-right corners of the disc.
    point_bl=Point(pole.posx - discsize/2,
                  pole.posy - pole.poleh/2 + (discslot-1)*discy)
    point_tr=Point(pole.posx + discsize/2,
                  pole.posy - pole.poleh/2 + discslot*discy)
    # Define the disc, fill it with colour, then draw it.
    disc=Rectangle(point_bl,point_tr)
    disc.setFill('blue')
    disc.draw(win)

    # This line returns the object disc s.t. commands in main() can use
    # disc, e.g. the move command: disc.move(some2dvec)
    return disc


def update_disclist(poleinit, polefin, poles, noofdiscs, win):
    '''Updates the disclists given an initial pole from which to move a disc
    and a final pole to move the disc to.
    '''

    # These loops find poleinit's highest occupied slot and polefin's lowest
    # unoccupied slot. These are where the disc is being moved from and to
    # respectively.
    i = 0
    while (i < noofdiscs and poles[poleinit].disclist[i] != 0):
        i += 1
    if i == 0:
        sys.exit("ERROR: initial pole empty, so no disc can be moved from it.")
    initslot = i-1

    i = 0
    while (i < noofdiscs and poles[polefin].disclist[i] != 0):
        i += 1
    if i == 0:
        finslot = i
    elif i < noofdiscs:
        finslot = i
    elif i == noofdiscs:
        sys.exit("ERROR: final pole full, so no disc can be moved onto it.")

    # We are storing the updated disclists in a variable list called
    # globaldisclist. This we will return to the main program.
    globaldisclist = [0] * 3
    # We are setting globaldisclist equal to the VALUES of poles[all].disclist
    # , and not passing by reference.
    globaldisclist[0] = poles[0].disclist[:]
    globaldisclist[1] = poles[1].disclist[:]
    globaldisclist[2] = poles[2].disclist[:]
    tmp = poles[poleinit].disclist[initslot]
    globaldisclist[poleinit][initslot] = 0
    globaldisclist[polefin][finslot] = tmp

    # Return the updated disclist. Note that the pole's disclist and the
    # globaldisclist still differ.
    return globaldisclist

def visualisation(noofdiscs, moves):

#    # This command sets all python process in front of all other windows.
#    os.system(
#        '''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process \
#        "Python" to true' '''
#    )

    # Define the resolution of the graphics window.
    xres=800
    yres=400
    # Creates the graphics window.
    win = GraphWin("The Tower of Hanoi",xres,yres)
    # This command flips the y-axis s.t. origin is in the bottom-left.
    win.yUp()

    # Initialise the disc-lists, one for each pole. The first pole is filled
    # with noofdiscs discs and the rest have noofdiscs unoccupied slots.
    globaldisclist = [0] * 3
    globaldisclist[0] = range(1,noofdiscs+1)
    globaldisclist[1] = [0] * noofdiscs
    globaldisclist[2] = [0] * noofdiscs
    # Initialises the pole class. In this case it means draw pole at the
    # position specified. The position is the middle of the pole. This
    # way the thickness is more easily accounted for.
    #pole args: xres, yres, noofdiscs, posx, posy, disclist, win
    poles = [0] * 3
    poles[0] = pole(xres, yres, noofdiscs,
                    3*xres/16, 3*yres/8,
                    globaldisclist[0], win)
    poles[1] = pole(xres, yres, noofdiscs,
                    8*xres/16, 3*yres/8,
                    globaldisclist[1], win)
    poles[2] = pole(xres, yres, noofdiscs,
                    13*xres/16, 3*yres/8,
                    globaldisclist[2], win)

    for j in range(0, len(moves)):
        # Update the disclist inputting the initial pole, final pole,
        # the set of pole classes and the number of discs.
        globaldisclist = update_disclist(moves[j][0], moves[j][1],
                                         poles, noofdiscs, win)

        # This is 1 second sleep is just here to see moves clearly.
        time.sleep(1)

        # We are changing update s.t. it takes the globaldisclist as an
        # argument. Hence we can compare the pole's disclist to globaldisclist
        # and undraw/draw differences.
        poles[0].update(globaldisclist[0])
        poles[1].update(globaldisclist[1])
        poles[2].update(globaldisclist[2])

    # This command only allows win to close when the user clicks.
    win.getMouse()
