spectral_model_pwl = PowerLawSpectralModel(
)
model_pwl = SkyModel(spectral_model=spectral_model, name="crab_pwl")

datasets.models = [model_pwl]

fit = Fit()
result_pwl = fit.run(datasets=datasets)

datasets.models.to_parameters_table()
print(result_pwl)
print(result_pwl.total_stat)
