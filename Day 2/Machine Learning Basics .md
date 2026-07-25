# Day 2: Machine Learning Fundamentals & Hands-on

## Rule 1 — You MUST write code yourself
You cannot become good by reading only. You will:
- Type code manually
- Debug errors
- Break things
- Fix things
- Improve code

That is how engineers are made.

## Rule 2 — We focus on WHY, not memorization
For every topic:
- What problem it solves
- Why industry uses it
- When NOT to use it
- Common mistakes
- Performance concerns

## Rule 3 — Real Industry Approach
We will simulate:
- Client requirements
- Messy datasets
- Broken code
- Deployment problems
- Model failures
- Hallucinations
- Optimization challenges

---

## Today's Agenda
1. Setup local LLMs and start using them independently via Ollama.
2. Demonstrate Hugging Face models with Ollama and explain how to use them.
3. Machine Learning Fundamentals.
4. Supervised Learning and Unsupervised Learning.
5. Regression.
6. Linear Regression.
7. Classification.
8. Feature Engineering.

---


## Hugging Face Model Demo
1. **AI Humanizer** - [https://huggingface.co/spaces/gpthuman/ai-humanizer](https://huggingface.co/spaces/gpthuman/ai-humanizer)
2. **Sulphur-2-base** - An uncensored video generation model based on LTX 2.3 supporting both t2v and i2v natively, as well as all of the other ltx 2.3 formats. - [http://huggingface.co/SulphurAI/Sulphur-2-base](http://huggingface.co/SulphurAI/Sulphur-2-base)


## What is Machine Learning?
Before ML existed, programmers wrote rules manually.
### Traditional Programming
```
Input + Rules -> Output
```


**Example:**
```python
if temperature > 35:
    print("Hot")
```

Here:
- Human writes logic
- Machine follows instructions
- This is traditional programming.

### The Problem
Real-world problems are **TOO complex**.

**Example:** How do you write rules for:
- Face recognition?
- Spam detection?
- Self-driving cars?
- Language translation?

**Impossible.** Because:
- Millions of conditions exist
- Patterns are hidden
- Rules constantly change

So instead of writing rules manually… we let the machine:
- Observe data
- Learn patterns
- Make decisions

**That is Machine Learning.**

### CORE IDEA OF ML

- **Traditional Programming:** Rules + Data → Output
- **Machine Learning:** Data + Answers → Rules

**VERY IMPORTANT:** ML learns rules automatically.

---

## What Is a LABEL?

This is the **MOST IMPORTANT** concept. Imagine teaching a child. You show:

| Animal Image | Answer |
| :--- | :--- |
| 🐶 | Dog |
| 🐱 | Cat |

Here:
- **Image** = Input
- **Answer** = Label

The label is the **correct answer**.

**Another Example:**
| House Size | Price |
| :--- | :--- |
| 1000 sqft | 10 lakhs |
| 2000 sqft | 20 lakhs |

Here:
- **Input** = House size
- **Label** = Price

The machine learns: `House Size → Price`

### SUPER SIMPLE DEFINITION
A **label** is the expected output we want the machine to learn.

### Why Labels Matter
Without labels, the machine doesn’t know:
- Right vs. Wrong
- Target
- Expected answer

Labels guide learning, like answer keys in school.

---

## Supervised Learning

### DEFINITION
Supervised learning means learning using **labeled data**.

### WHY “SUPERVISED”?
Because someone supervises the machine, like a teacher supervising a student.

### PROCESS
We give:
| Input | Label |
| :--- | :--- |
| Hours studied | Marks |
| Email | Spam/Not Spam |
| Symptoms | Disease |

The machine studies relationships.

### GOAL
The goal is to **predict future outputs correctly**.

**Example — House Price Prediction:**
| Size | Price |
| :--- | :--- |
| 1000 | 10L |
| 2000 | 20L |
| 3000 | 30L |

Machine learns: `Bigger house → Higher price`. Then predicts: `2500 sqft → ?`

### WHY DO WE DO SUPERVISED LEARNING?
Because prediction is valuable. Companies want predictions.

### REAL INDUSTRY PURPOSE
- **Amazon:** Predict what you may buy.
- **Banks:** Predict loan default risk.
- **Hospitals:** Predict disease probability.
- **Netflix:** Predict movies you’ll like.

**Supervised Learning = Prediction Engine**

---

## What Is Regression?

Regression is a type of supervised learning.

### PURPOSE OF REGRESSION
Regression predicts **NUMBERS**.

**Example:**
- Salary
- Stock price
- Rainfall
- House price
- Temperature

**Example Dataset:**
| Experience | Salary |
| :--- | :--- |
| 1 year | 3L |
| 2 years | 5L |
| 5 years | 10L |

Machine predicts: `7 years → ?`

### Why It Is Called Linear Regression
Because it tries to fit a **LINE**.

**VISUAL IDEA:**
```
salary
  |
10|                *
  |
  |           *
  |
5 |      *
  |
  |  *
  +-----------------
      experience
```
Machine draws best-fit line.

### Mathematical Form
`y = mx + b`

Where:
- **y** = Output
- **x** = Input
- **m** = Slope
- **b** = Starting point (y-intercept)

### WHY DO WE USE LINEAR REGRESSION?
Because many real-world relationships are approximately linear.
- More experience → More salary
- More ads → More sales
- More study → More marks

### Python Example
```python
from sklearn.linear_model import LinearRegression
import numpy as np

# Input
X = np.array([[1], [2], [3], [4]])

# Labels
y = np.array([10, 20, 30, 40])

# Model
model = LinearRegression()

# Learning
model.fit(X, y)

# Prediction
print(model.predict([[5]]))
```

### WHAT IS HAPPENING INSIDE?
The machine tries to discover: `y = 10x`
Because:
- 1 → 10
- 2 → 20
- 3 → 30
So for 5: `5 → 50`

---

## What Is Classification?

Classification is **ALSO** supervised learning, but instead of numbers, it predicts **CATEGORIES**.

### PURPOSE OF CLASSIFICATION
To identify classes/groups.

**Examples:**
| Input | Output |
| :--- | :--- |
| Email | Spam/Not Spam |
| Tumor | Cancer/Normal |
| Image | Cat/Dog |
| Transaction | Fraud/Valid |

### KEY IDEA
- **Regression** predicts continuous values.
- **Classification** predicts categories/classes.

### WHY DO WE NEED CLASSIFICATION?
Because businesses make decisions using categories.
- Approve/Reject loan
- Fraud/Not fraud
- Pass/Fail
- Disease/No disease

**Example:**
| Study Hours | Pass? |
| :--- | :--- |
| 1 | No |
| 5 | Yes |

The machine learns boundaries.

**Visual Idea:**
`Fail Fail Fail | Pass Pass Pass`
It tries to separate categories.

---

## What Is Unsupervised Learning?

Now remove labels completely.

**Example:** Suppose you only have: `10, 12, 15, 80, 85, 90`. No labels. No meaning. Machine must discover patterns itself.

### PURPOSE OF UNSUPERVISED LEARNING
- Discover hidden structures
- Group similar things
- Find unusual patterns

### WHY DO WE NEED IT?
Because real-world data often has **NO labels**. Labels are expensive.
**Example:** Millions of customer records with no manual labels. The machine must explore itself.

---

## What Is Clustering?

Clustering is a type of unsupervised learning.

### PURPOSE OF CLUSTERING
To group similar data.

**Example:** Customer ages: `18, 20, 21, 65, 70, 72`.
Machine creates:
- Young Group
- Old Group
Automatically.

### WHY BUSINESSES USE THIS
- **Marketing:** Group customers by interests, age, or buying behavior.
- **E-commerce:** Group similar products.
- **Cybersecurity:** Find abnormal behavior.

---

## What Is K-Means?

K-Means is a clustering algorithm.

### PURPOSE OF K-MEANS
To divide data into **K groups**.

### WHY “K”?
Because **K** = number of groups.
- K=2 → Two clusters
- K=3 → Three clusters

### HOW K-MEANS WORKS
Suppose data: `10, 12, 15, 80, 85, 90`

1. **STEP 1 — Pick Centers:** Machine randomly picks centers. (e.g., A=12, B=85)
2. **STEP 2 — Assign Nearest Group:** 10, 12, 15 → A; 80, 85, 90 → B.
3. **STEP 3 — Update Centers:** New average A=12.3, B=85.
4. **STEP 4 — Repeat Until Stable.**

### WHY DO WE USE K-MEANS?
Because grouping data is useful, and businesses use it heavily.

### Python Example
```python
from sklearn.cluster import KMeans
import numpy as np

X = np.array([
    [10], [12], [15],
    [80], [85], [90]
])

model = KMeans(n_clusters=2)
model.fit(X)

print(model.labels_)
```

### WHAT DOES fit() MEAN?
**IMPORTANT:** `fit()` = **LEARNING**.
When we write `model.fit(X, y)`, the model:
- Studies patterns
- Adjusts internal math
- Learns relationships

### AFTER fit()
The model becomes trained. Then we can use `model.predict()`.

---

## Why ML Is Powerful

Because it can:
- Learn automatically
- Improve from data
- Adapt to changing environments
- Solve impossible rule-based problems

### Traditional Programming vs ML
- **Traditional Programming:** Human writes rules.
- **Machine Learning:** Machine learns rules.

---

## OUR UNDERSTANDING

### Supervised Learning
- **Goal:** Predict outputs
- **Needs:** Labels, answers, supervision
- **Examples:** Regression, Classification

### Unsupervised Learning
- **Goal:** Discover hidden patterns
- **Needs:** Only data, no answers
- **Examples:** Clustering, Anomaly detection
