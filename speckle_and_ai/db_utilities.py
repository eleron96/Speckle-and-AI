from speckle_and_ai.db_handler import DatabaseHandler

db = DatabaseHandler()


def view_previous_results_option():
    # Display previous results from the database
    results = db.get_previous_results()
    if results:
        print("\n=== Previous Results ===")
        for result in results:
            print("-" * 35)
            print(f"Commit ID: {result[0]}")
            print(f"Upload date: {result[1]}")
            print(f"File name: {result[2]}")
            print(f"Number of elements: {result[3]}")
            print(f"Number of wall elements: {result[4]}")
        print("=" * 35)
    else:
        print("No previous results found.")
