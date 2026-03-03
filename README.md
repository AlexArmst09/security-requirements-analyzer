# Security Requirements Analyzer

## Team Members

| Alex Armstrong | 904251294 | aha0022@auburn.edu |

## LLM Used
Gemma-3-1B (google/gemma-3-1b-it)

## How to Run

### Setup
```bash
python3 -m venv comp5700-venv
source comp5700-venv/bin/activate
pip install -r requirements.txt
```

### Run the program
```bash
python main.py pdfs/cis-r1.pdf pdfs/cis-r2.pdf
```

### Run the tests
```bash
pytest task1_extractor/test_extractor.py
pytest task2_comparator/test_comparator.py
pytest task3_executor/test_executor.py
```

## Input Combinations
- Input-1: cis-r1.pdf and cis-r1.pdf
- Input-2: cis-r1.pdf and cis-r2.pdf
- Input-3: cis-r1.pdf and cis-r3.pdf
- Input-4: cis-r1.pdf and cis-r4.pdf
- Input-5: cis-r2.pdf and cis-r2.pdf
- Input-6: cis-r2.pdf and cis-r3.pdf
- Input-7: cis-r2.pdf and cis-r4.pdf
- Input-8: cis-r3.pdf and cis-r3.pdf
- Input-9: cis-r3.pdf and cis-r4.pdf

## Project Structure
```
security-requirements-analyzer/
├── task1_extractor/
│   ├── extractor.py
│   └── test_extractor.py
├── task2_comparator/
│   ├── comparator.py
│   └── test_comparator.py
├── task3_executor/
│   ├── executor.py
│   └── test_executor.py
├── outputs/
├── pdfs/
├── PROMPT.md
├── README.md
├── requirements.txt
└── main.py
```