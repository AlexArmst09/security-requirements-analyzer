import yaml
import os

def load_yaml_files(yaml1_path, yaml2_path):
    for path in [yaml1_path, yaml2_path]:
        if not os.path.exists(path):
            raise FileNotFoundError("File not found: " + path)
    with open(yaml1_path, "r") as f:
        yaml1 = yaml.safe_load(f)
    with open(yaml2_path, "r") as f:
        yaml2 = yaml.safe_load(f)
    return yaml1, yaml2

def compare_element_names(yaml1_path, yaml2_path):
    yaml1, yaml2 = load_yaml_files(yaml1_path, yaml2_path)

    names1 = set(v["name"] for v in yaml1.values() if "name" in v)
    names2 = set(v["name"] for v in yaml2.values() if "name" in v)

    differences = names1.symmetric_difference(names2)

    output_file = "outputs/element_name_differences.txt"
    with open(output_file, "w") as f:
        if differences:
            for name in differences:
                f.write(name + "\n")
        else:
            f.write("NO DIFFERENCES IN REGARDS TO ELEMENT NAMES")

    return output_file

def compare_requirements(yaml1_path, yaml2_path):
    yaml1, yaml2 = load_yaml_files(yaml1_path, yaml2_path)

    reqs1 = {}
    reqs2 = {}

    for v in yaml1.values():
        if "name" in v and "requirements" in v:
            reqs1[v["name"]] = set(v["requirements"])

    for v in yaml2.values():
        if "name" in v and "requirements" in v:
            reqs2[v["name"]] = set(v["requirements"])

    differences = []
    all_names = set(reqs1.keys()).union(set(reqs2.keys()))

    yaml1_name = os.path.basename(yaml1_path)
    yaml2_name = os.path.basename(yaml2_path)

    for name in all_names:
        in_yaml1 = name in reqs1
        in_yaml2 = name in reqs2

        if in_yaml1 and not in_yaml2:
            differences.append(name + ",ABSENT-IN-" + yaml2_name + ",PRESENT-IN-" + yaml1_name + ",NA")
        elif in_yaml2 and not in_yaml1:
            differences.append(name + ",ABSENT-IN-" + yaml1_name + ",PRESENT-IN-" + yaml2_name + ",NA")
        else:
            r1 = reqs1.get(name, set())
            r2 = reqs2.get(name, set())
            only_in_r1 = r1 - r2
            only_in_r2 = r2 - r1
            for req in only_in_r1:
                differences.append(name + ",ABSENT-IN-" + yaml2_name + ",PRESENT-IN-" + yaml1_name + "," + req)
            for req in only_in_r2:
                differences.append(name + ",ABSENT-IN-" + yaml1_name + ",PRESENT-IN-" + yaml2_name + "," + req)

    output_file = "outputs/requirement_differences.txt"
    with open(output_file, "w") as f:
        if differences:
            for line in differences:
                f.write(line + "\n")
        else:
            f.write("NO DIFFERENCES IN REGARDS TO ELEMENT REQUIREMENTS")

    return output_file