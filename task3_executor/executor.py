import os
import subprocess
import pandas as pd

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

def run_kubescape(controls_file, yamls_path="project-yamls"):
    if not os.path.exists(controls_file):
        raise FileNotFoundError("Controls file not found: " + controls_file)

    with open(controls_file, "r") as f:
        content = f.read().strip()

    if content == "NO DIFFERENCES FOUND":
        cmd = ["kubescape", "scan", yamls_path, "--format", "json", "--output", "outputs/kubescape_results.json"]
    else:
        controls = [line.strip() for line in content.split("\n") if line.strip()]
        controls_str = ",".join(controls)
        cmd = ["kubescape", "scan", "control", controls_str, yamls_path, "--format", "json", "--output", "outputs/kubescape_results.json"]

    subprocess.run(cmd)

    results = parse_kubescape_output("outputs/kubescape_results.json")
    return