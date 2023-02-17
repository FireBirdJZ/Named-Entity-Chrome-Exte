# app.py
import json
import flask
from flask import request, Flask, jsonify
import torch
from transformers import AutoTokenizer, AutoModel
import transformers
import random
from flask_cors import CORS
from transformers import pipeline, set_seed
from transformers import AutoTokenizer, AutoModelForTokenClassification
from bs4 import BeautifulSoup, NavigableString
import re

from ipymarkup import show_span_ascii_markup, show_dep_ascii_markup
from ipymarkup import show_span_box_markup
from ipymarkup.palette import palette, BLUE, RED, GREEN
from ipymarkup import format_span_box_markup


def highlight_entities(text, entities):
    color_map = {
        "PER": "pink",
        "ORG": "yellow",
        "LOC": "green"
    }
    default_color = "purple"
    highlighted_text = {}
    last_end = 0
    for entity in entities:
        label = entity["entity_group"]
        start = entity["start"]
        end = entity["end"]
        color = color_map.get(label, default_color)
        highlighted_text[text[last_end:start]] = text[last_end:start]
        highlighted_text[text[start:end]] = f'<span style="background-color: {color};">{text[start:end]}</span>'
        last_end = end
    highlighted_text[text[last_end:]] = text[last_end:]
    return highlighted_text


# def highlight_entities(text, entities):
#     color_map = {
#         "PER": "pink",
#         "ORG": "yellow",
#         "LOC": "green"
#     }
    
#     highlighted_text = {}
#     last_end = 0
#     for entity in entities:
#         label = entity["entity_group"]
#         start = entity["start"]
#         end = entity["end"]
#         if label not in color_map:
#             highlighted_text[text[last_end:end]] = text[last_end:end]
#         else:
#             color = color_map[label]
#             highlighted_text[text[last_end:start]] = text[last_end:start]
#             highlighted_text[text[start:end]] = f'<span style="background-color: {color};">{text[start:end]}</span>'
#         last_end = end
#     highlighted_text[text[last_end:]] = text[last_end:]
#     return highlighted_text

def update_html_with_highlights(html, highlighted_text):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all():
        if tag.string:
            highlighted_text_for_string = highlighted_text.get(tag.string)
            if highlighted_text_for_string:
                new_tag = BeautifulSoup(highlighted_text_for_string, "html.parser")
                tag.replace_with(new_tag)
    return str(soup)



def extract_text_from_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def prettify(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.prettify()





app = flask.Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def receive_text():
    if request.method == "POST":
        word = request.form
        print(word)
        return word
    return "This is a Flask server. Send a POST request with a form field named 'word' to print the word."



@app.route('/html', methods=['POST'])
def html():
   
    # Best working so far
    # html = request.data.decode('utf-8')
    # words = html.split()
    # modified_html = ""
    # for word in words:
    #   if word == "he":
    #     modified_html += "<span style='background-color: purple;'>" + word + "</span> "
    #   else:
    #     modified_html += word + " "
    # return modified_html

   
    html = request.data.decode("utf-8")
    text = extract_text_from_html(html)
    #tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
    #model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
    #ßnlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="max")

    # Trying differnt model
    model_checkpoint = "xlm-roberta-large-finetuned-conll03-english"
    nlp = pipeline("token-classification", model=model_checkpoint, aggregation_strategy="simple")
    
    entities = nlp(text)
    highlighted_text = highlight_entities(text, entities)


    updated_html = update_html_with_highlights(html, highlighted_text)

    # for entity in entities:
    #     label = entity["entity_group"]
    #     text = entity["word"]
    #     print(f"{label}: {text}")
    # spans = []
    # for entity in entities:
    #     label = entity["entity_group"]
    #     start = entity["start"]
    #     end = entity["end"]
    #     new_text += text[last_end:start]
    #     color = color_map.get(label, "black")
    #     new_text += f'<span style="color: {color};">{text[start:end]}</span>'
    #     last_end = end
    # new_text += text[last_end:
        # spans.append((entity["start"], entity["end"], entity["entity_group"]))

    #show_span_ascii_markup(text, spans)

    # show_span_box_markup(text, spans, palette=palette(PER=BLUE, ORG=RED, LOC=GREEN))

    # updated_text_with_spans = list(format_span_box_markup(text, spans))

    # need to turn the list into html object like string
    #return prettify(updated_text_with_spans)
    return (prettify(updated_html))





if __name__ == "__main__":
    app.run(debug=True)


