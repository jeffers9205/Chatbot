from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from .models import Questions




def train_model():
    all_questions = Questions.objects.all()
    questions = [q.token for q in all_questions] 
    answers = [q.respuesta for q in all_questions]
    model = make_pipeline(CountVectorizer(), MultinomialNB())
    model.fit(questions, answers)
    return model