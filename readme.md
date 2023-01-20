# Strava API Fun

### Data source: 
- [Strava API](https://developers.strava.com/)
### Inspiration from: 
- [Rene's writeup](https://towardsdatascience.com/visualize-your-strava-data-on-an-interactive-map-with-python-92c1ce69e91d)

## Planned Features
[] Elevation profile
[] Coaching - do more, rest more, you're doing more than usual
[] Comparison to past performance aka "Relative Performance"
[] Add database schema with all columns and column types
[] Make a PostGreSQL database on Render and store the data there, instead of in DataFrames
[] Cadence x Power x Heartrate?

## MVP Features
[] Tell me how many miles per each activity I have completed.
[] Tell me how many miles per each activity I have completed by month.
[] Tell me how many more miles per each activity I need to do to achieve the next milestone.

## Software Dev Features
[] Pre-and post hooks for managing Conda environments
- https://stackoverflow.com/questions/52038034/push-and-pull-my-conda-environment-using-git/56787188#56787188

## Key concepts practiced
1. Security
- Best practice for hiding API keys and login information
2. Pandas data manipulation
- GROUP BY, SUM, AGG
    - https://stackoverflow.com/questions/39922986/how-do-i-pandas-group-by-to-get-sum
3. Exporting environment.yml files for use by other developers or for other machines.
- Step 1: Export the environment.
    - conda env export > environment.yml
- Step 2: Create the environment from the exported file.
    - conda env create -f environment.yml
- Step 3: If updating the environment and using it on another machine:
    - conda activate myenv
    - conda env update --file local.yml --prune
    - ALTERNATE one line of code: conda env update --name myenv --file local.yml --prune
    - add the `--prune` option to also uninstall packages that were removed from the environment.yml
    - https://stackoverflow.com/questions/42352841/how-to-update-an-existing-conda-environment-with-a-yml-file

4. Working with JSON data type
- https://towardsdatascience.com/all-pandas-json-normalize-you-should-know-for-flattening-json-13eae1dfb7dd
5. Deployment
- https://dash.plotly.com/deployment
- Deploy using Render: https://www.youtube.com/watch?v=H16dZMYmvqo
6. `pip freeze` and `conda list --export` for generating requirements files for your environment
- conda list --export > requirements.txt
- conda create --name <envname> --file requirements.txt
- https://stackoverflow.com/questions/41249401/difference-between-pip-freeze-and-conda-list
7. if __name__ == __main__
- https://www.freecodecamp.org/news/if-name-main-python-example/
- https://realpython.com/if-name-main-python/#:~:text=Nesting%20code%20under%20if%20__,defined%2C%20but%20no%20code%20executes.

## Goal Gear
[] Tri-capable watch
[] Competitive bike
[] Helmet