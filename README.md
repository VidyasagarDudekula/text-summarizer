
# Abstractive Text Summarization

This project uses advanced Natural Language Processing (NLP) techniques and a pre-trained model to generate a summary of large blocks of text. The main steps involved in this process are data cleaning, sentence tokenization, and finally, text summarization using the pre-trained model.



## Overview

### 1. Data Cleaning and Preparation

Before processing, the text data is first cleaned and prepared using a series of techniques defined in the utils.py file. These techniques include removing unnecessary characters and handling encoding issues. We also perform capitalization of the first letter of a sentence and all proper nouns in the text. Once the data is cleaned, it is tokenized into individual sentences ready for summarization.

### 2. Text Summarization

For text summarization, we use the pre-trained model Yale-LILY/brio-cnndm-uncased. This model is trained on the CNN/Daily Mail dataset and is capable of generating abstractive summaries of text. It takes tokenized sentences as input and outputs a summarized version of the input text.

The main.py script handles the summarization process. It first loads the configuration parameters defined in the config.yaml file, prepares the text data using the utilities from utils.py, and finally uses the pre-trained model to generate a summary.
## Configurations

The config.yaml file contains various configuration parameters that control the behavior of the summarization process:

model: The pre-trained model used for text summarization. Default is Yale-LILY/brio-cnndm-uncased.
min, max: The minimum and maximum length (as a proportion of the original text length) of the generated summary.
## Requirements

Please ensure that all dependencies are installed by running the following command:

```bash
  gpip install -r requirements.txt
```
## Usage

To generate a summary, run the main.py script. Make sure to update the config.yaml file with your preferences.

```bash
  python main.py
```
## Examples

### Input Text

Machine learning, a subfield of artificial intelligence, is a fascinating blend of statistics, computer science, and data analysis. It's an innovative discipline that imbues machines with the capacity to learn from and make decisions or predictions based on data, without being explicitly programmed to perform the task. The dramatic rise of machine learning in recent years is essentially the story of computers becoming increasingly smarter, and their ever-growing ability to understand, interact with, and influence the world around us.

The underlying concept of machine learning revolves around algorithms — a set of rules or instructions followed by the computer to solve problems. These algorithms are crafted in such a way that they can learn and improve over time when exposed to new data. The ability of an algorithm to learn from data makes it possible for computers to perform tasks that were once thought to be exclusively human capabilities, such as recognizing images or understanding natural language.

One of the primary categories of machine learning is supervised learning. This involves training an algorithm using a labeled dataset, where the correct answers (or "labels") are provided. The algorithm processes the input data and tries to model the relationship between these inputs and their corresponding outputs. Once the model is trained, it can predict outcomes for new, unseen data based on what it has learned. For example, a supervised learning algorithm could be trained to predict the price of a house based on features such as its size, location, and number of bedrooms.

On the other hand, unsupervised learning doesn't rely on labeled data. Instead, it aims to find patterns and relationships within the data itself. It helps discover hidden structures and regularities that may not be immediately apparent. Clustering (grouping similar data points together) and anomaly detection (identifying data points that are significantly different from the rest) are common tasks in unsupervised learning.

A more complex variant of machine learning is reinforcement learning, where an agent learns to make decisions by interacting with an environment. The agent performs actions and receives rewards or penalties based on the results of these actions. Over time, it learns to make decisions that maximize the cumulative reward. This type of learning is particularly beneficial in areas like game playing, robotics, and navigation, where the machine must learn to adapt to changing conditions and make optimal decisions.

Deep learning, a subset of machine learning, takes inspiration from the human brain's structure and function to create artificial neural networks. These networks consist of layers of interconnected nodes, or "neurons," which process information and learn complex patterns. Deep learning has been instrumental in significant advancements in image and speech recognition, natural language processing, and other areas requiring the understanding and replication of human-like thinking patterns.

Despite its promise and potential, machine learning also presents certain challenges. Bias in data can lead to unfair or discriminatory outcomes, and the "black box" nature of some machine learning models can make it difficult to understand how they're making decisions. Moreover, as machine learning models become more complex, they demand more computational power and larger volumes of high-quality data to train effectively.

Nonetheless, the possibilities for machine learning are vast. From self-driving cars to predictive healthcare, from personalized education to smart homes, machine learning is progressively redefining the boundaries of what technology can accomplish. As we continue to refine these techniques, we move closer to a world where machines can learn, adapt, and make decisions with human-like intelligence. The journey of machine learning, from a theoretical concept to a transformative technology, underscores our remarkable progress in the ongoing quest to unravel the complexities of artificial intelligence.


### Generated Summary

Summary is:- 

Machine learning is a subfield of artificial intelligence that allows computers to learn from and make decisions based on data. The rise of machine learning is redefining the boundaries of what technology can do. Machine learning can help computers learn and make human-like decisions with human intelligence. The discipline is a blend of statistics, computer science, and data analysis. The possibilities for machine learning include self-driving cars, predictive healthcare, and smart homes. The rise of Machine learning is the result of advances in computer science and artificial intelligence. And the rise in the field of computer science is called machine learning.  And the growth of the field is expected to accelerate in The Coming Years.

Time to generate the summary:- 16.07secs





## Improve

For any issues or improvements, feel free to open an issue or a pull request.