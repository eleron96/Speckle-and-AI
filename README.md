
# Speckle Stream Processor

Speckle Stream Processor is a terminal-based application to fetch and process data from Speckle streams, focusing on commit details and wall counting. It offers the ability to save the processed data to a database and retrieve previous results. With its interactive terminal UI, you can either process specific commits or all available commits.

## Installation

1. Ensure you have Python 3.x installed. If not, download and install it from [here](https://www.python.org/downloads/).
2. Clone this repository:
   ```bash
   git clone [URL_TO_YOUR_REPO]
   cd [YOUR_REPO_DIRECTORY]
   ```
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Before running the application, ensure to set up the configuration:

1. Edit the `config.py` file to specify your Speckle server host and stream ID.
2. Ensure that the database configurations in `db_handler.py` match your environment.

## Usage

1. Run the main application:
   ```bash
   python main.py
   ```

2. The main menu provides the following options:
   - **Start**: Fetch and process data from Speckle.
   - **View Previous Results**: Check the results saved in the database.
   - **Exit**: Close the application.

### Start Option

When you select the **Start** option, the application lists available commits:

```
[1] Commit ID: f54c703393, Upload date: 2023-10-14 15:01:13.919000+00:00, File name: 17.10.23
[2] Commit ID: 96daf9aef8, Upload date: 2023-10-14 14:35:44.052000+00:00, File name: 16.10.23
...
Select a commit number (1-4) or press Enter to process all:
```

- **Specific Commit**: Enter the number of the commit you wish to process. For example, entering `2` will process only the second commit.
- **All Commits**: Press `Enter` without specifying a commit number to process all commits.

After processing, the application will display results and save them to the database.

### View Previous Results Option

Selecting the **View Previous Results** option will retrieve and display all the results previously saved in the database.

## Functions and Modules

- `config.py`: Contains configurations for the Speckle client.
- `db_handler.py`: Handles database operations, such as saving and retrieving results.
- `utilities.py`: Provides utility functions like `count_walls()` for wall counting.
- `commit_processor.py`: Contains functions for processing commits and listing them.

## License

Specify your licensing terms here if any.


