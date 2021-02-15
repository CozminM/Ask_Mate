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


@app.route('/list/order_by=<criteria>&order_direction=<direction>', methods=['GET', 'POST'])
def questions_page(criteria, direction):
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    sorted_data = util.sort_data(raw_data, criteria, direction)
    return render_template('list_questions.html', data=sorted_data)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    question = data_manager.get_question_or_answer('id', data_manager.questions_file, question_id)
    answer = data_manager.get_question_or_answer('question_id', data_manager.answers_file, question_id)
    return render_template('individual_question_and_answer_page.html', questions=question, answers=answer)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question_page():
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    if request.method == 'POST':
        new_id = int(raw_data[-1].get('id')) + 1
        img = request.files['img']
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_row = {'id': new_id, 'submission_time': int(round(time.time())), 'view_number': 0,
                    'vote_number': 0, 'title': request.form['title'], 'image': img.filename,
                    'message': request.form['message']}
        data_manager.append_to_csv(data_row, data_manager.QUESTION_HEADER, data_manager.questions_file)
        return redirect(url_for('individual_q_and_a', question_id=new_id))
    return render_template('add_question.html')


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    raw_data = data_manager.read_from_csv(data_manager.answers_file)
    data_manager.delete_from_csv(answer_id, raw_data, data_manager.ANSWER_HEADER, data_manager.answers_file)
    return redirect(url_for('individual_q_and_a', question_id=answer_id))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    data_manager.delete_image(data_manager.questions_file, question_id)
    data_manager.delete_from_csv(question_id, raw_data, data_manager.QUESTION_HEADER, data_manager.questions_file)
    return redirect(url_for('questions_page', criteria='title', direction='asc'))


if __name__ == "__main__":
    app.run(debug=True)
