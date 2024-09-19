from flask import Flask, send_from_directory, render_template

flask_app = Flask(__name__)

@flask_app.route('/')
def home():
    return render_template('index.html')

@flask_app.route('/resume')
def resume():
    return send_from_directory('static', 'resume.pdf')

if __name__ == "__main__":
    flask_app.run(debug=True)
