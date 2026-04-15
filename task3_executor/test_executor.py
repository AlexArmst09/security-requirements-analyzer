import pytest
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task3_executor.executor import load_text_files, determine_controls, run_kubescape, generate_csv

TEST_TEXT1 = "outputs/test_text1.txt"
TEST_TEXT2 = "outputs/test_text2.txt"
TEST_TEXT_NODIFF1 = "outputs/test_nodiff1.txt"
TEST_TEXT_NODIFF2 = "outputs/test_nodiff2.txt"

def setup_module():
    with open(TEST_TEXT1, "w") as f:
        f.write("Password Policy,Must be 8 characters\nAccess Control,Must authenticate")
    with open(TEST_TEXT2, "w") as f:
        f.write("Firewall Rules,Must block port 22")
    with open(TEST_TEXT_NODIFF1, "w") as f:
        f.write("NO DIFFERENCES IN REGARDS TO ELEMENT NAMES")
    with open(TEST_TEXT_NODIFF2, "w") as f:
        f.write("NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS")

def test_load_text_files():
    text1, text2 = load_text_files(TEST_TEXT1, TEST_TEXT2)
    assert isinstance(text1, str)
    assert isinstance(text2, str)

def test_determine_controls_no_differences():
    output_file = determine_controls(TEST_TEXT_NODIFF1, TEST_TEXT_NODIFF2)
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
    assert "NO DIFFERENCES FOUND" in content

def test_run_kubescape():
    with open("outputs/controls.txt", "w") as f:
        f.write("NO DIFFERENCES FOUND")
    if not os.path.exists("YAMLfiles"):
        os.makedirs("YAMLfiles")
    df = run_kubescape("outputs/controls.txt")
    assert isinstance(df, pd.DataFrame)

def test_generate_csv():
    df = pd.DataFrame([{
        "FilePath": "test.yaml",
        "Severity": "High",
        "Control name": "C-0007",
        "Failed resources": 1,
        "All Resources": 5,
        "Compliance score": 80
    }])
    output_file = generate_csv(df)
    assert os.path.exists(output_file)
    assert output_file.endswith(".csv")