# fantasy_stattracker
Fantasy hockey statistics aggregator and tracking, as well as visualizations

## Installation
This program requires Python >=3.6. All dependencies can be installed using `pip install .`.

## Setup
1. Register for a [Yahoo Developer Network API key](https://developer.yahoo.com/apps/) by creating an app and filling in the relevant information. For URLs, you can use any valid URLs (they don't really matter here, feel free to use [https://github.com/archielee/fantasy_stattracker](https://github.com/archielee/fantasy_stattracker)). Copy the resulting API access key information into `auth_key.json`. Remember to keep these keys private!

2. Specify your league settings in `league_info.json`, including things such as your league type ("hockey", "basketball", etc.), league ID (the number that's in the URL when you go to your league homepage), number of teams, schedule length, and roster make-up.

3. Run `scripts/initial_setup.py` in your terminal and log into Yahoo using the resulting browser pop-up. Allow the app to access your fantasy data. After, you should see a screen that says "Use this code to connect and share your Yahoo info...". Copy the code into the terminal and press `[Enter]` to continue. The information in `league_info.json` will automatically update. DO NOT TOUCH THIS FILE AFTER YOU HAVE DONE THIS STEP.

Note: If you wish to stop allowing this app to access your fantasy information, then you can look under the recent activity tab in your Yahoo account information page and remove the app there.

## Development
If you are attempting to modify this library, you can install the package in development mode using the command `pip install --editable .`. Then, you can modify the library components in `fantasy_stattracker` or the scripts that use the library in `scripts`.
