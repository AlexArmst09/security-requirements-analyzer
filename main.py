import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from task1_extractor.extractor import validate_inputs, extract_kdes, collect_llm_outputs, zero_shot_prompt, few_shot_prompt, chain_of_thought_prompt
from task2_comparator.comparator import compare_element_names, compare_requirements
from task3_executor.executor import determine_controls, run_kubescape, generate_csv

def run_pipeline(doc1_path, doc2_path):
    print("Validating inputs...")
    validate_inputs(doc1_path, doc2_path)

    print("Extracting KDEs from doc1 using zero shot...")
    kdes1_zs, yaml1_zs = extract_kdes(doc1_path, doc2_path, zero_shot_prompt)

    print("Extracting KDEs from doc1 using few shot...")
    kdes1_fs, yaml1_fs = extract_kdes(doc1_path, doc2_path, few_shot_prompt)

    print("Extracting KDEs from doc1 using chain of thought...")
    kdes1_cot, yaml1_cot = extract_kdes(doc1_path, doc2_path, chain_of_thought_prompt)

    print("Extracting KDEs from doc2 using zero shot...")
    kdes2_zs, yaml2_zs = extract_kdes(doc2_path, doc1_path, zero_shot_prompt)

    print("Extracting KDEs from doc2 using few shot...")
    kdes2_fs, yaml2_fs = extract_kdes(doc2_path, doc1_path, few_shot_prompt)

    print("Extracting KDEs from doc2 using chain of thought...")
    kdes2_cot, yaml2_cot = extract_kdes(doc2_path, doc1_path, chain_of_thought_prompt)

    print("Collecting all LLM outputs...")
    collect_llm_outputs(doc1_path, doc2_path)

    print("Comparing element names...")
    names_file = compare_element_names(yaml1_zs, yaml2_zs)

    print("Comparing requirements...")
    reqs_file = compare_requirements(yaml1_zs, yaml2_zs)

    print("Determining Kubescape controls...")
    controls_file = determine_controls(names_file, reqs_file)

    print("Running Kubescape...")
    df = run_kubescape(controls_file)

    print("Generating CSV...")
    csv_file = generate_csv(df)

    print("Done! Results saved to: " + csv_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python main.py <doc1.pdf> <doc2.pdf>")
        sys.exit(1)

    doc1 = sys.argv[1]
    doc2 = sys.argv[2]
    run_pipeline(doc1, doc2)