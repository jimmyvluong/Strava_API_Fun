conda install -c conda-forge plotly_express
conda install -c conda-forge jupyter-dash

conda activate strava_api_env
conda env update --file config/environment.yml --prune