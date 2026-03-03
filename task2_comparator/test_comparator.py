import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task2_comparator.comparator import load_yaml_files, compare_element_names, compare_requirements

TEST_YAML1 = "outputs/test_yaml1.yaml"
TEST_YAML2 = "outputs/test_yaml2.yaml"
TEST_YAML_SAME = "outputs/test_yaml_same.yaml"

def setup_module():
    import yaml
    data1 = {
        "element1": {"name": "Password Policy", "requirements": ["Must be 8 characters", "Must have uppercase"]},
        "element2": {"name": "Access Control", "requirements": ["Must authenticate"]}
    }
    data2 = {
        "element1": {"name": "Password Policy", "requirements": ["Must be 8 characters"]},
        "element2": {"name": "Firewall Rules", "requirements": ["Must block port 22"]}
    }
    with open(TEST_YAML1, "w") as f:
        yaml.dump(data1, f)
    with open(TEST_YAML2, "w") as f:
        yaml.dump(data2, f)
    with open(TEST_YAML_SAME, "w") as f:
        yaml.dump(data1, f)

def test_load_yaml_files():
    yaml1, yaml2 = load_yaml_files(TEST_YAML1, TEST_YAML2)
    assert isinstance(yaml1, dict)
    assert isinstance(yaml2, dict)

def test_compare_element_names_differences():
    output_file = compare_element_names(TEST_YAML1, TEST_YAML2)
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
    assert "NO DIFFERENCES" not in content

def test_compare_requirements_no_differences():
    output_file = compare_requirements(TEST_YAML1, TEST_YAML_SAME)
    assert os.path.exists(output_file)
    with open(output_file, "r") as f:
        content = f.read()
    assert "NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS" in content