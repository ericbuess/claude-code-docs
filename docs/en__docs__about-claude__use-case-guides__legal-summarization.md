# Legal summarization

> This guide walks through how to leverage Claude's advanced natural language processing capabilities to efficiently summarize legal documents, extracting key information and expediting legal research. With Claude, you can streamline the review of contracts, litigation prep, and regulatory work, saving time and ensuring accuracy in your legal processes.

> Visit our [summarization cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb) to see an example legal summarization implementation using Claude.

## Before building with Claude

### Decide whether to use Claude for legal summarization

Here are some key indicators that you should employ an LLM like Claude to summarize legal documents:

<AccordionGroup>
  <Accordion title="You want to review a high volume of documents efficiently and affordably">Large-scale document review can be time-consuming and expensive when done manually. Claude can process and summarize vast amounts of legal documents rapidly, significantly reducing the time and cost associated with document review. This capability is particularly valuable for tasks like due diligence, contract analysis, or litigation discovery, where efficiency is crucial.</Accordion>
  <Accordion title="You require automated extraction of key metadata">Claude can efficiently extract and categorize important metadata from legal documents, such as parties involved, dates, contract terms, or specific clauses. This automated extraction can help organize information, making it easier to search, analyze, and manage large document sets. It's especially useful for contract management, compliance checks, or creating searchable databases of legal information. </Accordion>
  <Accordion title="You want to generate clear, concise, and standardized summaries">Claude can generate structured summaries that follow predetermined formats, making it easier for legal professionals to quickly grasp the key points of various documents. These standardized summaries can improve readability, facilitate comparison between documents, and enhance overall comprehension, especially when dealing with complex legal language or technical jargon.</Accordion>
  <Accordion title="You need precise citations for your summaries">When creating legal summaries, proper attribution and citation are crucial to ensure credibility and compliance with legal standards. Claude can be prompted to include accurate citations for all referenced legal points, making it easier for legal professionals to review and verify the summarized information.</Accordion>
  <Accordion title="You want to streamline and expedite your legal research process">Claude can assist in legal research by quickly analyzing large volumes of case law, statutes, and legal commentary. It can identify relevant precedents, extract key legal principles, and summarize complex legal arguments. This capability can significantly speed up the research process, allowing legal professionals to focus on higher-level analysis and strategy development.</Accordion>
</AccordionGroup>

### Determine the details you want the summarization to extract

There is no single correct summary for any given document. Without clear direction, it can be difficult for Claude to determine which details to include. To achieve optimal results, identify the specific information you want to include in the summary.

For instance, when summarizing a sublease agreement, you might wish to extract the following key points:

```python  theme={null}
details_to_extract = [
    'Parties involved (sublessor, sublessee, and original lessor)',
    'Property details (address, description, and permitted use)', 
    'Term and rent (start date, end date, monthly rent, and security deposit)',
    'Responsibilities (utilities, maintenance, and repairs)',
    'Consent and notices (landlord\'s consent, and notice requirements)',
    'Special provisions (furniture, parking, and subletting restrictions)'
]
```

### Establish success criteria

Evaluating the quality of summaries is a notoriously challenging task. Unlike many other natural language processing tasks, evaluation of summaries often lacks clear-cut, objective metrics. The process can be highly subjective, with different readers valuing different aspects of a summary. Here are criteria you may wish to consider when assessing how well Claude performs legal summarization.

<AccordionGroup>
  <Accordion title="Factual correctness">The summary should accurately represent the facts, legal concepts, and key points in the document.</Accordion>
  <Accordion title="Legal precision">Terminology and references to statutes, case law, or regulations must be correct and aligned with legal standards.</Accordion>
  <Accordion title="Conciseness"> The summary should condense the legal document to its essential points without losing important details.</Accordion>
  <Accordion title="Consistency">If summarizing multiple documents, the LLM should maintain a consistent structure and approach to each summary.</Accordion>
  <Accordion title="Readability">The text should be clear and easy to understand. If the audience is not legal experts, the summarization should not include legal jargon that could confuse the audience.</Accordion>
  <Accordion title="Bias and fairness">The summary should present an unbiased and fair depiction of the legal arguments and positions.</Accordion>
</AccordionGroup>

See our guide on [establishing success criteria](/en/docs/test-and-evaluate/define-success) for more information.

***

## How to summarize legal documents using Claude

