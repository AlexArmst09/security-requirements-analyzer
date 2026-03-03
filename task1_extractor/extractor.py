import fitz
import yaml
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "google/gemma-3-1b-it"
tokenizer = None
model = None

def load_model():
    global tokenizer, model
    if model is None:
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, torch_dtype=torch.float32)

def validate_inputs(doc1_path, doc2_path):
    for path in [doc1_path, doc2_path]:
        if not os.path.exists(path):
            raise FileNotFoundError("File not found: " + path)
        if not path.endswith(".pdf"):
            raise ValueError("File is not a PDF: " + path)
    return True

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text[:3000]

def zero_shot_prompt(doc_text):
    return (
        "Read the following security document and identify all key data elements.\n"
        "For each element provide its name and list all requirements associated with it.\n\n"
        "Document:\n"
        + doc_text +
        "\n\nFormat your response exactly like this:\n"
        "element1:\n"
        "  name: example name\n"
        "  requirements:\n"
        "    - requirement 1\n"
        "    - requirement 2"
    )

def few_shot_prompt(doc_text):
    return (
        "Here are examples of key data elements from security documents:\n\n"
        "Example 1:\n"
        "element1:\n"
        "  name: Password Policy\n"
        "  requirements:\n"
        "    - Passwords must be 8 or more characters\n"
        "    - Passwords must contain uppercase letters\n"
        "    - Passwords must expire every 90 days\n\n"
        "Example 2:\n"
        "element1:\n"
        "  name: Access Control\n"
        "  requirements:\n"
        "    - Users must authenticate before access\n"
        "    - Admins require multi factor authentication\n\n"
        "Now do the same for this document:\n"
        + doc_text +
        "\n\nFormat your response exactly like the examples above."
    )

def chain_of_thought_prompt(doc_text):
    return (
        "Let us identify key data elements step by step.\n\n"
        "Step 1: Read the document carefully\n"
        "Step 2: Find any data or system that has security requirements around it\n"
        "Step 3: For each element found list what requirements apply to it\n"
        "Step 4: Format your answer as shown below\n\n"
        "Document:\n"
        + doc_text +
        "\n\nFormat your response exactly like this:\n"
        "element1:\n"
        "  name: example name\n"
        "  requirements:\n"
        "    - requirement 1\n"
        "    - requirement 2"
    )

def run_llm(prompt):
    load_model()
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=512)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

def parse_llm_output(llm_output):
    elements = {}
    lines = llm_output.split("\n")
    current_element = None
    in_requirements = False
    count = 1

    for line in lines:
        line = line.strip()
        if line.startswith("name:"):
            name = line.replace("name:", "").strip()
            key = "element" + str(count)
            elements[key] = {"name": name, "requirements": []}
            current_element = key
            in_requirements = False
            count += 1
        elif line == "requirements:" and current_element:
            in_requirements = True
        elif line.startswith("- ") and in_requirements and current_element:
            elements[current_element]["requirements"].append(line[2:])

    if not elements:
        elements["element1"] = {"name": "Unknown", "requirements": [llm_output[:200]]}

    return elements

def extract_kdes(doc_path, prompt_func):
    text = extract_text_from_pdf(doc_path)
    prompt = prompt_func(text)
    llm_output = run_llm(prompt)
    kdes = parse_llm_output(llm_output)

    doc_name = os.path.basename(doc_path).replace(".pdf", "")
    prompt_type = prompt_func.__name__.replace("_prompt", "")
    yaml_filename = "outputs/" + doc_name + "-" + prompt_type + "-kdes.yaml"

    with open(yaml_filename, "w") as f:
        yaml.dump(kdes, f, default_flow_style=False)

    return kdes, yaml_filename

def collect_llm_outputs(doc1_path, doc2_path):
    load_model()
    prompt_funcs = [zero_shot_prompt, few_shot_prompt, chain_of_thought_prompt]
    prompt_types = ["zero-shot", "few-shot", "chain-of-thought"]
    results = []

    for doc_path in [doc1_path, doc2_path]:
        text = extract_text_from_pdf(doc_path)
        for prompt_func, prompt_type in zip(prompt_funcs, prompt_types):
            prompt = prompt_func(text)
            llm_output = run_llm(prompt)
            results.append((prompt_type, prompt, llm_output))

    output_file = "outputs/llm_outputs.txt"
    with open(output_file, "w") as f:
        for prompt_type, prompt, llm_output in results:
            f.write("*LLM Name*\n" + MODEL_NAME + "\n\n")
            f.write("*Prompt Used*\n" + prompt + "\n\n")
            f.write("*Prompt Type*\n" + prompt_type + "\n\n")
            f.write("*LLM Output*\n" + llm_output + "\n\n")
            f.write("=" * 50 + "\n\n")

    return output_file