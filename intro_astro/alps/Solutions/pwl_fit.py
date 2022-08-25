# %load ./Solutions/pwl_fit.py
datasets_flare_pwl        = datasets_flare.stack_reduce(name="NGC1275")
pwl2                 = pwl.copy()
pwl2.tag[0]          ='PowerLawSpectralModel'
model                 = SkyModel(spectral_model=pwl2, name="NGC1275")
datasets_flare_pwl.models = model

fit           = Fit()
results_flare_pwl = fit.run(datasets_flare_pwl)

print(datasets_flare_pwl)
print(results_flare_pwl.parameters.to_table())
datasets_flare_pwl.plot_fit()

e_min, e_max = 0.08, 2.1
energy_edges = np.geomspace(e_min, e_max, 21) * u.TeV

fpe_pwl = FluxPointsEstimator(
    energy_edges=energy_edges, source="NGC1275", selection_optional="all"
)
flux_points_pwl = fpe.run(datasets=datasets_flare_pwl)

flux_points_dataset_pwl = FluxPointsDataset(
    data=flux_points_pwl, models=datasets_flare_pwl.models
)

plt.figure(figsize=(14, 6))
ax = flux_points_pwl.plot(sed_type="e2dnde", color="darkorange")
flux_points_pwl.plot_ts_profiles(ax=ax, sed_type=r"e2dnde")
emin, emax = 80, 2100#5e-2,0.3e1
ymin, ymax = 4e-12,3e-10
ax.set_xlim([emin, emax])
ax.set_ylim([ymin, ymax])
ax.set_ylabel(r"$E^2 dN/dE \quad  [ erg \; cm^{-2} s^{-1}] $",size=20)
for e in dataset_on_off.counts.geom.axes["energy"].edges:
    ax.vlines( e,ymin,ymax, color="black", alpha=0.1 ) 




