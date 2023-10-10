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
from FinalMerge import read_output, DataInfo, DataType
from NetworkXScript import parse_cfg, merge_javaparser

app = Flask(__name__)



def merge_files(current_dir):
    # # Output
    ck_class_filename = os.path.join(current_dir, "ck_output", 'class.csv')
    ckjm_filename = os.path.join(current_dir, "ckjm_output", 'ckjm_output.csv')

    jp_output = os.path.join(current_dir, "jp_output")
    jp_filename = next((f for f in os.listdir(jp_output) if f.endswith('_javaparser.csv')), None)
    if jp_filename is None:
        raise FileNotFoundError("JavaParser CSV file not found in the current directory.")
    # evo1_filename = os.path.join(current_dir, "evosuite-report", 'statistics.csv')


    # List of input files
    # input_files = [
    #     # DataInfo("Javaparser", jp_filename, "jp", DataType.FEATURE),  # javaparser is merged with networkx data
    #     DataInfo("Javaparser-NetworkX", "jpnX.csv", "jpnX", DataType.FEATURE),
    # ]
    input_files = [
        DataInfo("CK", ck_class_filename, "ck", DataType.FEATURE),
        DataInfo("Javaparser", os.path.join(jp_output, jp_filename), "jp", DataType.FEATURE),
        DataInfo("CKJM", ckjm_filename, "ckjm", DataType.FEATURE),
        # DataInfo("Evosuite_DYNAMOSA", evo1_filename, "DYNAMOSA", DataType.ALGORITHM)
        # DataInfo("Evosuite_Random", evo2_filename, "rand", DataType.ALGORITHM),
        # DataInfo("Evosuite_MIO", "evo_mio.csv", "mio", DataType.ALGORITHM),
    ]

    read_output(input_files, current_dir)

def unzip_project(current_dir, pro_file):
    # save and extract project
    temp_file_path = os.path.join(current_dir, pro_file.filename)
    pro_file.save(temp_file_path)
    with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
        zip_ref.extractall(current_dir)

    proj_folder = os.path.join(current_dir, pro_file.filename[:-4])

    # compile
    compile_output = os.path.join(proj_folder, "compile_output")
    os.mkdir(compile_output)
    java_source_dir = f"{proj_folder}/src/main"
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

def extract_metrics(current_dir, proj_folder):
    compile_output = os.path.join(proj_folder, "compile_output")
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

def run_evosuite(current_dir, pro_filename):
    os.chdir(current_dir)
    compile_output = os.path.join(pro_filename, "compile_output")

    evo_command = ["java", "-jar", "../../evosuite-1.0.6.jar", "-target", compile_output, "-criterion", "branch",
                   "-Dshow_progress=false", "-Dwrite_cfg=true", "-Dsearch_budget=1", "-Dsandbox=false",
                   "-generateRandom", "-inheritanceTree"]

    jar_files = [file for file in os.listdir(f"{pro_filename}/lib") if file.endswith('.jar')]
    if len(jar_files) != 0:
        jar_path = ":".join(os.path.join(f"{pro_filename}/lib", jar) for jar in jar_files)
        print("jar_path", jar_path)
        evo_command.append("-projectCP")
        evo_command.append(jar_path)

    with cjdk.java_env(vendor="temurin", version="8.0.372"):
        subprocess.run(evo_command, check=True)
    os.chdir('../../')

@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        current_id = str(uuid.uuid4())
        current_dir = os.path.join("targ_files", current_id)
        os.mkdir(current_dir)
        pro_file = request.files['file']
        unzip_project(current_dir, pro_file)

        proj_folder = os.path.join(current_dir, pro_file.filename[:-4])
        extract_metrics(current_dir, proj_folder)
        run_evosuite(current_dir, pro_file.filename[:-4])

        parse_cfg(current_dir)
        merge_javaparser(current_dir)

        merge_files(current_dir)

        # return redirect(f"/result/{current_id}")
        return redirect(f"/")
    return render_template("home.html")


@app.route("/index")
def index():
    return render_template("index.html")


@app.route("/result/<id>")
def result(id):
    with open(f"targ_files/{id}/merged_output.csv") as file:
        reader = csv.reader(file)
        return render_template("result.html", csv=reader)

if __name__ == '__main__':
    app.run(port=8001)
