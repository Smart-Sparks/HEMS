# file to hold the functions necessary to calculate any info from the raw datafiles pulled from comms
from math import acos
#energy consumed in a minute's calculation
#takes power as an input; energy consumed is the power (J/s) times 60, multiplied by the
#   arccos of the powerfactor.
def energy(power, pf):
    return power * 60 * acos(pf) 

