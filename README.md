# Century Health | ML Engineer Take Home Assignment

# Data
the original notes from the physicians are on notes.xlsx
structured outputs are in final.csv
all intermediate checkpoints are in the folder named 'checkpoints'. They are the intermediate steps, saved in case of a Jupyter kernel crash.

# Strategy
Load data in a pandas dataset, dump it in a csv checkpoint at every step.
Define extractors and extract all the structured demographic data like MR, Name, Age, Gender 
Define the fields that need to be extracted from the unstructured text and define the JSON structure expected of the LLM
Use LLM (in this case 2 different ones) to fill in the reuqeste fields
Compare results and optimize.

# Code
The code is in CH.ipynb. The need for multiple files/modules is reduced by the fact that Jupyter notebooks are in sections that clearly separate the code in logical blocks.

# Extraction of demographic data
I have chosen RegEx with fuzzy logic that allows for typos.
The code is case-insensitive.
The extraction process is not sensitive to new lines (\n) but there is a data cleanup step that is.This cleanup is optional and can be omitted in case new lines are unreliable.

It is also possible to use NER and LLMs to extract this data. NER and LLMs are more powerful tools than RegEx and work well when the data is less structured. The complexity of NER and LLM comes at a cost that in this case does not seem justified. This decision is affected by the quality of the data.
Better data => smaller model.

# Extraction of medical data

The medical data is not structured and cannot be easily extracted with RegEx.

Why not spacy?
Spacy pipelines are well established, fast and efficient. Historically they were rule-based and relied heavily on dictionaries or manually mapped features. Recently they have been adapted to include BERT transformers, that offer more accuracy, reliability and reduce reliance on dictionaries (at the cost of needing a GPU).

What's difficult about the spacy pipeline? Support on medspacy is patchy at best. scispacy is not much better. The rule-based models (CPU) require a dictionary or a set of rules (can be done manually on a limited domain, but not elegant nor very scalable). The BERT transformers available seem to have conflicts with certain versions torch and CUDA.

In short: great tool, requires a non-trivial setup. Ideal setup (technically complex) spacy + ClinicalBERT.

So I went the GPT way. GPT models (decoder) are designed to complete text, so they are not as specialized as BERT (encoder) at understanding meaning. However, they can do an excellent job and even if they are a blunt tool, they are a powerful and versatile one that reuires minimal setup.

I used 2 different LLMs.

Each Langchain pipeline has 3 parts: the prompt structure with JSON schema, the generation and the JSON validation.

json_schema = [
    ["disease", "The disease the patient is suffering from"],
    ["symptoms", "The symptoms the patient is experiencing"],
    ["lab_results", "The results of the lab tests"],
    ["current_medication", "The medication the patient is currently taking"],
    ["current_dosage", "The dosage of the current medication, just the dosage, not the name"],
    ["current_frequency", "The frequency of  current medication, just the frequency, not the name"],
    ["prescribed_medication", "The medication prescribed"],
    ["prescribed_dosage", "The dosage of the prescribed medication"],
    ["prescribed_frequency", "The frequency of the prescribed medication"],
]

This (almost) identical pipeline was run through ChatGPT-4o-mini (online) and though Qwen/Qwen2.5-32B-Instruct-GPTQ-Int4 (on metal on a local GPU)

I'd like to share some of the thought process behind benchmarking two different LLMs and the results:

Qwen/Qwen2.5-32B-Instruct-GPTQ-Int4 is a mid-sized model, it's a 32b, in its 4bit-quantized version it runs on 20Gb or VRAM. This means it is compatible with workstation hardware.

* Advantages of Qwen-32b

From a business standpoint this has two advantages:
1. Fine-tuning and LORA is possible and cheaper on smaller open source models. Fime-tuning can also create a techological moat
2. Regulations (national/international) might not allow the use of a US model / public model to process medical records

There are cases where the ability to run a model locally is valuable.

* Disadvantages of Qwen-32b

The difference between a naked model from HuggingFace and a service like ChatGPT is that the naked model is not a finished products and the layers of verification and output conditioning we are used to are not there.
More specifically, Qwen is subject to repetition and more effort has to be put in cleaning up and verifying the output.
A second obvious drawback is that, although the required infrastructure is cheaper, it still has to be managed nevertheless.

# Evaluation

I have not built a full verifier. However, since i have extracted the same data from 2 different LLMs, we do have a frame of reference and results can be assessed manually. The output with the comparison between the files in final.csv

How do the two models do:


# How to improve the code

Load records to the LLM in batches (for speed)
Deploy Qwen over FastApi instead of the workstation of the data-scientist (practical, scalable)
Run a typo check on inputs.
Build a ClinicalBERT pipeline with spacy or Langchain as a substitute or verifier of the LLM.

# Step 4: Summary

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