# Century Health | ML Engineer Take Home Assignment

# Data
the original notes from the physicians are on original_data.xlsx
Outputs are in final_results.csv

All intermediate checkpoints are in the folder named 'checkpoints'. They are the intermediate steps, saved in case of a Jupyter kernel crash.

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

I have not built a full verifier. However, since i have extracted the same data from 2 different LLMs, we do have a frame of reference and results can be assessed manually. The output with the comparison between the files in final_comparison.xlxs (some colums that are not relevant have been omitted)

How do the two models do:
In general Qwen massively outperformed ChatGPT, especially on the medication side. More specifically, it had less hallucinations, it was more able to ignore irrelevant information, missed less medications and was better able to distinguish between medications the patients were alrady one and new prescriptions.
This is not suprising since the version of qwen used is optimized to follow instructions, when chatgpt is optimized for text generation.

# How to improve the code

Load records to the LLM in batches (for speed)
Deploy Qwen over FastApi instead of the workstation of the data-scientist (practical, scalable)
Run a typo check on inputs.
Build a ClinicalBERT pipeline with spacy or Langchain as a substitute or verifier of the LLM.

