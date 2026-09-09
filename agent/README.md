# FIFA Match Analytics - Agent

Background service that captures FIFA match statistics automatically through hotkeys. This is part of the FIFA Match Analytics suite.

## Features

- Silent background operation
- Hotkey detection
- Automatic screenshot capture of match statistics
- Integration with FIFA Match Analytics dashboard

## Usage

1. Play a FIFA match
2. When the match ends, press `Win + O` on the statistics screen
3. The agent will capture the statistics and hand them to the backend for OCR

Note: results are not persisted yet, so there is no match history to view. See
the root `README.md` for what is and isn't built.

## Prerequisites

.venv\Scripts\activate
python main.py