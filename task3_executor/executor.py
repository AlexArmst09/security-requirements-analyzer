import os
import subprocess
import pandas as pd
import json

def load_text_files(text1_path, text2_path):
    for path in [text1_path, text2_path]:
        if not os.path.exists(path):
            raise FileNotFoundError("File not found: " + path)
    with open(text1_path, "r") as f:
        text1 = f.read()
    with open(text2_path, "r") as f:
        text2 = f.read()
    return text1, text2

def determine_controls(text1_path, text2_path):
    text1, text2 = load_text_files(text1_path, text2_path)
    no_diff1 = "NO DIFFERENCES" in text1
    no_diff2 = "NO DIFFERENCES" in text2
    output_file = "outputs/controls.txt"
    if no_diff1 and no_diff2:
        with open(output_file, "w") as f:
            f.write("NO DIFFERENCES FOUND")
        return output_file
    keyword_to_controls = {
        "password": ["C-0007", "C-0026"],
        "access": ["C-0001", "C-0002"],
        "network": ["C-0021", "C-0035"],
        "firewall": ["C-0021"],
        "encryption": ["C-0066"],
        "authentication": ["C-0007", "C-0001"],
        "logging": ["C-0024"],
        "audit": ["C-0024"],
        "privilege": ["C-0002"],
        "patch": ["C-0030"],
    }
    combined_text = (text1 + text2).lower()
    matched_controls = set()
    for keyword, controls in keyword_to_controls.items():
        if keyword in combined_text:
            for control in controls:
                matched_controls.add(control)
    with open(output_file, "w") as f:
        if matched_controls:
            for control in matched_controls:
                f.write(control + "\n")
        else:
            f.write("NO DIFFERENCES FOUND")
    return output_file

def run_kubescape(controls_file, yamls_path="YAMLfiles"):
    kubescape_path = os.path.expanduser("~/.kubescape/bin/kubescape")
    if not os.path.exists(controls_file):
        raise FileNotFoundError("Controls file not found: " + controls_file)
    with open(controls_file, "r") as f:
        content = f.read().strip()
    if content == "NO DIFFERENCES FOUND":
        cmd = [kubescape_path, "scan", yamls_path, "--format", "json", "--output", "outputs/kubescape_results.json"]
    else:
        controls = [line.strip() for line in content.split("\n") if line.strip()]
        controls_str = ",".join(controls)
        cmd = [kubescape_path, "scan", "control", controls_str, yamls_path, "--format", "json", "--output", "outputs/kubescape_results.json"]
    subprocess.run(cmd)
    results = parse_kubescape_output("outputs/kubescape_results.json")
    return results

def parse_kubescape_output(json_file):
    if not os.path.exists(json_file):
        return pd.DataFrame(columns=["FilePath", "Severity", "Control name", "Failed resources", "All Resources", "Compliance score"])
    with open(json_file, "r") as f:
        content = f.read().strip()
    if not content:
        return pd.DataFrame([{
            "FilePath": "N/A",
            "Severity": "N/A",
            "Control name": "N/A",
            "Failed resources": 0,
            "All Resources": 0,
            "Compliance score": 0
        }])
    data = json.loads(content)
    rows = []
    results = data.get("results", [])
    for result in results:
        control_name = result.get("controlID", "Unknown")
        severity = result.get("severity", {}).get("severity", "Unknown")
        failed = result.get("summary", {}).get("failedResources", 0)
        total = result.get("summary", {}).get("allResources", 0)
        score = result.get("summary", {}).get("complianceScore", 0)
        resources = result.get("resourcesResult", {})
        for filepath in resources.keys():
            rows.append({
                "FilePath": filepath,
                "Severity": severity,
                "Control name": control_name,
                "Failed resources": failed,
                "All Resources": total,
                "Compliance score": score
            })
    if not rows:
        rows.append({
            "FilePath": "N/A",
            "Severity": "N/A",
            "Control name": "N/A",
            "Failed resources": 0,
            "All Resources": 0,
            "Compliance score": 0
        })
    return pd.DataFrame(rows)

def generate_csv(dataframe):
    output_file = "outputs/kubescape_results.csv"
    dataframe.to_csv(output_file, index=False)
    return output_file
