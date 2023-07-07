import nltk
import yaml
import os
import time
import torch
from transformers import BartForConditionalGeneration, BartTokenizer, AutoTokenizer
from utils import sentenceTokenizer, clean, afterClean
current_file_path = os.path.dirname(os.path.realpath(__file__))
config = {}
proj_path = current_file_path.split('/')[:-1]
config_path = "/".join(proj_path + ['dependencies'] + ['config.yaml'])

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)
config_data = config['data']


class Summarizer:
    def __init__(self):
        self.model = ""
        self.tokenizer = ""
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.token_counter = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.load(config_data['model'])
        self._text = ""
        self.x = 0.25
        self.y = 0.65
        self.summary = ""
    
    def get_token_count(self, text):
        return len(self.token_counter.tokenize(text))

    def load(self, model_name):
        model = BartForConditionalGeneration.from_pretrained(model_name).to(self.device)
        tokenizer = BartTokenizer.from_pretrained(model_name)
        self.model = model
        self.tokenizer = tokenizer

    def getMinMax(self, text):
        tokens_count = len(nltk.word_tokenize(text))
        return int(tokens_count*config_data['min']), int(tokens_count*config_data['max'])

    def invoke_model(self, text):
        text = text.strip()
        self.x, self.y = self.getMinMax(text)
        try:
            inputs = self.tokenizer([text.lower()], max_length=self.y, return_tensors="pt", truncation=True)
            summary_ids = self.model.generate(inputs["input_ids"])
            data = self.tokenizer.batch_decode(summary_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
            self.summary = data
            if self.summary is None:
                self.summary = ""
        except Exception as ex:
            print(ex)
            self.summary = ""

    def get_segments(self, text):
        if self.get_token_count(text) <= 500:
            return [text]
        sentences = sentenceTokenizer(text)
        if len(sentences) <= 1:
            return sentences
        segments = []
        segment = []
        counter = 0
        curr = 0
        for sent in sentences:
            curr = self.get_token_count(sent)
            if curr + counter > 280:
                segments.append(" ".join(segment))
                segment = [sent]
                counter = curr
            else:
                segment.append(sent)
                counter += curr
        if segment != []:
            segments.append(" ".join(segment))
        return segments

    def generate_summary(self, text):
        text = clean(text)
        segments = self.get_segments(text)
        for segment in segments:
            self.invoke_model(self.summary + " " + segment)
        final_summary = afterClean(self.summary, text)
        return final_summary


if __name__ == '__main__':
    summ = Summarizer()
    text = """
    Machine learning, a subfield of artificial intelligence, is a fascinating blend of statistics, computer science, and data analysis. It's an innovative discipline that imbues machines with the capacity to learn from and make decisions or predictions based on data, without being explicitly programmed to perform the task. The dramatic rise of machine learning in recent years is essentially the story of computers becoming increasingly smarter, and their ever-growing ability to understand, interact with, and influence the world around us.

The underlying concept of machine learning revolves around algorithms — a set of rules or instructions followed by the computer to solve problems. These algorithms are crafted in such a way that they can learn and improve over time when exposed to new data. The ability of an algorithm to learn from data makes it possible for computers to perform tasks that were once thought to be exclusively human capabilities, such as recognizing images or understanding natural language.

One of the primary categories of machine learning is supervised learning. This involves training an algorithm using a labeled dataset, where the correct answers (or "labels") are provided. The algorithm processes the input data and tries to model the relationship between these inputs and their corresponding outputs. Once the model is trained, it can predict outcomes for new, unseen data based on what it has learned. For example, a supervised learning algorithm could be trained to predict the price of a house based on features such as its size, location, and number of bedrooms.

On the other hand, unsupervised learning doesn't rely on labeled data. Instead, it aims to find patterns and relationships within the data itself. It helps discover hidden structures and regularities that may not be immediately apparent. Clustering (grouping similar data points together) and anomaly detection (identifying data points that are significantly different from the rest) are common tasks in unsupervised learning.

A more complex variant of machine learning is reinforcement learning, where an agent learns to make decisions by interacting with an environment. The agent performs actions and receives rewards or penalties based on the results of these actions. Over time, it learns to make decisions that maximize the cumulative reward. This type of learning is particularly beneficial in areas like game playing, robotics, and navigation, where the machine must learn to adapt to changing conditions and make optimal decisions.

Deep learning, a subset of machine learning, takes inspiration from the human brain's structure and function to create artificial neural networks. These networks consist of layers of interconnected nodes, or "neurons," which process information and learn complex patterns. Deep learning has been instrumental in significant advancements in image and speech recognition, natural language processing, and other areas requiring the understanding and replication of human-like thinking patterns.

Despite its promise and potential, machine learning also presents certain challenges. Bias in data can lead to unfair or discriminatory outcomes, and the "black box" nature of some machine learning models can make it difficult to understand how they're making decisions. Moreover, as machine learning models become more complex, they demand more computational power and larger volumes of high-quality data to train effectively.

Nonetheless, the possibilities for machine learning are vast. From self-driving cars to predictive healthcare, from personalized education to smart homes, machine learning is progressively redefining the boundaries of what technology can accomplish. As we continue to refine these techniques, we move closer to a world where machines can learn, adapt, and make decisions with human-like intelligence. The journey of machine learning, from a theoretical concept to a transformative technology, underscores our remarkable progress in the ongoing quest to unravel the complexities of artificial intelligence.
    """
    start_time = time.time()
    summary = summ.generate_summary(text)
    print("Summary is:- \n")
    print(summary)
    end_time = time.time()
    print(f"Time to generate the summary:- {round(end_time - start_time,2)}secs")
