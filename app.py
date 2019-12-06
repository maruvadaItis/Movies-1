from flask import Flask
from flask import render_template
from flask import request
from collections import Counter
from math import log10, log
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import word_tokenize
from numpy import dot
import json
import numpy as np
from numpy.linalg import norm
import pandas as pd
import pickle
import csv

import nltk
nltk.download('stopwords')

class Engine:
    def __init__(self):
        self.movie_data = []
        self.image_data = []

        with open('static/movie.csv', 'r', encoding='utf-8') as csvfile:
            moviereader = csv.reader(csvfile)
            index = 0
            for movie_line in moviereader:
                if index == 500:
                    break
                try:
                    if (movie_line[20] == 'title'):
                        pass
                    else:
                        self.movie_data.append({'overview': movie_line[9], 'id': movie_line[5], 'title': movie_line[20],
                                          'original_title': movie_line[8], 'poster_path': movie_line[11]})
                except:
                    pass
                index += 1

        with open('static/images.csv', 'r', encoding='utf-8') as imageFile:
            imgreader = csv.reader(imageFile)
            for img_line in imgreader:
                if(img_line[0] != "id" and img_line[1] != "url" and img_line[2] != "caption"):
                    try:
                        self.image_data.append({'id': img_line[0], 'url': img_line[1], 'caption': img_line[2]})
                    except:
                        pass
                else:
                    pass

        self.stop_words = stopwords.words('english')
        ## movie data
        self.movie_unique_words = set()
        self.movie_word_document_frequency = {}
        self.movie_word_frequency_documents = {}
        self.movie_document_lengths = {}
        movie_length = len(self.movie_data)

        for index in range(movie_length):
            row = self.movie_data[index]

            document = row['overview']
            title = row['title']
            movie_id = row['id']
            tokens = self.stem_tokenize(str(document))
            self.movie_unique_words = self.movie_unique_words.union(set(tokens))
            for term in set(tokens):
                if term not in self.movie_word_frequency_documents:
                    self.movie_word_frequency_documents[term] = {}
                self.movie_word_frequency_documents[term][movie_id] = tokens.count(term)

            for term in self.movie_word_frequency_documents:
                self.movie_word_document_frequency[term] = len(self.movie_word_frequency_documents[term])
            self.movie_document_lengths[movie_id] = len(tokens)

        ## image data
        self.image_unique_words = set()
        self.image_word_caption_frequency = {}
        self.image_word_frequency_captions = {}
        self.image_caption_lengths = {}
        image_length = len(self.image_data)

        for index in range(image_length):
            row = self.image_data[index]

            caption = " ".join(eval(str(row['caption'])))
            image_id = row['id']
            tokens = self.stem_tokenize(str(caption))
            self.image_unique_words = self.image_unique_words.union(set(tokens))
            for term in set(tokens):
                if term not in self.image_word_frequency_captions:
                    self.image_word_frequency_captions[term] = {}
                self.image_word_frequency_captions[term][image_id] = tokens.count(term)

            for term in self.image_word_frequency_captions:
                self.image_word_caption_frequency[term] = len(self.image_word_frequency_captions[term])
            self.image_caption_lengths[image_id] = len(tokens)

    def stem_tokenize(self, document):
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'[a-zA-Z]+')

        terms = tokenizer.tokenize(document.lower())
        filtered = [stemmer.stem(word) for word in terms if not word in self.stop_words]
        return filtered

    def make_tf_idf_table(self, tf_scores, idf_scores, image_id, query_words):
        table = '<table class="table table-striped"><tr>'
        table += '<th class="col_token">Token</th><th class="col_tf">TF</th><th class="col_idf">IDF</th><th class="col_tf_idf">TF * IDF</th>'
        table += '</tr>'
        final_score = 0.0
        for token in query_words:
            tf_score = tf_scores[image_id][token] if token in tf_scores[image_id] else 0.0
            idf_score = idf_scores[token] if token in idf_scores else 0.0
            final_score = final_score + (tf_score * idf_score)
            table += '<tr><td>' + token + '</td><td>' + str(tf_score) + '</td><td>' + str(
                idf_score) + '</td><td>' + str(tf_score * idf_score) + '</td></tr>'
        table += '</table>'
        return table

    def search_movie(self, query_string):
        query_words = self.stem_tokenize(query_string)

        tf_scores = {}
        for word in query_words:
            for movie_id in self.movie_word_frequency_documents[word]:
                if movie_id not in tf_scores:
                    tf_scores[movie_id] = {}
                tf_scores[movie_id][word] = self.movie_word_frequency_documents[word][movie_id] / self.movie_document_lengths[movie_id]

        idf_scores = {}
        for word in set(query_words):
            if word in self.movie_word_document_frequency:
                idf_scores[word] = log10(len(self.movie_document_lengths) / self.movie_word_document_frequency[word])
            else:
                idf_scores[word] = 0

        query_length = len(query_words)
        query_vector = []
        for term in query_words:
            term_count = query_words.count(term)
            term_F = term_count / query_length
            query_idf = 0
            if term in query_words:
                query_idf = log10(query_length / term_count)

            tf_idf = term_F * query_idf
            query_vector.append(tf_idf)

        document_similarity = Counter()

        document_vectors = {}
        for movie_id in tf_scores:
            document_vectors[movie_id] = []
            for query_term in query_words:
                if query_term in self.movie_unique_words:
                    if movie_id in self.movie_word_frequency_documents[query_term]:
                        tf = self.movie_word_frequency_documents[query_term][movie_id] / self.movie_document_lengths[movie_id]
                        idf = 0
                        if query_term in self.movie_word_document_frequency:
                            idf = log10(len(self.movie_document_lengths) / self.movie_word_document_frequency[query_term])
                        else:
                            idf = 0
                        tf_idf = tf * idf
                        document_vectors[movie_id].append(tf_idf)
                    else:
                        document_vectors[movie_id].append(0)
                else:
                    document_vectors[movie_id].append(0)

            document_similarity += {movie_id: dot(query_vector, document_vectors[movie_id]) / (
                    norm(query_vector) * norm(document_vectors[movie_id]))}

        views = []
        for item in document_similarity.most_common(5):
            row = [d for d in self.movie_data if (d['id'] == item[0])][0]

            view = {
                "title_eng": row['title'],
                "title_orig": row['original_title'],
                "overview": row['overview'],
                "poster": "https://image.tmdb.org/t/p/w300_and_h450_bestv2" + row['poster_path'],
                "score_table": self.make_tf_idf_table(tf_scores, idf_scores, item[0], query_words),
            }

            views.append(view)

        return views, query_words

    def search_classify(self, query_string):
        Genres = ['Action', 'Adventure', 'Animation', 'Aniplex', 'Carousel', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Entertainment', 'Family', 'Fantasy', 'Foreign', 'History', 'Horror', 'Music', 'Mystery', 'Odyssey', 'Romance', 'Science', 'Thriller', 'TV', 'War', 'Western']
        TotalCount = []
        ClassifyData = []

        df = pd.read_csv('static/movie.csv')
        data = df['genres'].tolist()
        overviews = df['overview'].tolist()
        end = len(data)
        TotalCountGenre = 0

        for counter in range(0, len(Genres)):
            val = 0
            for count in range(0, end):
                string = data[count]
                key = Genres[counter]

                if key in string:
                    val = val + 1
            TotalCountGenre += val
            TotalCount.append(val)

        movieName = query_string.lower()
        token = movieName.split(' ')
        total = len(token)

        TotalProb = 0
        posterior = []
        for counter in range(0, len(Genres)):
            sum = 0
            for i in range(0, total):
                if (len(token[i]) > 2):
                    for count in range(0, end):
                        if Genres[counter] in data[count]:
                            if str(token[i]) in str(overviews[count]):
                                sum = sum + 1
                else:
                    continue
            liklihood = (sum / TotalCount[counter]) * (TotalCount[counter] / TotalCountGenre)
            TotalProb = TotalProb + liklihood
            posterior.append(liklihood)

        Final = []
        TFinal = 0
        for counter in range(0, len(posterior)):
            temp = (posterior[counter] / TotalProb) * 100
            TFinal = TFinal + temp
            Final.append(temp)
            ClassifyData.append('Probability of ' + str(Genres[counter]) + ' = ' + str(temp) + '%')

        return ClassifyData

    def search_image(self, query_string):
        query_words = self.stem_tokenize(query_string)

        tf_scores = {}
        for word in query_words:
            for image_id in self.image_word_frequency_captions[word]:
                if image_id not in tf_scores:
                    tf_scores[image_id] = {}
                tf_scores[image_id][word] = self.image_word_frequency_captions[word][image_id] / self.image_caption_lengths[image_id]

        idf_scores = {}
        for word in set(query_words):
            if word in self.image_word_caption_frequency:
                idf_scores[word] = log10(len(self.image_caption_lengths) / self.image_word_caption_frequency[word])
            else:
                idf_scores[word] = 0

        query_length = len(query_words)
        query_vector = []
        for term in query_words:
            term_count = query_words.count(term)
            term_F = term_count / query_length
            query_idf = 0
            if term in query_words:
                query_idf = log10(query_length / term_count)

            tf_idf = term_F * query_idf
            query_vector.append(tf_idf)

        caption_similarity = Counter()

        caption_vectors = {}
        for image_id in tf_scores:
            caption_vectors[image_id] = []
            for query_term in query_words:
                if query_term in self.image_unique_words:
                    if image_id in self.image_word_frequency_captions[query_term]:
                        tf = self.image_word_frequency_captions[query_term][image_id] / self.image_caption_lengths[image_id]
                        idf = 0
                        if query_term in self.image_word_caption_frequency:
                            idf = log10(len(self.image_caption_lengths) / self.image_word_caption_frequency[query_term])
                        else:
                            idf = 0
                        tf_idf = tf * idf
                        caption_vectors[image_id].append(tf_idf)
                    else:
                        caption_vectors[image_id].append(0)
                else:
                    caption_vectors[image_id].append(0)

            caption_similarity += {image_id: dot(query_vector, caption_vectors[image_id]) / (
                    norm(query_vector) * norm(caption_vectors[image_id]))}

        views = []
        for item in caption_similarity:
            row = [d for d in self.image_data if (d['id'] == item)][0]

            view = {
                "caption": " ".join(eval(str(row['caption']))),
                "image": row['url'],
                "score_table": self.make_tf_idf_table(tf_scores, idf_scores, item, query_words),
            }

            views.append(view)

        return views, query_words


engine = Engine()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    flag = request.form['flag']
    query_string = request.form['query_string']
    if flag == "Search":
        results, query_words = engine.search_movie(query_string)
        return render_template('index.html', query_string=query_string, query_words=query_words, flag=flag, res=results)
    elif flag == "Classify":
        results = engine.search_classify(query_string)
        return render_template('index.html', query_string=query_string, flag=flag, res=results)
    else:
        results, query_words = engine.search_image(query_string)
        return render_template('index.html', query_string=query_string, query_words=query_words, flag=flag, res=results)


if __name__ == '__main__':
    app.run()
