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
[] Half-year in Review and Year in Review
[] Cadence x Power x Heartrate?
[] Using Dash themes

## MVP Features
[] Tell me how many miles per each activity I have completed.
[] Tell me how many miles per each activity I have completed by time (week, month, year)
[] Tell me how many more miles per each activity I need to do to achieve the next milestone.

## Software Dev Features
[] Pre-and post hooks for managing Conda environments
- https://stackoverflow.com/questions/52038034/push-and-pull-my-conda-environment-using-git/56787188#56787188
[] Protect my API keys by reading data from a Google spreadsheet
[] Optional - let others use their own spreadsheet using the spreadsheet id

## Key concepts practiced
1. Security
- Best practice for hiding API keys and login information
- https://www.freecodecamp.org/news/private-api-keys/
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
8. Dash themes
- https://towardsdatascience.com/3-easy-ways-to-make-your-dash-application-look-better-3e4cfefaf772#:~:text=There%20are%20a%20range%20of,%2C%20VAPOR%2C%20YETI%2C%20ZEPHYR.
- https://pypi.org/project/dash-bootstrap-templates/
9. PIP versus CONDA for installing packages
- https://stackoverflow.com/questions/20994716/what-is-the-difference-between-pip-and-conda#:~:text=It's%20fully%20recommended%20to%20use,perfectly%20acceptable%20to%20use%20pip.


## Goal Gear
[x] Tri-capable watch
[] Competitive bike
[] Helmet
[] Bike computer
[] Daily trainer shoes #3

## Goal ???
[] Donate old ___ to someone.
[] 

KOR CONNECT
https://korconnect.io/security.html

RESEARCH
https://science4performance.com/2017/05/05/strava-fitness-and-freshness/

### Thoughts - what do I want to know?
- Total mileage per month
- Spread of distances over time?
- How do I replace Strava premium for the features that I want?
- What is my "easy" running pace?
- *Look at preparation up to the half-marathon*
- *Could set weekly time running goals and/or weekly running mileage goals.* Did I actually stick to the plan?
- hard, hard, easy patterns? Does my training mirror this? What is a hard week? Pace, mileage, heartrate, average heartrate could label a week by difficulty? https://www.outsideonline.com/health/running/training-advice/science/big-data-reveals-new-marathon-training-approaches/