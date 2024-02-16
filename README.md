[![Maintainability](https://api.codeclimate.com/v1/badges/58743ca4ae6635619d7a/maintainability)](https://codeclimate.com/github/eleron96/Speckle-and-AI/maintainability)

# Speckle Stream Processor 🚀

**Speckle Stream Processor** is a robust terminal-based application designed to seamlessly fetch and process data from Speckle streams. It emphasizes commit details, room counting, and wall counting, offering a comprehensive insight into your Speckle data. With its intuitive terminal UI, you can either dive deep into specific commits or get an overview of all available commits.

## 📌 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Start Option](#start-option)
  - [View Previous Results Option](#view-previous-results-option)
- [Functions and Modules](#functions-and-modules)
- [License](#license)

## 🛠 Installation

1. Ensure you have **Python 3.x** installed. If not, [download and install it](https://www.python.org/downloads/).
2. Clone this repository:
   ```bash
   git clone [URL_TO_YOUR_REPO]
   cd [YOUR_REPO_DIRECTORY]
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙ Configuration

Before diving in, make sure to:

1. Edit the `config.py` file to specify your Speckle server host and stream ID.
2. Ensure the database configurations in `db_handler.py` align with your setup.

## 🚀 Usage

Kickstart the application with:
```bash
python main.py
```

### Start Option

Upon selecting the **Start** option, the application unveils available commits:

```
[1] Commit ID: f54c703393, Upload date: 2023-10-14 15:01:13.919000+00:00, File name: 17.10.23
[2] Commit ID: 96daf9aef8, Upload date: 2023-10-14 14:35:44.052000+00:00, File name: 16.10.23
...
```

- **Specific Commit**: Input the commit number to process. E.g., `2` processes the second commit.
- **All Commits**: Simply press `Enter` to process every commit.

Post-processing, the application showcases results and archives them in the database.

### View Previous Results Option

Opting for **View Previous Results** fetches and displays all the results previously stashed in the database.

## 📚 Functions and Modules

- `config.py`: Houses configurations pivotal for the Speckle client.
- `db_handler.py`: Orchestrates database operations, ensuring smooth saving and retrieval of results.
- `utilities.py`: A utility belt with functions like `count_walls()` for meticulous wall counting.
- `commit_processor.py`: Encompasses functions tailored for processing and listing commits.

## 📜 License

Specify your licensing terms here if any.

