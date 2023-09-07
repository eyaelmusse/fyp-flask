from flask import Flask, render_template, request, redirect
import os
import csv
import uuid
import numpy as np
import pandas as pd
import zipfile
import cjdk
import subprocess
from enum import Enum
from scipy.stats.mstats import spearmanr

app = Flask(__name__)

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

    # Save the first column and remove it temporarily (first two if ck because type_ck
    columns_to_remove = set()

    if "type_ck" in dataframe:
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

    return df_filtered


def algorithm_spearman(dataframe, input_files):

    features = []
    algos = []

    for file_in in input_files:
        if file_in.data_type == DataType.FEATURE:
            features.append(dataframe.filter(regex=file_in.abb+"$"))
        elif file_in.data_type == DataType.ALGORITHM:
            algos.append(dataframe.filter(regex=file_in.abb+"$"))

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
            low_corr_column = [col for col, correlation in correlations if correlation < FEATURE_ALGO_CONSIDERATION]
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

            # If first column is not class
            if header_row[0] != "TARGET_CLASS":
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

            # Modify the feature dataframes based on Spearman's Correlation
            if file.data_type == DataType.FEATURE:
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

    merged_df = algorithm_spearman(merged_df, input_files)

    # Write the merged data to a new CSV file
    merged_filename = f"{current_dir}/merged_output.csv"
    merged_df.to_csv(merged_filename, index=False)


@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        current_id = str(uuid.uuid4())
        current_dir = os.path.join("targ_files", current_id)
        os.mkdir(current_dir)

        # save and extract project
        pro_file = request.files['file']
        temp_file_path = os.path.join(current_dir, pro_file.filename)
        pro_file.save(temp_file_path)
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            zip_ref.extractall(current_dir)

        proj_folder = os.path.join(current_dir, pro_file.filename[:-4])

        # compile
        compile_output = os.path.join(proj_folder, "compile_output")
        os.mkdir(compile_output)
        java_source_dir = f"{proj_folder}/src"
        dependencies = f"{proj_folder}/lib/*"

        java_files = []
        for root, _, files in os.walk(java_source_dir):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))

        if java_files:
            # try:
            with cjdk.java_env(vendor="temurin", version="8.0.372"):
                subprocess.run(["javac", "-cp", dependencies, "-d", compile_output] + java_files,
                               check=True)
                print("Compilation successful!")
            # except subprocess.CalledProcessError as e:
            #     print(f"Compilation failed: {e}")
        else:
            print(f"No Java files found")

        class_files = subprocess.check_output(['find', compile_output, '-name', '*.class'], text=True).split('\n')
        class_files = class_files[:-1]

        # ck
        ck_output = os.path.join(current_dir, "ck_output")
        os.mkdir(ck_output)
        use_jars = 'true'
        max_files_per_partition = '0'
        variables_and_field_metrics = 'False'
        ck_command = ["java", "-jar", "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar", proj_folder, use_jars,
                      max_files_per_partition, variables_and_field_metrics, ck_output + "/"]
        with cjdk.java_env(vendor="temurin-jre", version="17.0.3"):
            subprocess.run(ck_command, check=True)

        # javaparser
        jp_output = os.path.join(current_dir, "jp_output")
        os.mkdir(jp_output)
        jp_command = ["java", "-jar", "javaparser-extractor-1.0-SNAPSHOT-shaded.jar", proj_folder, jp_output + "/"]
        with cjdk.java_env(vendor="temurin-jre", version="18.0.1"):
            subprocess.run(jp_command, check=True)

        # ckjm
        ckjm_output = os.path.join(current_dir, "ckjm_output")
        os.mkdir(ckjm_output)
        ckjm_text = os.path.join(ckjm_output, "ckjm_output.txt")

        for class_file in class_files:
            try:
                ckjm_command = ["java", "-jar", "runable-ckjm_ext-2.5.jar", class_file]
                with cjdk.java_env(vendor="temurin-jre", version="17.0.3"):
                    with open(ckjm_text, "a") as output_file:
                        subprocess.run(ckjm_command, stdout=output_file, check=True)
            except:
                pass

        with open(os.path.join(ckjm_output, "ckjm_output.csv"), 'w') as ckjm_csv:
            writer = csv.writer(ckjm_csv)
            writer.writerow(("TARGET_CLASS", "WMC", "DIT", "NOC", "CBO", "RFC", "LCOM", "Ca", "Ce", "NPM", "LCOM3", "LOC",
                             "DAM", "MOA", "MFA", "CAM", "IC", "CBM", "AMC"))
            with open(os.path.join(ckjm_output, "ckjm_output.txt")) as in_file:
                stripped = (line.strip() for line in in_file)
                lines = (line.split(" ") for line in stripped if line)
                lines = (line for line in lines if line[0] != '~')
                writer.writerows(lines)


        # evosuite
        evo_output = os.path.join(current_dir, "evo_output")
        os.mkdir(evo_output)

        evo_command = ["java", "-jar", "evosuite-1.0.6.jar", "-target", compile_output, "-criterion", "branch",
                       f"-Dreport_dir={evo_output}", f"-Dtest_dir={evo_output}/tests", "-Dshow_progress=false"]

        jar_files = [file for file in os.listdir(f"{proj_folder}/lib") if file.endswith('.jar')]
        if len(jar_files) != 0:
            jar_path = ":".join(os.path.join(f"{proj_folder}/lib", jar) for jar in jar_files)
            print("jar_path", jar_path)
            evo_command.append("-projectCP")
            evo_command.append(jar_path)

        with cjdk.java_env(vendor="temurin", version="8.0.372"):
            subprocess.run(evo_command, check=True)


        # Output
        ck_class_filename = os.path.join(ck_output, 'class.csv')
        ckjm_filename = os.path.join(ckjm_output, 'ckjm_output.csv')
        jp_filename = next((f for f in os.listdir(jp_output) if f.endswith('_javaparser.csv')), None)
        if jp_filename is None:
            raise FileNotFoundError("JavaParser CSV file not found in the current directory.")

        evo1_filename = os.path.join(evo_output, 'statistics.csv')

        # List of input files
        input_files = [
            DataInfo("CK", ck_class_filename, "ck", DataType.FEATURE),
            DataInfo("Javaparser", jp_filename, "jp", DataType.FEATURE),
            DataInfo("CKJM", ckjm_filename, "ckjm", DataType.FEATURE),
            DataInfo("Evosuite_DYNAMOSA", evo1_filename, "DYNAMOSA", DataType.ALGORITHM)
            # DataInfo("Evosuite_Random", evo2_filename, "rand", DataType.ALGORITHM),
            # DataInfo("Evosuite_MIO", "evo_mio.csv", "mio", DataType.ALGORITHM),
        ]

        read_output(input_files, current_dir)

        return redirect(f"/result/{current_id}")
    return render_template("home.html")


@app.route("/result/<id>")
def result(id):
    with open(f"targ_files/{id}/merged_output.csv") as file:
        reader = csv.reader(file)
        return render_template("result.html", csv=reader)

import matlab.engine

@app.route("/matlab")
def matlab():
    eng = matlab.engine.start_matlab()
    eng.run_file("my_matlab_script.m")
    eng.quit()

if __name__ == '__main__':
  app.run(port=8000)
