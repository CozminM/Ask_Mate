from flask import Flask, render_template, request, redirect, url_for
import util
import time
import data_manager
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/bogdan/Desktop/web projects/ask-mate-1-python-bogdaniordan/static/images'


@app.route("/")
def hello():
    return '<a href="/list/order_by=title&order_direction=asc">List stories</a>'


@app.route('/list/order_by=<criteria>&order_direction=<direction>', methods=['GET', 'POST'])
def questions_page(criteria, direction):
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    data = util.sort_data(raw_data, str(criteria), str(direction))
    if request.method == 'POST':
        img = request.files['img']
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_row = {'id': int(raw_data[-1].get('id')) + 1, 'submission_time': int(round(time.time())), 'view_number': 0,
                    'vote_number': 0, 'title': request.form['title'], 'image': img.filename,
                    'message': request.form['message']}
        data_manager.append_to_csv(data_row, data_manager.QUESTION_HEADER, data_manager.questions_file)
        return redirect(url_for('individual_q_and_a', question_id=data_row.get('id')))
    return render_template('list_questions.html', data=data)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
