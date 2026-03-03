# Prompts Used for Key Data Element Extraction

## Zero-Shot Prompt

Read the following security document and identify all key data elements.
For each element provide its name and list all requirements associated with it.

Document:
{doc_text}

Format your response exactly like this:
element1:
  name: example name
  requirements:
    - requirement 1
    - requirement 2

## Few-Shot Prompt

Here are examples of key data elements from security documents:

Example 1:
element1:
  name: Password Policy
  requirements:
    - Passwords must be 8 or more characters
    - Passwords must contain uppercase letters
    - Passwords must expire every 90 days

Example 2:
element1:
  name: Access Control
  requirements:
    - Users must authenticate before access
    - Admins require multi factor authentication

Now do the same for this document:
{doc_text}

Format your response exactly like the examples above.

## Chain-of-Thought Prompt

Let us identify key data elements step by step.

Step 1: Read the document carefully
Step 2: Find any data or system that has security requirements around it
Step 3: For each element found list what requirements apply to it
Step 4: Format your answer as shown below

Document:
{doc_text}

Format your response exactly like this:
element1:
  name: example name
  requirements:
    - requirement 1
    - requirement 2