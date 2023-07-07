import nltk
import yaml
import os
import time
from transformers import pipeline, BartForConditionalGeneration, BartTokenizer
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
        self.pipe = self.load(config_data['model'])
        self._text = ""
        self.x = 0.25
        self.y = 0.65
        self.summary = ""

    def load(self, model_name):
        model = BartForConditionalGeneration.from_pretrained(model_name)
        tokenizer = BartTokenizer.from_pretrained(model_name)
        return pipeline("summarization", model=model, tokenizer=tokenizer, device=-1)

    def getMinMax(self, text):
        tokens_count = len(nltk.word_tokenize(text))
        return int(tokens_count*config_data['min']), int(tokens_count*config_data['max'])

    def invoke_model(self, text):
        self.x, self.y = self.getMinMax(text)
        try:
            data = self.pipe(
                "Summarize:- \n\n"+text,
                min_length=self.x,
                truncation=True,
                no_repeat_ngram_size=3,
                max_length=self.y,
                temperature=0,
                top_k=0,
            )
            if not data or 'summary_text' not in data[0].keys():
                self.summary = ""
            else:
                self.summary = data[0]['summary_text'].replace('\n', ' ')
                self.summary = self.summary.replace('  ', ' ')
        except Exception as ex:
            print(ex)
            self.summary = ""

    def generate_summary(self, text):
        text = clean(text)
        self.invoke_model(text)
        sentences = sentenceTokenizer(self.summary)
        for sent in range(len(sentences)):
            sentences[sent] = afterClean(sentences[sent], text)
        final_summary = " ".join(sentences)
        return final_summary


if __name__ == '__main__':
    summ = Summarizer()
    text = """
    Action movie Sound of Freedom has defied expectations at the Box Office and beaten Harrison Ford's swansong, Indiana Jones and the Dial of Destiny.
    The movie centers around the real-life story of the founder of the anti-sex trafficking charity Operation Underground Railroad, Tim Ballard. It's seen as a surprise that this relatively small-scale movie outperformed what is seen as the summer blockbuster Indiana Jones on the Fourth of July, a date that in the past has been dominated by the likes of Jaws, Forrest Gump and Top Gun: Maverick.
    The feat of Sound of Freedom beating Indiana Jones and the Dial of Destiny is even more impressive when you consider the numbers behind each movie's release.
    The first movie not to be written by George Lucas or directed by Steven Spielberg, the fifth Indiana Jones had a reported budget up to $295 million, according to Deadline, if not more, according to other sources cited.
    Sound of Freedom, co-written and directed by Alejandro Monteverde, cost $14.5 million to make according to the Wall Street Journal. By today's standards this is a pittance compared to the massive budgets assigned to your regular summer blockbusters that are often north of $100 million.
    The movie box office website Box Office Mojo confirmed that Sound of Freedom outperformed Indiana Jones and the Dial of Destiny on Tuesday July 4.
    While the fifth Indiana Jones movie made $11,698,989, Sound of Freedom made almost its entire budget back: $14,242,063. Animated movies Elemental and Spider-Man: Across the Spider-Verse were behind these films, taking in over $2 million each.
    There are some extenuating factors to consider when it comes to comparing the two, in what could be seen as a David-versus-Goliath situation when it comes to movie making.
    Indiana Jones and the Dial of Destiny was released in movie theaters almost a week ago, coming out on June 30, 2023. It's taken in over $154 million at the international box office in that time as it attempts to claw back its sizable budget.
    In comparison, Sound of Freedom's first day of release was Tuesday July 4, and famously the first day of release is always the most profitable for a movie as theater-goers rush to see it.
    Sound of Freedom tells for story of Tim Ballard, who quits his job as a special agent with Homeland Security to embark on a mission to rescue children from cartels and human traffickers in Latin America.
    Ballard was in the news recently after rumors surfaced that Mel Gibson had helped him make a four-part documentary series about about child sex-trafficking. Gibson's representatives confirmed to Newsweek this was not the case, despite the rumors.
    """
    print("Summary is:- \n")
    start_time = time.time()
    print(summ.generate_summary(text))
    end_time = time.time()
    print(f"Time to generate the summary:- {round(end_time - start_time,2)}secs")
