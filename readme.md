# Strava API Fun

### Data source: 
- [Strava API](https://developers.strava.com/)
### Inspiration from: 
- [Rene's writeup](https://towardsdatascience.com/visualize-your-strava-data-on-an-interactive-map-with-python-92c1ce69e91d)

## Planned Features
[] Elevation profile
[] Coaching - do more, rest more, you're doing more than usual
[] Comparison to past performance aka "Relative Performance"

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
4. Working with JSON data type
- https://towardsdatascience.com/all-pandas-json-normalize-you-should-know-for-flattening-json-13eae1dfb7dd
## Goal Gear
[] Tri-capable watch
[] Competitive bike