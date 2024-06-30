from flask import Flask, render_template
import random
import datetime
app = Flask(__name__)

@app.route('/')
def hello_world():
  random_number = random.randint(1, 100)
  current_year = datetime.datetime.now().year
  return render_template("index.html", num=random_number, yr=current_year)

@app.route('/anotherpage')
def get_another_page():
  return render_template("anotherpage.html")

if __name__ == "__main__":
  app.run(debug=True)