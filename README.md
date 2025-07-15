# FIFA Match Analytics Suite

I don't know about you, but I love FIFA (or should I say FC). However, it is unfortunate that EA does not provide a comprehensive way to track and analyze your match statistics. I'm looking at other games such as Dota 2 and League of Legends, which have amazing analytics platforms. 

What I've always wished for is to be able to seemlessly track my match performances (focus at this point is match statistics for Online Seasons, which is what I play!) without having to manually copy and paste data to a spreadsheet or some other tool. I'm proposing something like this FIFA Match Analytics tool, which allows you after a match to hit a hotkey, and the system will automatically capture the match statistics and store them for you to review later in a nice dashboard.

Note: If EA ever decides to provide a proper analytics platform for FIFA/FC, I'll be the first to switch over. But until then, this should do. It also gives us a chance to learn about analytics, machine learning, and web development!

## 1. FIFA Match Analytics - Agent (Windows System Tray Service)

- MSI installer for the background service
- Installs to Program Files
- Creates startup entry
- System tray integration

## 2. FIFA Match Analytics - Backend (Local Web Service)

- Separate executable that runs the REST API and web app
- Handles OCR processing
- Manages SQLite database
- Serves web UI on localhost

## Installation

FIFA_Match_Analytics_Setup.msi

## Credits

This project is organized based on [fastapi/full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template), which is licensed under the MIT License.