from flask import Flask, render_template, request, redirect, url_for
import util
import time
import data_manager
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/home/bogdan/Desktop/web projects/ask-mate-1-python-bogdaniordan/static/images'


@app.route("/")
def index_page():
    return redirect(url_for('questions_page', criteria='id', direction='asc'))


#or use uuid for id
@app.route('/list/order_by=<criteria>&order_direction=<direction>', methods=['GET', 'POST'])
def questions_page(criteria, direction):
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    sorted_data = util.sort_data(raw_data, criteria, direction)
    if request.method == 'POST':
        img = request.files['img']
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_row = {'id': int(raw_data[-1].get('id')) + 1, 'submission_time': int(round(time.time())), 'view_number': 0,
                    'vote_number': 0, 'title': request.form['title'], 'image': img.filename,
                    'message': request.form['message']}
        data_manager.append_to_csv(data_row, data_manager.QUESTION_HEADER, data_manager.questions_file)
        return redirect(url_for('individual_q_and_a', question_id=data_row.get('id')))
    return render_template('list_questions.html', data=sorted_data)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    question = data_manager.get_question_or_answer('id', data_manager.questions_file, question_id)
    answer = data_manager.get_question_or_answer('question_id', data_manager.answers_file, question_id)
    return render_template('individual_question_and_answer_page.html', questions=question, answers=answer)


if __name__ == "__main__":
    app.run(debug=True)
