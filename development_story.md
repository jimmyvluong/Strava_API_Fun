1. December 2022
- After following the Towards Data Science tutorials I decided to branch off and initially not focus on mapping, but more on working with the activity data in DataFrames.
2. January 2023
- I could be ready to "go live" with the data in plots with Render, but I am wary of exposing my Strava API keys to people using DevTools.
3. February 2023
- I consulted my software development friend and she suggested reading the data from a Google spreadsheet. This is an interesting idea to pursue. Maybe this opens up the possibility that other people could use their own Google spreadsheets with the project by simply exporting their Strava data from the website.
4. March 2023
- A friend of mine suggested I write some user stories for this app. I decided to write a user story for myself and include it in a "Data Project Template".
- Tried to use config.py as a secret file to pull keys from. Did not work. Next step is to use environment variables.
- After implementing environment variables in Render, I found that the access_token wasn't available. I printed the payload's contents and found that for the key values, like client_id, I didn't need to put quotes around the key's value, like '98155'. I only need to enter 98155.
5. April 2023
- Strava doesn't offer the feature of tracking goals when people ride together - I will try to build out a way to track our group ride's progress
6. May 2023
- I found a way to show the map by hosting the file on github pages.
- see the github page here: https://github.com/jimmyvluong/Strava_API_Fun/settings/pages
7. November 2023
- Floating the idea to create a "Year in Review" story
- show: race results tag: "race"
- show: sticking to the plan"
- 