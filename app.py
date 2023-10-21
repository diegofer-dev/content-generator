import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    product_name = "Product Name"
    product_header = "Product Header"
    product_introduction = "Product Introduction"
    product_list = ["Item 1", "Item 2", "Item 3"]
    product_advantages = ["Ventaja 1", "Ventaja 2", "Ventaja 3"]
    product_conclusion = "Product Conclusion"
    result = False
    if request.method == "POST":
        product_name = request.form["product"]
        # El encabezado
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Escribe en español el título del encabezado para un artículo del producto: {product_name}",
            temperature=0.4,
            max_tokens=70,
            stop="."
        )
        if response:
            product_header = response.choices[0].text

        # La introduccion
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Escribe en español una descripción detallada del producto: {product_name}\n",
            temperature=0.6,
            max_tokens=3900,
            top_p=1,
            frequency_penalty=0.27,
            presence_penalty=0.58
        )
        if response:
            product_introduction = response.choices[0].text
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"Completa este artículo hasta que tenga 500 palabras:\n {product_introduction}\n",
                temperature=0.6,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0.27,
                presence_penalty=0.58
            )
            product_introduction += response.choices[0].text

        # La lista de caracteristicas tecnicas
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Escribe en español una lista de las características técnicas del prodcuto: {product_name}\n",
            temperature=0.4,
            max_tokens=1000
        )
        if response:
            unproccesed_list = response.choices[0].text
            product_list = list(
                map(lambda e: e[1:], unproccesed_list.split("\n")))[1:]

        # la lista de ventajas
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Escribe en español una lista detallada de las ventajas del prodcuto: {product_name}\n",
            temperature=0.6,
            max_tokens=2000
        )
        if response:
            unproccesed_list = response.choices[0].text
            product_advantages = list(map(
                lambda e: e[1:], unproccesed_list.split("\n")))[1:]

        # La conclusión
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=f"Escribe en español una conclusión para un artículo del producto: {product_name}\n\nEn conclusión a lo visto anteriormente",
            temperature=0.73,
            max_tokens=3900,
            top_p=1,
            frequency_penalty=0.27,
            presence_penalty=0.58
        )
        if response:
            product_conclusion = response.choices[0].text
            response = openai.Completion.create(
                model="text-davinci-002",
                prompt=f"Completa este artículo hasta que tenga 300 palabras:\n {product_conclusion}\n",
                temperature=0.73,
                max_tokens=3000,
                top_p=1,
                frequency_penalty=0.27,
                presence_penalty=0.58
            )
            product_conclusion += response.choices[0].text

        result = True

    return render_template("index.html", product_name=product_name,
                           product_header=product_header,
                           product_introduction=product_introduction,
                           product_list=product_list,
                           product_advantages=product_advantages,
                           product_conclusion=product_conclusion,
                           result=result)
