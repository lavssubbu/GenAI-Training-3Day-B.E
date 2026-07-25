# Our Roadmap — Build a Mini Transformer From Scratch

```
Raw Text (list of strings)
   ↓
Tokenizer
   ↓
Vocabulary (shared across all sentences)
   ↓
Token IDs  (encoded — list of lists)
   ↓
Padding    (all sequences aligned to the same length)
   ↓
Embeddings
   ↓
Attention Mechanism
   ↓
Mini Transformer
   ↓
Next Token Prediction
```

---

# Simple Tokenizer

```python
import re

raw_text = "I love AI and AI loves me"

def simple_tokenizer(text):
    text = text.lower()
    tokens = text.split()
    return tokens

tokens = simple_tokenizer(raw_text)
print(tokens)
# ['i', 'love', 'ai', 'and', 'ai', 'loves', 'me']
```

Then we map the tokens to token IDs (vocabulary mapping):

```python
vocab = {}

for token in tokens:
    if token not in vocab:
        vocab[token] = len(vocab) + 1

print(vocab)
# {'i': 1, 'love': 2, 'ai': 3, 'and': 4, 'loves': 5, 'me': 6}
```

Get the encoded IDs:

```python
encoded_text = [vocab[token] for token in tokens]
print(encoded_text)
# [1, 2, 3, 4, 3, 5, 6]
```

---

# Better Tokenizer — Handles a List of Strings

Our first tokenizer was too simple.

**Problems:**
- Punctuation not handled
- Uppercase/lowercase inconsistency
- Repeated spaces
- Unknown words (`<UNK>`)
- Sentences of different lengths (need padding)
- Only handled **one** string at a time

Real tokenizers accept **a list of sentences** and process them all together.

---

## Usage

```python
from tokenizer import Tokenizer

sentences = [
    "I love AI, and AI loves me",
    "https://example.com",
    "2025",
    "if(x > 5):",
]

t = Tokenizer(sentences)
```

---

## Step 1 — Punctuation Handling (Regex Tokenization)

Each sentence is tokenized with a regex that separates words **and** punctuation:

```python
import re

def _tokenize_sentence(text: str) -> list[str]:
    text = text.lower()
    tokens = re.findall(r'\w+|[^\w\s]', text)
    return tokens
```

**Example output:**
```
Sentence 1: ['i', 'love', 'ai', ',', 'and', 'ai', 'loves', 'me']
Sentence 2: ['https', ':', '/', '/', 'example', '.', 'com']
Sentence 3: ['2025']
Sentence 4: ['if', '(', 'x', '>', '5', ')', ':']
```

---

## Step 2 — Shared Vocabulary Building

A single vocabulary is built across **all** sentences.  
Special tokens are reserved at fixed indices:

| Token   | ID |
|---------|----|
| `<PAD>` | 0  |
| `<UNK>` | 1  |
| (words) | 2+ |

```python
def _build_vocabulary(tokenized_sentences):
    vocab = {"<PAD>": 0, "<UNK>": 1}
    for tokens in tokenized_sentences:
        for token in tokens:
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab
```

---

## Step 3 — Encoding

Each sentence is converted to a list of token IDs:

```python
encoded = t.encoding()
# Sentence 1: [2, 3, 4, 5, 6, 4, 7, 8]
# Sentence 2: [9, 10, 11, 11, 12, 13, 14]
# Sentence 3: [15]
# Sentence 4: [16, 17, 18, 19, 20, 21, 10]
```

Returns a `list[list[int]]` — one inner list per sentence.

---

## Step 4 — Decoding

Token IDs are mapped back to words using the reverse vocabulary:

```python
decoded = t.decoding(encoded)
# Sentence 1: ['i', 'love', 'ai', ',', 'and', 'ai', 'loves', 'me']
# Sentence 2: ['https', ':', '/', '/', 'example', '.', 'com']
# Sentence 3: ['2025']
# Sentence 4: ['if', '(', 'x', '>', '5', ')', ':']
```

Returns a `list[list[str]]`.

---

## Step 5 — Padding

NLP models require all input sequences to have the **same length**.  
Shorter sequences are padded with `<PAD>` (ID = 0); longer ones are truncated.

```python
padded = t.padding()         # auto max_length
padded = t.padding(max_length=10)  # or specify manually
```

**Example output (max_length = 8):**
```
Sentence 1: [2, 3, 4, 5, 6, 4, 7, 8]      ← no padding needed
Sentence 2: [9, 10, 11, 11, 12, 13, 14, 0] ← 1 pad token added
Sentence 3: [15, 0, 0, 0, 0, 0, 0, 0]     ← 7 pad tokens added
Sentence 4: [16, 17, 18, 19, 20, 21, 10, 0] ← 1 pad token added
```

Before padding:
```
[[2], [2,3,4], [2,3]]
```
After padding (max_length = 3):
```
[[2, 0, 0], [2, 3, 4], [2, 3, 0]]
```

> **This is the foundation for all LLMs.**

---
