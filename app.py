from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", message=None, sum_result=None)

@app.route('/hello', methods=['POST'])
def hello():
    name = request.form.get('username','').strip()
    if name:
        return render_template("index.html", message=f"Hello {name}, welcome to Jenkins CI/CD demo!", sum_result=None)
    else:
        return render_template("index.html", message="Hello there", sum_result=None)

@app.route('/sum', methods=['POST'])
def calculate_sum():
    try:
        a = float(request.form.get('a', 0))
        b = float(request.form.get('b', 0))
        result = a + b
        return render_template("index.html", message=None, sum_result=result)
    except ValueError:
        return render_template("index.html", message=None, sum_result="Invalid input")




if __name__ == "__main__":
    app.run()


# test webhook
# nouvelle modif
