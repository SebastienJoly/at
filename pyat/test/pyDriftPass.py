import numpy

'''
This is an example of a python passmethod, here the Drift
passmethod. This is a simplified version that does not check
aperture.
The python passmethods has to be in the python path and contain
a function trackFunction, the element creation is as follows:

drift = elements.Drift('drift', 1.0, PassMethod='pyDriftPass')

To be noted:
The particles are described by a one dimensional vector
6*num_particles in the C tracking engine.
In case a python passmethod and a c passmethod with the same name
are found, the c passmethod is used


'''
def drift6(r, L):
    p_norm = 1/(1+r[4])
    NormL  = L*p_norm   
    r[0]+= NormL*r[1] 
    r[2]+= NormL*r[3]
    r[5]+= NormL*p_norm*(r[1]*r[1]+r[3]*r[3])/2
    return r
   

def trackFunction(rin,elem=None):  
    l = elem.Length
    for i in range(0,len(rin),6):
        rtmp = rin[i:i+6]
        if hasattr(elem,'T1'): rtmp += elem.T1
        if hasattr(elem,'R1'): rtmp = numpy.dot(elem.R1,rtmp)
        rtmp = drift6(rtmp, l)
        if hasattr(elem,'R2'): rtmp = numpy.dot(elem.R2,rtmp)
        if hasattr(elem,'T2'): rtmp += elem.T2
        rin[i:i+6] = rtmp
    return rin