### Select the right Claude model

Model accuracy is extremely important when summarizing legal documents. Claude Sonnet 4.5 is an excellent choice for use cases such as this where high accuracy is required. If the size and quantity of your documents is large such that costs start to become a concern, you can also try using a smaller model like Claude Haiku 4.5.

To help estimate these costs, below is a comparison of the cost to summarize 1,000 sublease agreements using both Sonnet and Haiku:

* **Content size**
  * Number of agreements: 1,000
  * Characters per agreement: 300,000
  * Total characters: 300M

* **Estimated tokens**
  * Input tokens: 86M (assuming 1 token per 3.5 characters)
  * Output tokens per summary: 350
  * Total output tokens: 350,000

* **Claude Sonnet 4.5 estimated cost**
  * Input token cost: 86 MTok \* \$3.00/MTok = \$258
  * Output token cost: 0.35 MTok \* \$15.00/MTok = \$5.25
  * Total cost: \$258.00 + \$5.25 = \$263.25

* **Claude Haiku 3 estimated cost**
  * Input token cost: 86 MTok \* \$0.25/MTok = \$21.50
  * Output token cost: 0.35 MTok \* \$1.25/MTok = \$0.44
  * Total cost: \$21.50 + \$0.44 = \$21.96

<Tip>Actual costs may differ from these estimates. These estimates are based on the example highlighted in the section on [prompting](#build-a-strong-prompt).</Tip>

### Transform documents into a format that Claude can process

Before you begin summarizing documents, you need to prepare your data. This involves extracting text from PDFs, cleaning the text, and ensuring it's ready to be processed by Claude.

Here is a demonstration of this process on a sample pdf:

```python  theme={null}
from io import BytesIO
import re

import pypdf
import requests

def get_llm_text(pdf_file):
    reader = pypdf.PdfReader(pdf_file)
    text = "\n".join([page.extract_text() for page in reader.pages])

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text) 

    # Remove page numbers
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text) 

    return text


# Create the full URL from the GitHub repository
url = "https://raw.githubusercontent.com/anthropics/anthropic-cookbook/main/skills/summarization/data/Sample Sublease Agreement.pdf"
url = url.replace(" ", "%20")

# Download the PDF file into memory
response = requests.get(url)

# Load the PDF from memory
pdf_file = BytesIO(response.content)

document_text = get_llm_text(pdf_file) 
print(document_text[:50000]) 
```

In this example, we first download a pdf of a sample sublease agreement used in the [summarization cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/data/Sample%20Sublease%20Agreement.pdf). This agreement was sourced from a publicly available sublease agreement from the [sec.gov website](https://www.sec.gov/Archives/edgar/data/1045425/000119312507044370/dex1032.htm).

We use the pypdf library to extract the contents of the pdf and convert it to text. The text data is then cleaned by removing extra whitespace and page numbers.

### Build a strong prompt

Claude can adapt to various summarization styles. You can change the details of the prompt to guide Claude to be more or less verbose, include more or less technical terminology, or provide a higher or lower level summary of the context at hand.

Here’s an example of how to create a prompt that ensures the generated summaries follow a consistent structure when analyzing sublease agreements:

```python  theme={null}
import anthropic

# Initialize the Anthropic client
client = anthropic.Anthropic()

def summarize_document(text, details_to_extract, model="claude-sonnet-4-5", max_tokens=1000):

    # Format the details to extract to be placed within the prompt's context
    details_to_extract_str = '\n'.join(details_to_extract)
    
    # Prompt the model to summarize the sublease agreement
    prompt = f"""Summarize the following sublease agreement. Focus on these key aspects:

    {details_to_extract_str}

    Provide the summary in bullet points nested within the XML header for each section. For example:

    <parties involved>
    - Sublessor: [Name]
    // Add more details as needed
    </parties involved>
    
    If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.

    Sublease agreement text:
    {text}
    """

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="You are a legal analyst specializing in real estate law, known for highly accurate and detailed summaries of sublease agreements.",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "Here is the summary of the sublease agreement: <summary>"}
        ],
        stop_sequences=["</summary>"]
    )

    return response.content[0].text

sublease_summary = summarize_document(document_text, details_to_extract)
print(sublease_summary)
```

This code implements a `summarize_document` function that uses Claude to summarize the contents of a sublease agreement. The function accepts a text string and a list of details to extract as inputs. In this example, we call the function with the `document_text` and `details_to_extract` variables that were defined in the previous code snippets.

Within the function, a prompt is generated for Claude, including the document to be summarized, the details to extract, and specific instructions for summarizing the document. The prompt instructs Claude to respond with a summary of each detail to extract nested within XML headers.

Because we decided to output each section of the summary within tags, each section can easily be parsed out as a post-processing step. This approach enables structured summaries that can be adapted for your use case, so that each summary follows the same pattern.

### Evaluate your prompt

Prompting often requires testing and optimization for it to be production ready. To determine the readiness of your solution, evaluate the quality of your summaries using a systematic process combining quantitative and qualitative methods. Creating a [strong empirical evaluation](/en/docs/build-with-claude/develop-tests#building-evals-and-test-cases) based on your defined success criteria will allow you to optimize your prompts. Here are some metrics you may wish to include within your empirical evaluation:

<AccordionGroup>
  <Accordion title="ROUGE scores">This measures the overlap between the generated summary and an expert-created reference summary. This metric primarily focuses on recall and is useful for evaluating content coverage.</Accordion>
  <Accordion title="BLEU scores">While originally developed for machine translation, this metric can be adapted for summarization tasks. BLEU scores measure the precision of n-gram matches between the generated summary and reference summaries. A higher score indicates that the generated summary contains similar phrases and terminology to the reference summary. </Accordion>
  <Accordion title="Contextual embedding similarity">This metric involves creating vector representations (embeddings) of both the generated and reference summaries. The similarity between these embeddings is then calculated, often using cosine similarity. Higher similarity scores indicate that the generated summary captures the semantic meaning and context of the reference summary, even if the exact wording differs.</Accordion>
  <Accordion title="LLM-based grading">This method involves using an LLM such as Claude to evaluate the quality of generated summaries against a scoring rubric. The rubric can be tailored to your specific needs, assessing key factors like accuracy, completeness, and coherence. For guidance on implementing LLM-based grading, view these [tips](/en/docs/build-with-claude/develop-tests#tips-for-llm-based-grading).</Accordion>
  <Accordion title="Human evaluation">In addition to creating the reference summaries, legal experts can also evaluate the quality of the generated summaries. While this is expensive and time-consuming at scale, this is often done on a few summaries as a sanity check before deploying to production.</Accordion>
</AccordionGroup>

### Deploy your prompt

Here are some additional considerations to keep in mind as you deploy your solution to production.

1. **Ensure no liability:** Understand the legal implications of errors in the summaries, which could lead to legal liability for your organization or clients. Provide disclaimers or legal notices clarifying that the summaries are generated by AI and should be reviewed by legal professionals.

2. **Handle diverse document types:** In this guide, we’ve discussed how to extract text from PDFs. In the real-world, documents may come in a variety of formats (PDFs, Word documents, text files, etc.). Ensure your data extraction pipeline can convert all of the file formats you expect to receive.

3. **Parallelize API calls to Claude:** Long documents with a large number of tokens may require up to a minute for Claude to generate a summary. For large document collections, you may want to send API calls to Claude in parallel so that the summaries can be completed in a reasonable timeframe. Refer to Anthropic’s [rate limits](/en/api/rate-limits#rate-limits) to determine the maximum amount of API calls that can be performed in parallel.

***

## Improve performance

In complex scenarios, it may be helpful to consider additional strategies to improve performance beyond standard [prompt engineering techniques](/en/docs/build-with-claude/prompt-engineering/overview). Here are some advanced strategies:

### Perform meta-summarization to summarize long documents

Legal summarization often involves handling long documents or many related documents at once, such that you surpass Claude’s context window. You can use a chunking method known as meta-summarization in order to handle this use case. This technique involves breaking down documents into smaller, manageable chunks and then processing each chunk separately. You can then combine the summaries of each chunk to create a meta-summary of the entire document.

Here's an example of how to perform meta-summarization:

```python  theme={null}
import anthropic

# Initialize the Anthropic client
client = anthropic.Anthropic()

def chunk_text(text, chunk_size=20000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_long_document(text, details_to_extract, model="claude-sonnet-4-5", max_tokens=1000):

    # Format the details to extract to be placed within the prompt's context
    details_to_extract_str = '\n'.join(details_to_extract)

    # Iterate over chunks and summarize each one
    chunk_summaries = [summarize_document(chunk, details_to_extract, model=model, max_tokens=max_tokens) for chunk in chunk_text(text)]
    
    final_summary_prompt = f"""
    
    You are looking at the chunked summaries of multiple documents that are all related. 
    Combine the following summaries of the document from different truthful sources into a coherent overall summary:

    <chunked_summaries>
    {"".join(chunk_summaries)}
    </chunked_summaries>

    Focus on these key aspects:
    {details_to_extract_str})

    Provide the summary in bullet points nested within the XML header for each section. For example:

    <parties involved>
    - Sublessor: [Name]
    // Add more details as needed
    </parties involved>
    
    If any information is not explicitly stated in the document, note it as "Not specified". Do not preamble.
    """

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system="You are a legal expert that summarizes notes on one document.",
        messages=[
            {"role": "user",  "content": final_summary_prompt},
            {"role": "assistant", "content": "Here is the summary of the sublease agreement: <summary>"}

        ],
        stop_sequences=["</summary>"]
    )
    
    return response.content[0].text

long_summary = summarize_long_document(document_text, details_to_extract)
print(long_summary)
```

The `summarize_long_document` function builds upon the earlier `summarize_document` function by splitting the document into smaller chunks and summarizing each chunk individually.

The code achieves this by applying the `summarize_document` function to each chunk of 20,000 characters within the original document. The individual summaries are then combined, and a final summary is created from these chunk summaries.

Note that the `summarize_long_document` function isn’t strictly necessary for our example pdf, as the entire document fits within Claude’s context window. However, it becomes essential for documents exceeding Claude’s context window or when summarizing multiple related documents together. Regardless, this meta-summarization technique often captures additional important details in the final summary that were missed in the earlier single-summary approach.

### Use summary indexed documents to explore a large collection of documents

Searching a collection of documents with an LLM usually involves retrieval-augmented generation (RAG). However, in scenarios involving large documents or when precise information retrieval is crucial, a basic RAG approach may be insufficient. Summary indexed documents is an advanced RAG approach that provides a more efficient way of ranking documents for retrieval, using less context than traditional RAG methods. In this approach, you first use Claude to generate a concise summary for each document in your corpus, and then use Clade to rank the relevance of each summary to the query being asked. For further details on this approach, including a code-based example, check out the summary indexed documents section in the [summarization cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb).

### Fine-tune Claude to learn from your dataset

Another advanced technique to improve Claude's ability to generate summaries is fine-tuning. Fine-tuning involves training Claude on a custom dataset that specifically aligns with your legal summarization needs, ensuring that Claude adapts to your use case. Here’s an overview on how to perform fine-tuning:

1. **Identify errors:** Start by collecting instances where Claude’s summaries fall short - this could include missing critical legal details, misunderstanding context, or using inappropriate legal terminology.

2. **Curate a dataset:** Once you've identified these issues, compile a dataset of these problematic examples. This dataset should include the original legal documents alongside your corrected summaries, ensuring that Claude learns the desired behavior.

3. **Perform fine-tuning:** Fine-tuning involves retraining the model on your curated dataset to adjust its weights and parameters. This retraining helps Claude better understand the specific requirements of your legal domain, improving its ability to summarize documents according to your standards.

4. **Iterative improvement:** Fine-tuning is not a one-time process. As Claude continues to generate summaries, you can iteratively add new examples where it has underperformed, further refining its capabilities. Over time, this continuous feedback loop will result in a model that is highly specialized for your legal summarization tasks.

<Tip>Fine-tuning is currently only available via Amazon Bedrock. Additional details are available in the [AWS launch blog](https://aws.amazon.com/blogs/machine-learning/fine-tune-anthropics-claude-3-haiku-in-amazon-bedrock-to-boost-model-accuracy-and-quality/).</Tip>

<CardGroup cols={2}>
  <Card title="Summarization cookbook" icon="link" href="https://github.com/anthropics/anthropic-cookbook/blob/main/skills/summarization/guide.ipynb">
    View a fully implemented code-based example of how to use Claude to summarize contracts.
  </Card>

  <Card title="Citations cookbook" icon="link" href="https://github.com/anthropics/anthropic-cookbook/blob/main/misc/using_citations.ipynb">
    Explore our Citations cookbook recipe for guidance on how to ensure accuracy and explainability of information.
  </Card>
</CardGroup>
