import json
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Load the data from the JSON file
with open("data.json") as f:
    data = json.load(f)

city_dict = {}
for i in data:
    city_dict[i['pop2023']] = [i['country'], i['city']]

def comparison(a, b, score, choice):
    max_population = max(a, b)
    if (max_population == a and choice == "A") or (max_population == b and choice == "B"):
        score += 1
        result = "It's true."
    else:
        result = "Sorry, it's wrong."
    return score, result

@app.route('/', methods=['GET', 'POST'])
def play_game():
    if request.method == 'POST':
        score = int(request.form['score'])
        continuation = request.form['continuation']
        choice = request.form['choice']
        a = int(request.form['a'])
        b = int(request.form['b'])
        score, result = comparison(a, b, score, choice)
        if continuation == 'n':
            return render_template('final_score.html', score=score)
    else:
        score = 0
        result = ""

    information = random.choice(list(city_dict.items()))
    a, country_a, city_a = information[0], information[1][0], information[1][1]

    information = random.choice(list(city_dict.items()))
    b, country_b, city_b = information[0], information[1][0], information[1][1]

    return render_template('game.html', city_a=city_a, country_a=country_a, city_b=city_b, country_b=country_b, score=score, a=a, b=b, result=result)

@app.route('/stop', methods=['GET', 'POST'])
def stop_game():
    if request.method == 'POST':
        score = int(request.form['score'])
        return render_template('final_score.html', score=score)
    else:
        return render_template('final_score.html')

if __name__ == '__main__':
    app.run(debug=True)