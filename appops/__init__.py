def get_provider_info():
    return {
        "package-name": "airflow-provider-appops",
        "name": "App Ops Provider", # Required
        "description": "A App Ops for airflow providers.", # Required
        "hook-class-names": ["appops.hooks.admob.AdmobHook"],
        # "extra-links": ["sample_provider.operators.sample_operator.ExtraLink"],
        "versions": ["0.0.2"] # Required
    }