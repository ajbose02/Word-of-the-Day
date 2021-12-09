from django.shortcuts import render, get_object_or_404
from random_word import RandomWords
import json
from .models import word_class
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from datetime import date
import datetime


# Create your views here.
def index(request):
    rw = RandomWords()
    wod = rw.word_of_the_day(date=date.today().strftime('%Y-%m-%d'))
    if type(wod)== str:
        w = json.loads(wod)
    else:
        w = wod

    word = w['word'].capitalize()
    defin_dictionary = w['definations'][0]
    first_def = defin_dictionary['text']
    speech = defin_dictionary['partOfSpeech']
    new_word = word_class(word = word, definition = first_def, speech = speech, date_added = date.today())
    date_added = getattr(new_word, "date_added")
    try:
        dup_obj = word_class.objects.get(word = getattr(new_word, "word"))
    except word_class.DoesNotExist:
        new_word.save()

    context = {
        'word': word,
        'definition': first_def,
        'speech': speech,
        'date_added': date_added
    }
    return render(request, 'index.html', context)

def word(request, year, month, day):
    date_of_word = datetime.date(year, month, day)
    w = get_object_or_404(word_class, date_added = date_of_word)
    word = getattr(w, "word")
    definition = getattr(w, "definition")
    speech = getattr(w, "speech")
    date_added = getattr(w, "date_added")

    max_date = word_class.objects.latest('date_added').date_added
    min_date = datetime.date(2021,4,1)
    next_date = max_date
    prev_date = min_date
    num_days = datetime.timedelta(1)
    if date_of_word > min_date:
        prev_date = date_of_word - num_days
    if date_of_word < max_date:
        next_date = date_of_word + num_days

    context = {
        'word': word,
        'definition': definition,
        'speech': speech,
        'date_added': date_added,
        'next_date': next_date,
        'prev_date': prev_date
    }
    return render(request, 'word.html', context)

def words(request):
    rw = RandomWords()
    words = word_class.objects.order_by('-date_added')
    context = {
        'words': words
    }
    return render(request, 'words.html', context)
