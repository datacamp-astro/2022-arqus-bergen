source     = Source(z = 0.017559, ra = '03h19m48.1s', dec = '+41d30m42s') # this is for ngc1275

pin        = np.diag((1.,1.,0.)) * 0.5
alp        = ALP(0,0) 
modulelist = ModuleList(alp, source, pin = pin)
modulelist.add_propagation("ICMGaussTurb", 
          0, # position of module counted from the source. 
          nsim = 1, # number of random B-field realizations
          B0 = 15.,  # rms of B field
          n0 = 39.,  # normalization of electron density
          n2 = 4.05, # second normalization of electron density, see Churazov et al. 2003, Eq. 4
          r_abell = 500., # extension of the cluster
          r_core = 80.,   # electron density parameter, see Churazov et al. 2003, Eq. 4
          r_core2 = 280., # electron density parameter, see Churazov et al. 2003, Eq. 4
          beta = 1.2,  # electron density parameter, see Churazov et al. 2003, Eq. 4
          beta2= 0.58, # electron density parameter, see Churazov et al. 2003, Eq. 4
          eta = 0.5, # scaling of B-field with electron denstiy
          kL = 0.18, # maximum turbulence scale in kpc^-1, taken from A2199 cool-core cluster, see Vacca et al. 2012 
          kH = 9.,  # minimum turbulence scale, taken from A2199 cool-core cluster, see Vacca et al. 2012
          q = -2.80, # turbulence spectral index, taken from A2199 cool-core cluster, see Vacca et al. 2012
          seed=0 # random seed for reproducability, set to None for random seed.
         )
modulelist.add_propagation("EBL",1, model = 'dominguez') # EBL attenuation comes second, after beam has left cluster
modulelist.add_propagation("GMF",2, model = 'jansson12', model_sum = 'ASS') # finally, the beam enters the Milky Way Field


