# NLP Preprocessing Engine 
---

##  Project Overview

This project is developed as part of the **Data Science Internship Assignment (February 2026)**.

The goal is to build a **robust NLP preprocessing pipeline** that transforms noisy, real-world text data into clean, structured tokens suitable for machine learning models.

---

##  Objectives

* Clean and normalize raw text data
* Handle real-world noise (URLs, emojis, numbers, repeated characters)
* Generate meaningful tokens
* Perform token-level analytics
* Build a reusable NLP pipeline

---

##  Features
```
✔ Remove numbers
✔ Remove URLs and email patterns
✔ Convert text to lowercase
✔ Normalize repeated characters (e.g., *"soooo"* → *"so"*)
✔ Remove emojis and special characters
✔ Remove extra spaces
✔ Remove short words (≤2 characters, except **"no"**, **"not"**)
```

---

##  Technologies Used

* Python
* Regular Expressions (`re`)
* Collections (`Counter`)

---

##  Core Function

### `preprocess_text(text)`

This function:

* Cleans raw input text
* Removes unwanted noise
* Returns:

  * Cleaned tokens
  * Cleaned sentence

---

##  Full Pipeline

### `full_pipeline(text_list)`

Processes multiple text inputs and returns:

```
{
  "tokens": [...],
  "clean_sentences": [...]
}
```

---

##  Sample Input

```
"I absolutely looooved this product 😍😍"
```

##  Output

```
Tokens: ['absolutely', 'loved', 'this', 'product']
Cleaned Sentence: absolutely loved this product
```

---

##  Token Analytics

* Total tokens
* Unique tokens
* Average token length

---

##  Frequency Analysis

* Top 10 most frequent words
* Top 5 least frequent words

---

##  Error Handling

The system handles:

* Empty input
* Non-string input
* Emoji-only text
* Numeric-only text

---

##  How to Run

1. Open the notebook in Jupyter or Google Colab
2. Run all cells
3. View outputs for each task

---

##  Submission

This repository is submitted as part of the internship assignment via the provided Google Form.

---

##  Key Highlights

* Clean and modular code
* Real-world text handling
* Scalable preprocessing pipeline
* Well-structured notebook

---

