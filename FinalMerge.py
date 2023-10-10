import csv
import numpy as np
import pandas as pd
from enum import Enum
from scipy.stats.mstats import spearmanr

CORRELATE = True    
# Set a correlation threshold
FEATURE_FEATURE_THRESHOLD = 0.7
FEATURE_ALGO_CONSIDERATION = 0.3


class DataType(Enum):
    FEATURE = "FEATURE"
    ALGORITHM = "ALGORITHM"


class DataInfo:
    def __init__(self, name, filename, abb, data_type):
        self.name = name
        self.filename = filename
        self.abb = "_" + abb
        self.data_type = data_type


def feature_spearman(dataframe):
    df = dataframe

    # Save the first column and remove it temporarily (first two if ck because type_ck
    columns_to_remove = set()

    if "type_ck" in dataframe:

        # Remove all anonymous classes
        dataframe = dataframe[dataframe['type_ck'] != 'anonymous']

        # Remove the type_ck column
        dataframe = dataframe.iloc[:, 2:]
        print("Removed type_ck")
        columns_to_remove.add("type_ck")
    else:
        dataframe = dataframe.iloc[:, 1:]

    # Calculate Spearman correlations
    correlation_matrix = dataframe.corr(method='spearman')

    # Get column pairs with correlation greater than the threshold
    high_corr_columns = [(col1, col2) for col1 in correlation_matrix.columns for col2 in correlation_matrix.columns if
                         col1 != col2 and abs(correlation_matrix.loc[col1, col2]) > FEATURE_FEATURE_THRESHOLD]

    # Columns to remove (choose one from each correlated pair)
    for col1, col2 in high_corr_columns:
        if col1 not in columns_to_remove and col2 not in columns_to_remove:
            columns_to_remove.add(col2)
            print("removing " + col2)

    # Remove the selected columns
    df_filtered = df.drop(columns=columns_to_remove)

    # Convert all non-title columns into float
    columns_to_convert = df_filtered.columns[1:]
    df_filtered[columns_to_convert] = df_filtered[columns_to_convert].apply(pd.to_numeric, errors='coerce')

    print("keeping " + str(df_filtered.columns))
    return df_filtered


def algorithm_spearman(dataframe, input_files):

    features = []
    algos = []

    for file_in in input_files:
        if file_in.data_type == DataType.FEATURE:
            features.append(dataframe.filter(regex=file_in.abb+"$"))
        elif file_in.data_type == DataType.ALGORITHM:
            algos.append(dataframe.filter(regex=file_in.abb + "$"))

    columns_to_be_removed = []
    appropriate_corr = []

    for f_df in features:
        for algo in algos:
            correlations = []
            for col in f_df.columns:
                col1 = np.array(f_df[col], dtype=float)
                col2 = np.array(algo.filter(regex="Coverage"), dtype=float)

                # Check if they contain string
                correlation, _ = spearmanr(col1, col2, nan_policy='omit')
                correlations.append((col, correlation))

            # Find columns in df with correlation lower than threshold
            low_corr_column = [col for col, correlation in correlations if abs(correlation) < FEATURE_ALGO_CONSIDERATION]
            high_corr_column = [col for col in f_df.columns if col not in low_corr_column]

            # If correlation greater than threshold, we will keep only one
            if high_corr_column:
                if len(high_corr_column) > 1:
                    appropriate_corr.append(high_corr_column[1:])
                else:
                    appropriate_corr.append(high_corr_column[0])

            # Remove all columns with lower correlation
            if low_corr_column:
                for col in low_corr_column:
                    if col not in columns_to_be_removed and col not in appropriate_corr:
                        columns_to_be_removed.append(col)

    # Filter df to keep only the high-correlation columns
    df_filtered = dataframe.drop(columns=columns_to_be_removed)

    return df_filtered


# ----- Read in the CSV output files -----
def read_output(input_files, current_dir):
    # List of CSV_Data
    dataframes = []

    # For each csv
    for i, file in enumerate(input_files):

        # Open the input CSV file
        with open(file.filename, 'r') as infile:

            print("\nReading " + file.name)

            # Create a CSV reader object
            reader = csv.reader(infile)

            # Extract the header row
            header_row = next(reader)

            # Read the remaining rows
            rows = list(reader)

            # first columns are either class name or file path. If not the class...
            if header_row[0] != "TARGET_CLASS":

                if header_row[0] != "class_name":
                    # Remove the first column from each row
                    rows = [[col for i, col in enumerate(row) if i != 0] for row in rows]
                    header_row = header_row[1:]

                header_row[0] = "TARGET_CLASS"

            # Sort the rows by class
            sorted_rows = sorted(rows, key=lambda row: row[0])

            # Append every stat in the header with the abbreviation of the tool it comes from
            for j, cell in enumerate(header_row[1:], start=1):
                header_row[j] = cell + file.abb

            # Create a dataframe to store the data
            df = pd.DataFrame(sorted_rows, columns=header_row)

            # Remove all test classes
            df = df[~df['TARGET_CLASS'].str.contains("EvoSuiteTest")]

            # Remove all classes with anonymous in them
            df = df[~df['TARGET_CLASS'].str.contains("Anonymous")]

            # Modify the feature dataframes based on Spearman's Correlation
            if CORRELATE and file.data_type == DataType.FEATURE:
                df = feature_spearman(df)

            # Form the final array of dataframes and store it
            dataframes.append(df)
            print(file.name + " sorted and added\n")

    # Create an empty DataFrame to store the merged data
    print("\nAttempting to merge")
    merged_df = pd.DataFrame()

    # Populate the DataFrame with data from CSV_Data
    for index, df in enumerate(dataframes):

        # Strip any leading/trailing spaces (Javaparser csv seems to have leading spaces in the cells)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # Merge
        if index == 0:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on='TARGET_CLASS', how='outer')

    # remove covered goals, target goals, criterion
    merged_df = merged_df.drop(merged_df.filter(regex='Covered_Goals_').columns, axis=1).drop(merged_df.filter(regex='Total_Goals_').columns, axis=1).drop(merged_df.filter(regex='criterion_').columns, axis=1)

    # tcc_ck and lcc_ck are -1, 0, or NaN. Replace NaN string with 2, but not blank rows
    try:
        merged_df.loc[merged_df.tcc_ck == 'NaN', "tcc_ck"] = 2
        merged_df.loc[merged_df.lcc_ck == 'NaN', "lcc_ck"] = 2
    except AttributeError:
        # might've been correlated out
        pass

    if CORRELATE:
        merged_df = algorithm_spearman(merged_df, input_files)

    # Add feature_ or algo_ to relevant columns, as required by ISA
    merged_df.columns = [f'algo_{i}' if i.startswith('Coverage') else f'feature_{i}' if not i == 'TARGET_CLASS' else i for i in merged_df.columns]

    # rename class to INSTANCES, as required by ISA
    merged_df = merged_df.rename(columns={"TARGET_CLASS": "Instances"})

    old_df = merged_df
    merged_df = merged_df.drop_duplicates("Instances")
    print(f"Removed {old_df.shape[0] - merged_df.shape[0]} duplicate classes/rows")

    # Write the merged data to a new CSV file
    merged_filename = f"{current_dir}/merged_output.csv"
    merged_df.to_csv(merged_filename, index=False)

    print("\nMerged data written to", merged_filename)
