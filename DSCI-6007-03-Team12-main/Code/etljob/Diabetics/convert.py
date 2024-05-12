import gzip
import csv
import pandas as pd

try:
    with gzip.open(r"Diabetics", 'rt') as gz_file:
        csv_reader = csv.reader(gz_file)
        
        # Read the first row to use as column names
        columns = next(csv_reader)

        # Initialize an empty list to store CSV rows
        csv_list = []

        # Process each row in the CSV file
        for row in csv_reader:
            csv_list.append(row)  # Append each CSV row to the list

        # Create a pandas DataFrame from the list of CSV rows and set column names
        df = pd.DataFrame(csv_list, columns=columns)

        # Now you can work with the DataFrame 'df' as needed
        print(df.head())  # Print the first few rows of the DataFrame

        # Save the DataFrame to a CSV file with header (column names)
        df.to_csv('diabetics.csv', index=False)

except IOError as e:
    print("Error:", e)
