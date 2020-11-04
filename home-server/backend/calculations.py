# file to hold the functions necessary to calculate any info from the raw datafiles pulled from comms
#energy consumed in a minute's calculation
#takes power as an input assuming power is apparent power; energy consumed is the power (J/s) times 60, multiplied by the
def energy(power, pf):
    return power * 60 * pf 

