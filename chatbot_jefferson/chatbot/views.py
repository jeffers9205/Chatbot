from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from .models import Questions
from .forms import QuestionsForm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
import re
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .train_model import train_model


model = train_model()


@login_required
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')

        processed_message = process_message(message)

        if message.lower().strip() not in ['si', 'no']:
            predicted_response = model.predict([processed_message])[0]
            print("Predicted response:", predicted_response)
            print("user_response :", message.lower().strip())
            try:
                question = Questions.objects.get(respuesta__icontains=predicted_response)
                respuesta = question.respuesta
                if question.token == processed_message:
                    return JsonResponse({'message': respuesta})
                else:
                    request.session['pending_query'] = predicted_response
                    return JsonResponse({'message': f'Si te refieres a "{question.pregunta}", responde "sí" para obtener la respuesta completa.'})
            except Questions.DoesNotExist:
                respuesta = 'Lo siento, no entendí tu pregunta. ¿Puedes intentar otra vez?'
                return JsonResponse({'message': respuesta})

        elif 'pending_query' in request.session:
            pending_query = request.session.get('pending_query')
            user_response = message.lower().strip()

            if user_response in ['sí', 'si']:
                try:
                    question = Questions.objects.get(respuesta__icontains=pending_query)
                    return JsonResponse({'message': question.respuesta})
                except Questions.DoesNotExist:
                    return JsonResponse({'message': 'No se encontró una respuesta para tu consulta.'})
            elif user_response in ['no']:
                return JsonResponse({'message': 'Por favor, proporciona más detalles o intenta otra pregunta.'})

@login_required
def chat_view(request):
    return render(request, 'chat.html')

def remove_accents(input_str):
    accents = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U',
        'ñ': 'n', 'Ñ': 'N'
    }
    for accented_char, unaccented_char in accents.items():
        input_str = input_str.replace(accented_char, unaccented_char)
    return input_str

def process_message(message):
    message = re.sub(r'[^\w\s]', '', message)
    message = remove_accents(message)
    tokens = word_tokenize(message.lower())
    stop_words = set(stopwords.words('spanish'))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]
    processed_message = ' '.join(lemmatized_tokens)
    return processed_message

@login_required
def queries_list(request):
    queries = Questions.objects.all()
    return render(request, 'queries_list.html', {'queries': queries})

@login_required
def queries_add(request):
    if request.method == 'POST':
        form = QuestionsForm(request.POST)
        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']
            respuesta = form.cleaned_data['respuesta']
            token = process_message(pregunta)
            question = Questions(pregunta=pregunta, respuesta=respuesta, token=token)
            question.save()
            global model
            model = train_model()

            return redirect('queries_list')
    else:
        form = QuestionsForm()
    return render(request, 'queries_form.html', {'form': form})

@login_required
def queries_update(request, id):
    question = get_object_or_404(Questions, id=id)
    if request.method == 'POST':
        form = QuestionsForm(request.POST, instance=question)
        if form.is_valid():
            pregunta = form.cleaned_data['pregunta']
            respuesta = form.cleaned_data['respuesta']
            token = process_message(pregunta)
            question.pregunta = pregunta
            question.respuesta = respuesta
            question.token = token
            question.save()
            global model
            model = train_model()
            return redirect('queries_list')
    else:
        form = QuestionsForm(instance=question)
    return render(request, 'queries_form.html', {'form': form})

@login_required
def queries_delete(request, id):
    question = get_object_or_404(Questions, id=id)
    if request.method == 'POST':
        question.delete()
        global model
        model = train_model()

        return redirect('queries_list')
    return render(request, 'queries_confirm_delete.html', {'question': question})

def index(request):
    return render(request, 'index.html')