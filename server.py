from flask import Flask, render_template, request, redirect, url_for
import util
import time
import data_manager
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/tutu/Desktop/projects/web/ask-mate-1-python-bogdaniordan/static/images/'


@app.route("/")
def index_page():
    return redirect(url_for('questions_page', criteria='id', direction='asc'))


@app.route('/list/order_by=<criteria>&order_direction=<direction>', methods=['GET', 'POST'])
def questions_page(criteria, direction):
    unsorted_data = data_manager.read_from_csv(data_manager.questions_file)
    sorted_data = util.sort_data(unsorted_data, criteria, direction)
    return render_template('list_questions.html', data=sorted_data)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    question = data_manager.get_question_or_answer('id', data_manager.questions_file, question_id)
    answer = data_manager.get_question_or_answer('question_id', data_manager.answers_file, question_id)
    return render_template('individual_question_and_answer_page.html', questions=question, answers=answer)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    raw_data = data_manager.read_from_csv(data_manager.answers_file)
    if request.method == 'POST':
        new_id = int(raw_data[-1].get('id')) + 1
        img = request.files['img']
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_row = {'id': new_id, 'submission_time': int(round(time.time())), 'vote_number': 0,
                    'question_id': question_id, 'message': request.form['message'], 'image': img.filename}
        data_manager.append_to_csv(data_row, data_manager.ANSWER_HEADER, data_manager.answers_file)
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_answers.html')

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


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == "POST":
        questions = data_manager.read_from_csv(data_manager.questions_file)
        question = questions[int(question_id) - 1]
        id = int(question['id'])
        updated_question = dict(request.form)
        updated_question = dict((k.lower(), v.capitalize()) for k, v in updated_question.items())
        updated_question['id'] = updated_question.get(id, str(id))
        data_manager.edit_question(updated_question)
        print(updated_question)
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    else:
        questions = data_manager.read_from_csv(data_manager.questions_file)
        question = questions[int(question_id) - 1]
        id = int(question['id'])
        updated_question = dict(request.form)
        updated_question['id'] = updated_question.get(id, str(id))

        return render_template("edit_question.html", question=question)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    raw_data = data_manager.read_from_csv(data_manager.answers_file)
    data_manager.delete_from_csv(answer_id, raw_data, data_manager.ANSWER_HEADER, data_manager.answers_file)
    return redirect(url_for('questions_page', criteria='id', direction='asc'))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    raw_data = data_manager.read_from_csv(data_manager.questions_file)
    data_manager.delete_image(data_manager.questions_file, question_id)
    data_manager.delete_from_csv(question_id, raw_data, data_manager.QUESTION_HEADER, data_manager.questions_file)
    return redirect(url_for('questions_page', criteria='title', direction='asc'))


@app.route("/question/<question_id>/vote_up")
def vote_up(question_id):
    data_manager.vote_questions(data_manager.questions_file, question_id, 'up')
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route("/question/<question_id>/vote_down")
def vote_down(question_id):
    data_manager.vote_questions(data_manager.questions_file, question_id, 'down')
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/answer/<answer_id>/vote_up')
def answer_vote_up(answer_id):
    answers = data_manager.read_from_csv(data_manager.answers_file)
    for row in answers:
        if row['id'] == answer_id:
            question_id = row['question_id']
    data_manager.vote_answer(data_manager.answers_file, answer_id, 'up')
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/answer/<answer_id>/vote_down')
def answer_vote_down(answer_id):
    answers = data_manager.read_from_csv(data_manager.answers_file)
    for row in answers:
        if row['id'] == answer_id:
            question_id = row['question_id']
    data_manager.vote_answer(data_manager.answers_file, answer_id, 'down')
    return redirect(url_for('individual_q_and_a', question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)
