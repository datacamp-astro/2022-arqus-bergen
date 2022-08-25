sets = list(range(0,100))
#sets = list(range(0,70))
TS_list_sim = []
for arg in sets:
    # WE SAVE THE NULL HYPOTESIS logL
    logL_null = list_logL_null[arg]
    # WE LOAD THE SIMULATION
    path_to_folder=("./results_simulations_null/list_logL_per_gridpoint_model_simulation_{}.p".format(arg+1))
    with open(f'{path_to_folder}', 'rb') as fp:
        list_logL_arg = pickle.load(fp)
        # SAVE THE TRUE VALUE OF m and g USED FOR THE SIMULATION
        mgtrue = list( list_logL_arg[0].keys() )[61]
        # FOR EACH ALP GRIDPOINT WE FIND THE 95TH PERCENTILE
        # AND WE SAVE ALL THESE VALUES IN dictionary logL_Bfield
        logL_Bfield = {}
        for mgg in list_logL_arg[0].keys():
            listLogL_perBfield = [list_logL_arg[k][mgg] for k in range(100)]
            percentile         = 5
            logL               =  np.sort( listLogL_perBfield)[percentile]
            logL_Bfield[mgg]   = logL
        # WE CONVERT THE DICT TO A LIST
        list_logL_Bfield =  [logL_Bfield[key] for key in logL_Bfield.keys()]
        # WE ADD THE NULL HYPOTESIS logL
        list_logL_Bfield.append(logL_null)
        # WE LOOK FOR THE MINIMUM VALUE
        logL_min  = np.min(list_logL_Bfield )
        # WE ARE FINALLY READY FOR COMPUTING THE TS FOR THE arg-th SIMULATION
        # IF DATA SIMULATED WITH TRUE HYPOTHESIS DO THIS
        logL_True_Hypot = logL_null
        # IF DATA SIMULATED WITH HYPOTHESIS mgtrue
        #logL_True_Hypot  =  logL_Bfield[mgtrue]
        TS  =  logL_True_Hypot -  logL_min
        TS_list_sim.append(TS)
