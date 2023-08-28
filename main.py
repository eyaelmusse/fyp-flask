from flask import Flask, render_template, request, redirect
import os
import csv
import uuid
import pandas as pd
import zipfile
import cjdk
import subprocess

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        current_id = str(uuid.uuid4())
        current_dir = os.path.join("targ_files", current_id)
        os.mkdir(current_dir)

        pro_file = request.files['file']
        temp_file_path = os.path.join(current_dir, pro_file.filename)
        pro_file.save(temp_file_path)

        lib_provided = False
        try:
            lib_files = request.files['libFiles']
            lib_file_path = os.path.join(current_dir, 'lib.zip')
            lib_files.save(lib_file_path)
            with zipfile.ZipFile(lib_file_path, 'r') as zip_ref:
                zip_ref.extractall(current_dir)
                lib_provided = True
        except:
            pass

        ckjm_output = os.path.join(current_dir, "ckjm_output.txt")
        ckjm_command = ["java", "-jar", "runable-ckjm_ext-2.5.jar", temp_file_path]
        with cjdk.java_env(vendor="temurin-jre", version="17.0.3"):
            with open(ckjm_output, "w") as output_file:
                subprocess.run(ckjm_command, stdout=output_file, check=True)

        with open(os.path.join(current_dir, "ckjm_output.csv"), 'w') as ckjm_csv:
            writer = csv.writer(ckjm_csv)
            writer.writerow(("TARGET_CLASS", "WMC", "DIT", "NOC", "CBO", "RFC", "LCOM", "Ca", "Ce", "NPM", "LCOM3", "LOC",
                             "DAM", "MOA", "MFA", "CAM", "IC", "CBM", "AMC"))
            with open(os.path.join(current_dir, "ckjm_output.txt")) as in_file:
                stripped = (line.strip() for line in in_file)
                lines = (line.split(" ") for line in stripped if line)
                lines = (line for line in lines if line[0] != '~')
                writer.writerows(lines)

        # java8_home = "/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home"
        # java8 = f"{java8_home}/bin/java"
        # java8_tools = "/Library/Java/JavaVirtualMachines/jdk1.8.0_202.jdk/Contents/Home/lib/tools.jar"

        # os.environ["JAVA_HOME"] = java8_home
        # evosuite_comm = f"{java8} -jar evosuite-1.0.6.jar -target {temp_file_path} -criterion branch -Dreport_dir={current_dir} -Dtest_dir={current_dir}/tests -Dtools_jar_location={java8_tools} -Dshow_progress=false"
        # if lib_provided:
        #     evosuite_comm += f" -projectCP $(ls {current_dir}/lib/*.jar | tr '\n' ':')"
        # os.system(evosuite_comm)

        # evosuite_comm = f"  -Dtools_jar_location={java8_tools}"

        evo_command = ["java", "-jar", "evosuite-1.0.6.jar", "-target", temp_file_path, "-criterion", "branch", "-Dreport_dir={current_dir}", "-Dtest_dir={current_dir}/tests", "-Dshow_progress=false"]
        # if lib_provided:
        #     evo_command += f" -projectCP $(ls {current_dir}/lib/*.jar | tr '\n' ':')"
        with cjdk.java_env(vendor="temurin", version="8.0.372"):
            subprocess.run(evo_command, check=True)

        try:
            data1 = pd.read_csv(f'{current_dir}/statistics.csv')
        except:
            data1 = None
        data2 = pd.read_csv(f'{current_dir}/ckjm_output.csv')

        merged_output = pd.merge(data1, data2, on='TARGET_CLASS', how='outer')
        merged_output.to_csv(f'{current_dir}/merged_output.csv')

        return redirect(f"/result/{current_id}")


        return redirect("/")
    return render_template("home.html")


@app.route("/result/<id>")
def result(id):
    with open(f"targ_files/{id}/merged_output.csv") as file:
        reader = csv.reader(file)
        return render_template("result.html", csv=reader)

if __name__ == '__main__':
  app.run(port=8000)
