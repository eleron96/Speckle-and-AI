[![Maintainability](https://api.codeclimate.com/v1/badges/58743ca4ae6635619d7a/maintainability)](https://codeclimate.com/github/eleron96/Speckle-and-AI/maintainability)

# Speckle Stream Processor 🚀

Speckle Stream Processor is a robust terminal-based application designed to seamlessly fetch and process data from Speckle streams. It emphasizes commit details, room counting, and wall counting, offering a comprehensive insight into your Speckle data. With its intuitive terminal UI, you can either dive deep into specific commits or get an overview of all available commits.

A unique aspect of this program is that it was entirely created thanks to GPT-4 and management from my side. So, while the program might be considered primitive, the fact that it was assembled and developed with the help of AI makes it truly unique in its scope and execution.
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

````markdown
Available projects (streams):                                                   
┏━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┓                  
┃ Number ┃ Name                       ┃ ID                   ┃                  
┡━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━┩                  
│ 1      │ V------------2             │ e3------2e           │                  
│ 2      │ V------------9             │ d8------12           │                  
│ 3      │ IT_TEST                    │ 2e------35           │                  
│ 4      │ D----------- 4             │ 96------f6           │                  
│ 5      │ V------------3b            │ 45------f5           │                  
│ 6      │ D----------- 3             │ f6------8e           │                  
│ 7      │ О------------------------" │ d5------82           │                  
│ 8      │ О-----------------------"  │ 37------28           │                  
│ 9      │ !TEST                      │ f3------eb           │                  
│ 10     │ IT_TEST_2                  │ 43------9f           │                  
└────────┴────────────────────────────┴──────────────────────┘  
````
Next you can choose a project by entering the corresponding number. After selecting a project, you will be presented with the following options:
```markdown
╭─────── Speckle and AI Application ────────╮
│ [1] Commit Info                           │
│ [2] View Previous Results                 │
│ [3] Project Info                          │
│ [4] Check Potential Matches of Room Names │
│ [5] Check Last Commit Section Names       │
│ [6] Check area discrepancy                │
│ [7] Inspection of residential premises    │
│ Type 'exit' to exit the program           │
╰──────────────── Main Menu ────────────────╯
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
File name:                06.06.24
Number of elements:       1730
Number of rooms:          498
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
--------------------
Branch name:              section-2
File name:                06.06.24
Commit ID:                7*******28
Upload date:              2024-06-06 09:37:29.920000+00:00
Number of elements:       18863
Number of rooms:          5670
--------------------
----------Overall Total:-----------
Number of elements:       34626
Number of rooms:          10060
----------Apartment Types----------
3M - 203
2E*(1L) - 726
1M - 78
1E*(ST-M) - 38
ST-S - 12
3E*(2M) - 1045
4E*(3M) - 255
6E*(5S) - 117
.......
******************************
```
#### [4] Check Potential Matches of Room Names
Analyzes the project data to find potential matches for room names (for example between Latin 'M' and Cyrillic 'М' Alphabets), helping to identify inconsistencies or duplicates.

Example Output:
```sql
Check for the use of alphabets:
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━┓
┃ Room name            ┃ Alphabets ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━┩
│ 3M                   │ Latin     │
│ 2E*(1L)              │ Latin     │
│ 1M                   │ Latin     │
│ 1E*(ST-M)            │ Latin     │
│ ST-M                 │ Latin     │
│ МОП                  │ Cyrillic  │
│ 2E*(1S)              │ Latin     │
│ ВП                   │ Cyrillic  │
│ ИП                   │ Cyrillic  │
│ --                   │ Undefined │
│ 4S                   │ Latin     │
│ ST-S                 │ Latin     │
│ 3E*(2M)              │ Latin     │
│ Кровля               │ Cyrillic  │
│ 4E*(3M)              │ Latin     │
│ 6E*(5S)              │ Latin     │
└──────────────────────┴───────────┘
```

#### [5] Check Last Commit Section Names
Displays the section names from the last commit, providing insights into the structure and organization of the latest data.

Example Output:
```less
Checking branch: section-1
Corpus section short: 1
----------------------------------------
Checking branch: section-3
Corpus section short: 3
----------------------------------------
Checking branch: stlb
Warning: more than 1 value in the corpus:
Corpus section short:
2
1
4
P
3
----------------------------------------
Checking branch: section-2
Corpus section short: 2
----------------------------------------
```

#### [6] Check Area Discrepancy
Checks for discrepancies in the area calculations within the project, ensuring data accuracy.

Example Output:
```yaml
Checking branch: s3
Commit Message: 04.04.24
The rooms have been mapped
----------------------------------------
Checking branch: stlb
Commit Message: 04.04.24
The rooms have not been mapped!
┏━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━┓
┃   ┃          ┃             ┃ Area in     ┃ Rounded     ┃        ┃ Room       ┃
┃ № ┃ Rooms    ┃ Name        ┃ Revit       ┃ Area        ┃ Level  ┃ Number     ┃
┡━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━┩
│ 1 │ 16144623 │ Лестничная  │ 8.30374999… │ 9.1         │ 1 этаж │ 2          │
│   │          │ клетка      │             │             │        │            │
│ 2 │ 16193586 │ Торговый    │ 104.547999… │ 104.100000… │ 1 этаж │ 2          │
│   │          │ зал         │             │             │        │            │
└───┴──────────┴─────────────┴─────────────┴─────────────┴────────┴────────────┘
----------------------------------------
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





