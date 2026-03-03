import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from task1_extractor.extractor import validate_inputs, extract_kdes, collect_llm_outputs, zero_shot_prompt, few_shot_prompt, chain_of_thought_prompt
from task2_comparator.comparator import compare_element_names, compare_requirements
from task3_executor.executor import determine_controls, run_kubescape, generate_csv

def run_pipeline(doc1_path, doc2_path):
    print("Validating inputs...")
    validate_inputs(doc1_path, doc2_path)

    print("Extracting key data elements from document 1...")
    kdes1, yaml1 = extract_kdes(doc1_path, zero_shot_prompt)

    print("Extracting key data elements from document 2...")
    kdes2, yaml2 = extract_kdes(doc2_path, zero_shot_prompt)

    print("Collecting all LLM outputs...")
    collect_llm_outputs(doc1_path, doc2_path)

    print("Comparing element names...")
    names_file = compare_element_names(yaml1, yaml2)

    print("Comparing requirements...")
    reqs_file = compare_requirements(yaml1, yaml2)

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