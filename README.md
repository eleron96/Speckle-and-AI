[![Maintainability](https://api.codeclimate.com/v1/badges/58743ca4ae6635619d7a/maintainability)](https://codeclimate.com/github/eleron96/Speckle-and-AI/maintainability)

# Speckle Stream Processor 🚀

**Speckle Stream Processor** is a robust terminal-based application designed to seamlessly fetch and process data from Speckle streams. It emphasizes commit details, room counting, and wall counting, offering a comprehensive insight into your Speckle data. With its intuitive terminal UI, you can either dive deep into specific commits or get an overview of all available commits.

## 📌 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Main Menu Options](#main-menu-options)
    - [[1] Commit Info](#1-commit-info)
    - [[2] View Previous Results](#2-view-previous-results)
    - [[3] Project Info](#3-project-info)
    - [[4] Check Potential Matches of Room Names](#4-check-potential-matches-of-room-names)
    - [[5] Check Last Commit Section Names](#5-check-last-commit-section-names)
    - [[6] Check Area Discrepancy](#6-check-area-discrepancy)
    - [[7] Inspection of Residential Premises](#7-inspection-of-residential-premises)

## 🛠 Installation

1. Ensure you have **Python 3.x** installed. If not, [download and install it](https://www.python.org/downloads/).
2. Clone this repository:
   ```bash
   git clone https://github.com/eleron96/Speckle-and-AI
   cd Speckle-and-AI
   ```
3. Install the required packages:
   ```bash
   pip install poetry
   ```
4. Install the required packages using Poetry:
   ```bash
   poetry install
   ```

## ⚙ Configuration

Before diving in, make sure to:

1. Ensure the database configurations in `db_handler.py` align with your setup.
2. Update any necessary authentication details in `authentication.py`.

## 🚀 Usage

Kickstart the application with:
```bash
poetry run python main.py
```

### Main Menu Options
Upon starting the program, you will be presented with the main menu:

```
[1] Commit Info
[2] View Previous Results
[3] Project Info
[4] Check Potential Matches of Room Names
[5] Check Last Commit Section Names
[6] Check Area Discrepancy
[7] Inspection of Residential Premises
```
#### [1] Commit Info
This option allows you to view detailed information about a specific commit. You can choose to view the commit details by entering the commit ID.
````yaml
[1] Commit ID: f54c703393, Upload date: 2023-10-14 15:01:13.919000+00:00, File name: 17.10.23
[2] Commit ID: 96daf9aef8, Upload date: 2023-10-14 14:35:44.052000+00:00, File name: 16.10.23
...
````
##### Post-processing, the application showcases results and archives them in the database.
```markdown
File name:                    17.10.23
Number of elements:           120
Number of rooms:              5
-----------------------------------
```

#### [2] View Previous Results
Fetches and displays all the results previously stashed in the database.

Example Output:
```yaml
Previous Results:
1. File name: 17.10.23, Rooms: 5, Elements: 120
2. File name: 16.10.23, Rooms: 4, Elements: 110
...
```

#### [3] Project Info
Provides detailed information about the project, including metadata and current configurations.

Example Output:
```yaml
Project Information:
Branch: main
Last Commit: 2023-10-14
Number of elements: 120
Number of rooms: 5
-----------------------------------
```
#### [4] Check Potential Matches of Room Names
Analyzes the project data to find potential matches for room names, helping to identify inconsistencies or duplicates.

Example Output:
```sql
Check for potential name matches:
Room1 и Room2 - Potential matches
Room3 и Room4 - Potential matches
...
```

#### [5] Check Last Commit Section Names
Displays the section names from the last commit, providing insights into the structure and organization of the latest data.

Example Output:
```less
Last Commit Section Names:
Section 1: Living Room
Section 2: Bedroom
...
```

#### [6] Check Area Discrepancy
Checks for discrepancies in the area calculations within the project, ensuring data accuracy.

Example Output:
```yaml
Area Discrepancy Check:
Room: Living Room, Revit Area: 50, Calculated Area: 48
Room: Bedroom, Revit Area: 30, Calculated Area: 30
...
```

#### [7] Inspection of Residential Premises
Inspects residential areas within the project to verify compliance with specified criteria.

Example Output:
```yaml
Inspection of Residential Premises:
Room: Living Room, Status: Pass
Room: Bedroom, Status: Fail - Area discrepancy
...
```





