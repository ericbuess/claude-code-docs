# Embeddings

Text embeddings are numerical representations of text that enable measuring semantic similarity. This guide introduces embeddings, their applications, and how to use embedding models for tasks like search, recommendations, and anomaly detection.

---

## Before implementing embeddings

When selecting an embeddings provider, there are several factors you can consider depending on your needs and preferences:

- Dataset size & domain specificity: size of the model training dataset and its relevance to the domain you want to embed. Larger or more domain-specific data generally produces better in-domain embeddings
- Inference performance: embedding lookup speed and end-to-end latency. This is a particularly important consideration for large scale production deployments
- Customization: options for continued training on private data, or specialization of models for very specific domains. This can improve performance on unique vocabularies

## How to get embeddings with Anthropic

Anthropic does not offer its own embedding model. One embeddings provider that has a wide variety of options and capabilities encompassing all of the above considerations is Voyage AI.

Voyage AI makes state-of-the-art embedding models and offers customized models for specific industry domains such as finance and healthcare, or bespoke fine-tuned models for individual customers.

The rest of this guide is for Voyage AI, but we encourage you to assess a variety of embeddings vendors to find the best fit for your specific use case.

## Available Models

Voyage recommends using the following text embedding models:

| Model | Context Length | Embedding Dimension | Description |
| --- | --- | --- | --- |
| `voyage-3-large` | 32,000 | 1024 (default), 256, 512, 2048 | The best general-purpose and multilingual retrieval quality. See [blog post](https://blog.voyageai.com/2025/01/07/voyage-3-large/) for details. |
| `voyage-3.5` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for general-purpose and multilingual retrieval quality. See [blog post](https://blog.voyageai.com/2025/05/20/voyage-3-5/) for details. |
| `voyage-3.5-lite` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for latency and cost. See [blog post](https://blog.voyageai.com/2025/05/20/voyage-3-5/) for details. |
| `voyage-code-3` | 32,000 | 1024 (default), 256, 512, 2048 | Optimized for **code** retrieval. See [blog post](https://blog.voyageai.com/2024/12/04/voyage-code-3/) for details. |
| `voyage-finance-2` | 32,000 | 1024 | Optimized for **finance** retrieval and RAG. See [blog post](https://blog.voyageai.com/2024/06/03/domain-specific-embeddings-finance-edition-voyage-finance-2/) for details. |
| `voyage-law-2` | 16,000 | 1024 | Optimized for **legal** and **long-context** retrieval and RAG. Also improved performance across all domains. See [blog post](https://blog.voyageai.com/2024/04/15/domain-specific-embeddings-and-retrieval-legal-edition-voyage-law-2/) for details. |

Additionally, the following multimodal embedding models are recommended:

| Model | Context Length | Embedding Dimension | Description |
| --- | --- | --- | --- |
| `voyage-multimodal-3` | 32000 | 1024 | Rich multimodal embedding model that can vectorize interleaved text and content-rich images, such as screenshots of PDFs, slides, tables, figures, and more. See [blog post](https://blog.voyageai.com/2024/11/12/voyage-multimodal-3/) for details. |

Need help deciding which text embedding model to use? Check out the [FAQ](https://docs.voyageai.com/docs/faq#what-embedding-models-are-available-and-which-one-should-i-use&ref=anthropic).

## Getting started with Voyage AI

To access Voyage embeddings:

1. Sign up on Voyage AI's website
2. Obtain an API key
3. Set the API key as an environment variable for convenience:

```bash
export VOYAGE_API_KEY="<your secret key>"
```

You can obtain the embeddings by either using the official [`voyageai` Python package](https://github.com/voyage-ai/voyageai-python) or HTTP requests, as described below.

### Voyage Python library

The `voyageai` package can be installed using the following command:

```bash
pip install -U voyageai
```

Then, you can create a client object and start using it to embed your texts:

```python
import voyageai

vo = voyageai.Client()
# This will automatically use the environment variable VOYAGE_API_KEY.
# Alternatively, you can use vo = voyageai.Client(api_key="<your secret key>")

texts = ["Sample text 1", "Sample text 2"]

result = vo.embed(texts, model="voyage-3.5", input_type="document")
print(result.embeddings[0])
print(result.embeddings[1])
```

`result.embeddings` will be a list of two embedding vectors, each containing 1024 floating-point numbers. After running the above code, the two embeddings will be printed on the screen:

```
[-0.013131560757756233, 0.019828535616397858, ...]   # embedding for "Sample text 1"
[-0.0069352793507277966, 0.020878976210951805, ...]  # embedding for "Sample text 2"
```

When creating the embeddings, you can specify a few other arguments to the `embed()` function. 

For more information on the Voyage python package, see [the Voyage documentation](https://docs.voyageai.com/docs/embeddings#python-api).

### Voyage HTTP API

You can also get embeddings by requesting Voyage HTTP API. For example, you can send an HTTP request through the `curl` command in a terminal:

```bash
curl https://api.voyageai.com/v1/embeddings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $VOYAGE_API_KEY" \
  -d '{
    "input": ["Sample text 1", "Sample text 2"],
    "model": "voyage-3.5"
  }'
```

The response you would get is a JSON object containing the embeddings and the token usage:

```json
{
  "object": "list",
  "data": [
    {
      "embedding": [-0.013131560757756233, 0.019828535616397858, ...],
      "index": 0
    },
    {
      "embedding": [-0.0069352793507277966, 0.020878976210951805, ...],
      "index": 1
    }
  ],
  "model": "voyage-3.5",
  "usage": {
    "total_tokens": 10
  }
}

```

For more information on the Voyage HTTP API, see [the Voyage documentation](https://docs.voyageai.com/reference/embeddings-api).

### AWS Marketplace

Voyage embeddings are available on [AWS Marketplace](https://aws.amazon.com/marketplace/seller-profile?id=seller-snt4gb6fd7ljg). Instructions for accessing Voyage on AWS are available [here](https://docs.voyageai.com/docs/aws-marketplace-model-package?ref=anthropic).

## Quickstart example

Now that we know how to get embeddings, let's see a brief example.

Suppose we have a small corpus of six documents to retrieve from

```python
documents = [
    "The Mediterranean diet emphasizes fish, olive oil, and vegetables, believed to reduce chronic diseases.",
    "Photosynthesis in plants converts light energy into glucose and produces essential oxygen.",
    "20th-century innovations, from radios to smartphones, centered on electronic advancements.",
    "Rivers provide water, irrigation, and habitat for aquatic species, vital for ecosystems.",
    "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.",
    "Shakespeare's works, like 'Hamlet' and 'A Midsummer Night's Dream,' endure in literature."
]

```

We will first use Voyage to convert each of them into an embedding vector

```python
import voyageai

vo = voyageai.Client()

# Embed the documents
doc_embds = vo.embed(
    documents, model="voyage-3.5", input_type="document"
).embeddings
```

The embeddings will allow us to do semantic search / retrieval in the vector space. Given an example query,

```python
query = "When is Apple's conference call scheduled?"
```

we convert it into an embedding, and conduct a nearest neighbor search to find the most relevant document based on the distance in the embedding space.

```python
import numpy as np

# Embed the query
query_embd = vo.embed(
    [query], model="voyage-3.5", input_type="query"
).embeddings[0]

# Compute the similarity
# Voyage embeddings are normalized to length 1, therefore dot-product
# and cosine similarity are the same.
similarities = np.dot(doc_embds, query_embd)

retrieved_id = np.argmax(similarities)
print(documents[retrieved_id])
```

Note that we use `input_type="document"` and `input_type="query"` for embedding the document and query, respectively. More specification can be found [here](/docs/en/build-with-claude/embeddings#voyage-python-package).

The output would be the 5th document, which is indeed the most relevant to the query:

```
Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET.
```

If you are looking for a detailed set of cookbooks on how to do RAG with embeddings, including vector databases, check out our [RAG cookbook](https://github.com/anthropics/anthropic-cookbook/blob/main/third_party/Pinecone/rag_using_pinecone.ipynb).

## FAQ

  <section title="Why do Voyage embeddings have superior quality?">

    Embedding models rely on powerful neural networks to capture and compress semantic context, similar to generative models. Voyage's team of experienced AI researchers optimizes every component of the embedding process, including:
    - Model architecture 
    - Data collection
    - Loss functions
    - Optimizer selection

    Learn more about Voyage's technical approach on their [blog](https://blog.voyageai.com/).
  
</section>

  <section title="What embedding models are available and which should I use?">

    For general-purpose embedding, we recommend:
    - `voyage-3-large`: Best quality
    - `voyage-3.5-lite`: Lowest latency and cost
    - `voyage-3.5`: Balanced performance with superior retrieval quality at a competitive price point 
    
    For retrieval, use the `input_type` parameter to specify whether the text is a query or document type.

    Domain-specific models:

    - Legal tasks: `voyage-law-2`
    - Code and programming documentation: `voyage-code-3`
    - Finance-related tasks: `voyage-finance-2`
  
</section>

  <section title="Which similarity function should I use?">

    You can use Voyage embeddings with either dot-product similarity, cosine similarity, or Euclidean distance. An explanation about embedding similarity can be found [here](https://www.pinecone.io/learn/vector-similarity/).

    Voyage AI embeddings are normalized to length 1, which means that:

    - Cosine similarity is equivalent to dot-product similarity, while the latter can be computed more quickly.
    - Cosine similarity and Euclidean distance will result in the identical rankings.
  
</section>

  <section title="What is the relationship between characters, words, and tokens?">

    Please see this [page](https://docs.voyageai.com/docs/tokenization?ref=anthropic).
  
</section>

  <section title="When and how should I use the input_type parameter?">

    For all retrieval tasks and use cases (e.g., RAG), we recommend that the `input_type` parameter be used to specify whether the input text is a query or document. Do not omit `input_type` or set `input_type=None`. Specifying whether input text is a query or document can create better dense vector representations for retrieval, which can lead to better retrieval quality.

    When using the `input_type` parameter, special prompts are prepended to the input text prior to embedding. Specifically:

    > 📘 **Prompts associated with `input_type`**
    > 
    > - For a query, the prompt is “Represent the query for retrieving supporting documents: “.
    > - For a document, the prompt is “Represent the document for retrieval: “.
    > - Example
    >     - When `input_type="query"`, a query like "When is Apple's conference call scheduled?" will become "**Represent the query for retrieving supporting documents:** When is Apple's conference call scheduled?"
    >     - When `input_type="document"`, a query like "Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET." will become "**Represent the document for retrieval:** Apple's conference call to discuss fourth fiscal quarter results and business updates is scheduled for Thursday, November 2, 2023 at 2:00 p.m. PT / 5:00 p.m. ET."

    `voyage-large-2-instruct`, as the name suggests, is trained to be responsive to additional instructions that are prepended to the input text. For classification, clustering, or other [MTEB](https://huggingface.co/mteb) subtasks, please use the instructions [here](https://github.com/voyage-ai/voyage-large-2-instruct).
  
</section>

  <section title="What quantization options are available?">

    Quantization in embeddings converts high-precision values, like 32-bit single-precision floating-point numbers, to lower-precision formats such as 8-bit integers or 1-bit binary values, reducing storage, memory, and costs by 4x and 32x, respectively. Supported Voyage models enable quantization by specifying the output data type with the `output_dtype` parameter:

    - `float`: Each returned embedding is a list of 32-bit (4-byte) single-precision floating-point numbers. This is the default and provides the highest precision / retrieval accuracy.
    - `int8` and `uint8`: Each returned embedding is a list of 8-bit (1-byte) integers ranging from -128 to 127 and 0 to 255, respectively.
    - `binary` and `ubinary`: Each returned embedding is a list of 8-bit integers that represent bit-packed, quantized single-bit embedding values: `int8` for `binary` and `uint8` for `ubinary`. The length of the returned list of integers is 1/8 of the actual dimension of the embedding. The binary type uses the offset binary method, which you can learn more about in the FAQ below.

    > **Binary quantization example**
    > 
    > Consider the following eight embedding values: -0.03955078, 0.006214142, -0.07446289, -0.039001465, 0.0046463013, 0.00030612946, -0.08496094, and 0.03994751. With binary quantization, values less than or equal to zero will be quantized to a binary zero, and positive values to a binary one, resulting in the following binary sequence: 0, 1, 0, 0, 1, 1, 0, 1. These eight bits are then packed into a single 8-bit integer, 01001101 (with the leftmost bit as the most significant bit).
    >   - `ubinary`: The binary sequence is directly converted and represented as the unsigned integer (`uint8`) 77.
    >   - `binary`: The binary sequence is represented as the signed integer (`int8`) -51, calculated using the offset binary method (77 - 128 = -51).
  
</section>

  <section title="How can I truncate Matryoshka embeddings?">

    Matryoshka learning creates embeddings with coarse-to-fine representations within a single vector. Voyage models, such as `voyage-code-3`, that support multiple output dimensions generate such Matryoshka embeddings. You can truncate these vectors by keeping the leading subset of dimensions. For example, the following Python code demonstrates how to truncate 1024-dimensional vectors to 256 dimensions:

    ```python
    import voyageai
    import numpy as np

    def embd_normalize(v: np.ndarray) -> np.ndarray:
        """
        Normalize the rows of a 2D numpy array to unit vectors by dividing each row by its Euclidean
        norm. Raises a ValueError if any row has a norm of zero to prevent division by zero.
        """
        row_norms = np.linalg.norm(v, axis=1, keepdims=True)
        if np.any(row_norms == 0):
            raise ValueError("Cannot normalize rows with a norm of zero.")
        return v / row_norms


    vo = voyageai.Client()

    # Generate voyage-code-3 vectors, which by default are 1024-dimensional floating-point numbers
    embd = vo.embed(['Sample text 1', 'Sample text 2'], model='voyage-code-3').embeddings

    # Set shorter dimension
    short_dim = 256

    # Resize and normalize vectors to shorter dimension
    resized_embd = embd_normalize(np.array(embd)[:, :short_dim]).tolist()
    ```
  
</section>

## Pricing

Visit Voyage's [pricing page](https://docs.voyageai.com/docs/pricing?ref=anthropic) for the most up to date pricing details.