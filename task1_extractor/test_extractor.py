import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from task1_extractor.extractor import validate_inputs, zero_shot_prompt, few_shot_prompt, chain_of_thought_prompt, extract_kdes, collect_llm_outputs

def test_validate_inputs():
    with pytest.raises(FileNotFoundError):
        validate_inputs("fake.pdf", "fake2.pdf")

def test_zero_shot_prompt():
    result = zero_shot_prompt("test document text")
    assert isinstance(result, str)
    assert len(result) > 0

def test_few_shot_prompt():
    result = few_shot_prompt("test document text")
    assert isinstance(result, str)
    assert len(result) > 0

def test_chain_of_thought_prompt():
    result = chain_of_thought_prompt("test document text")
    assert isinstance(result, str)
    assert len(result) > 0

def test_extract_kdes():
    kdes, yaml_file = extract_kdes("pdfs/cis-r1.pdf", zero_shot_prompt)
    assert isinstance(kdes, dict)
    assert os.path.exists(yaml_file)

def test_collect_llm_outputs():
    output_file = collect_llm_outputs("pdfs/cis-r1.pdf", "pdfs/cis-r2.pdf")
    assert os.path.exists(output_file)