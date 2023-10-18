import numpy as np
import matplotlib.pyplot as plt
import loop

chim = loop.xchimney

howmany = 10
chunklength = len(chim)//howmany
L = chunklength*np.arange(1,howmany)
L[howmany//2:] += len(chim)%chunklength

chunks = np.split(chim,L)




