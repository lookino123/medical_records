# Century Health | ML Engineer Take Home Assignment

# Overview

For this assignment, you will receive a small, synthetic dataset of unstructured clinical notes. Your goal is to build a quick pipeline that:

1. **Extracts** specific clinical variables from the notes.
2. **Evaluates** the quality of the extraction.
3. **Outputs** a structured representation (e.g., JSON) with those key variables.

**Time expectation:** 2 hours 

# Data

[The linked excel file](https://docs.google.com/spreadsheets/d/1YdWhQwFehuXBveSaLEqw2QoQ3XEwSwrv/edit?usp=sharing&ouid=106734752345243548500&rtpof=true&sd=true) contains 20 unstructured clinical notes about patients with Type 2 Diabetes. Each note might contain:

- Demographics (fictitious age, gender).
- Key medications and dosages (e.g., metformin, insulin).
- Relevant labs (e.g., A1C levels).
- Brief mention of comorbidities (e.g., hypertension).
- Some “noise” text that isn’t relevant.

# Assignment Instructions

For speed and simplicity, write all your code in a Jupyter Notebook to show inputs and outputs. If easier to organize, feel free to write functions and prompts in a separate file to load in, but it is not required.

### Step 1: Extraction

1. Methodology 
    1. Identify which methodology you will use to solve this problem. Some examples include:
        1. Named Entity Recognition (NER)
        2. Question/ Answer
        3. Rule-Based Extraction
    2. For your methodology of choice, please explain why you chose this particular approach (or combination of approaches) and pros/ cons of different approaches.
2. Technical Setup 
    1. Based on your choice of methodology above, define your technical setup:
        1. Named Entity Recognition (NER)
            1. Use `spacy` and download a biomedical NLP model
            2. Fine-tune for extracting custom entities (e.g., medications, conditions, procedures) using a custom pipeline
        2. Question/ Answer
            1. [This linked OpenAI API key](https://drive.google.com/file/d/1CUa4NiCqicPilwjFkpVxR-6Cw9HtbrkV/view?usp=sharing) has has access to `4o-mini` and $5 in API calls. It should be sufficient for this exercise, but let us know if you do need access to more.
            2. Write one or more prompts in a way that the LLM outputs *only the relevant structured information*.
            3. For instance, you may want the LLM to return a JSON with fields like:
            
            ```jsx
            {
              "patient_name": "",
              "age": "",
              "disease": "",
              "medications": [],
              "lab_results": {},
              "symptoms": []
            }
            ```
            
            1. Demonstrate your *prompt engineering* approach. Example: few-shot examples, instructions to “only output JSON,” instructions to avoid extraneous text, etc.
        3. Rule-Based Extraction
            1. Define the RegEx needed to extract the variables of interest. 
            2. Note: You may want to incorporate RegEx to extract variables that NER or Question/ Answer have a tough time.
3. Process
    1. Named Entity Recognition (NER)
        1. Process NER model on your the clinical notes, extracting appropriate entities such as Name, Gender, Diagnoses, Medications, etc.
        2. Iterate on fine-tuning your NER model to bring in at least one custom entity, if needed.
        3. (Optional) Extract confidence scores for each variable extracted.
    2. Question/ Answer 
        1. Use LangChain, LlamaIndex, or a custom framework to demonstrate how to structure the prompts and calls.
        2. Show your pipeline from start to finish:
            1. Load or store your prompts using LangChain’s prompt templates, LlamaIndex’s prompt modules, or your own framework.
            2. Send requests to the LLM (OpenAI or other) through the chosen framework (e.g., `langchain.llms.OpenAI` or LlamaIndex’s `LLMPredictor`).
    3. Rule-Based Extraction
        1. Run RegEx on the clinical notes, extracting variables of interest.

### Step 2: Evaluation

1. Evaluation
    - **Structural evaluation**: Check if the returned text is valid JSON (or a valid structured format). Demonstrate how you handle parsing errors or invalid responses.
    - **Qualitative evaluation**: Manually or programmatically assess whether the extracted fields are correct. You can do one or more of the following:
        - Use a second LLM prompt to “judge” the correctness.
        - Or compare it against a simple “ground truth” you embed in your code. (Since this is synthetic data, you have a known correct answer.)

### Step 3: Output

1. Output
    - Return or print a final structured representation for each note (e.g., a Pandas DataFrame or a list of JSON objects).
    - (Optional) Briefly show how the structured data might be summarized. For example, “Generate a one-sentence summary for each patient highlighting their key risk factors.”

### Step 4: Summary

1. Short Summary
    - Summarize your approach:
        - How you arrived at your methodology and details.
        - How you are dealing with any “hallucinations” or extraneous text.
        - Why you chose the evaluation strategy you used.
    - Feel free to do this in the Jupyter notebook itself or a separate Markdown file.

# Rubric

We will be reviewing and assessing the following components:

- **Ability to translate business needs to an LLM problem**
    - Do you understand which clinical variables matter?
    - Are you structuring the output in a way that’s actually usable downstream?
- **Model Setup**
    - For NER, are you using the correct model and fine tuning it if needed
    - For Q&A, are you writing clear instructions to the model?
    - Do you handle unexpected LLM outputs or attempt to mitigate hallucinations?
- **Evaluation**
    - Do you implement a simple correctness check (structure + content)?
    - Can you explain how they would scale or improve the evaluation?
- **Code Quality & Reasoning**
    - Even if it’s a quick assignment, is the code organized?
    - Do they comment on potential pitfalls or limitations?

# Submission

Here are instructions for submitting the assignment:

- Upload your Jupyter notebook, associated files, and documentation to a Github repository
- Send an e-mail to [sanjay@century.health](mailto:sanjay@century.health) with the following information:
    - Title: “Century Health Technical Task - <First Name Last Name> - Submission”
    - A link to the repository
    - How many hours it took to complete the assignment end to end
    - Which AI tools did you use to help (e.g., ChatGPT, Cursor, Perplexity, etc.)

# Tips for Completing this Assignment

- **Leverage AI tools**: We encourage you to use AI-powered code generation tools like ChatGPT or Cursor to speed up development and improve clarity. At Century Health, we actively use these tools to enhance our workflows.
- **Simplify when needed**: If you encounter ambiguities, make reasonable assumptions that simplify rather than overcomplicate the problem and explain your reasoning. We're more interested in your thought process—how you decide which variables to extract, how you handle edge cases, and why you choose specific tools—rather than a single "correct" answer.
- **Timeboxing matters**: This assignment is designed to be completed in **under 2 hours**. If you find yourself far exceeding that, submit what you have along with a brief explanation of what you would improve with more time. We’re more interested in your approach than a fully polished solution.
- **Ask questions**: If anything is unclear, don’t hesitate to reach out to [sanjay@century.health](mailto:sanjay@century.health).