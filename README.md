# StatCan Metadata Scraper

A Python-based web scraper to extract and process metadata from Statistics Canada (StatCan) sources.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The StatCan Web Scraper is designed to automate the process of retrieving statistical metadata from the official Statistics Canada [website](https://www.statcan.gc.ca/). It supports efficient extraction, parsing, and storage of structured data for further analysis.

---

## Features

- Scrape metadata from StatCan tables and datasets
- Parse and clean the extracted data
- Export results to CSV or JSON formats
- Modular design for easy extension

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/avtomatik/statcan_web_scraper.git
cd statcan_web_scraper
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
python3 -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
```

---

## Usage

Run the scraper via the main script:

```bash
python3 src/main.py
# python3 -m src.main
```

The scraper will retrieve metadata and store results in the `output/` directory.

### Example

```bash
python3 src/main.py --dataset "Table 11-10-0010-01"
```

---

## Project Structure

```
statcan_web_scraper/
├── src/
│   ├── main.py         # Entry point
│   ├── core/
│   ├── spiders/        # Spider definition
│   └── utils/          # Utility functions
├── requirements.txt    # Python dependencies
├── README.md
└── LICENSE.md
```

---

## Configuration

Configuration options (like dataset IDs, output formats, and logging levels) can be set in `src/config.py`.

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/my-feature`)
6. Open a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE.md` for details.
