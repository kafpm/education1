from flask import Flask, render_template as render

app = Flask(__name__, static_folder='public', template_folder='public')

@app.route('/')
def main():
    return render('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=8000)
