e_min, e_max = 0.1, 10
energy_edges = np.geomspace(e_min, e_max, 16) * u.TeV

fpe = FluxPointsEstimator(
    energy_edges=energy_edges, source="crab", selection_optional="all"
)
flux_points_crab_pwl = fpe.run(datasets=datasets)

flux_points_pwl.to_table(sed_type="dnde", formatted=True)

plt.figure(figsize=(8, 5))
ax = flux_points.plot(sed_type="e2dnde", color="darkorange")
flux_points_pwl.plot_ts_profiles(ax=ax, sed_type="e2dnde")
