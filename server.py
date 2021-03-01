from flask import Flask, render_template, request, redirect, url_for
import util
import time
import data_manager
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'


@app.route("/", methods=['GET', 'POST'])
def index_page():
    return redirect(url_for('questions_page', criteria='id', direction='asc'))


@app.route('/list')
def questions_page():
    # criteria = request.args.get('order_by', 'submission_time')
    # direction = request.args.get('order_direction', 'desc')
    unsorted_data = data_manager.get_questions()
    # sorted_data = util.sort_data(unsorted_data, criteria, direction)
    return render_template('list_questions.html', data=unsorted_data)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    question = data_manager.get_individual_question(question_id)
    answer = data_manager.get_individual_answer(question_id)
    return render_template('individual_question_and_answer_page.html', questions=question, answers=answer)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    if request.method == 'POST':
        img = request.files['img']
        submit_time = util.current_time()
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_manager.save_answer(submit_time, 0, question_id, request.form['message'], img.filename)
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_answers.html')


@app.route('/add-question', methods=['GET', 'POST'])
def add_question_page():
    if request.method == 'POST':
        img = request.files['img']
        submit_time = util.single_value_dateconverter(round(time.time()))
        #filename = str(uuid4())
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
        data_manager.save_question(submit_time, 0, 0, request.form['title'], request.form['message'], img.filename)
        # fetches the id of the new question
        new_id = [dict(row) for (row) in data_manager.get_questions()][-1].get('id')
        return redirect(url_for('individual_q_and_a', question_id=new_id))
    return render_template('add_question.html')


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.get_individual_question(question_id)
    if request.method == 'POST':
        #question = request.form.to_dict
        submit_time = util.single_value_dateconverter(round(time.time()))
        data_manager.update_question(question_id, request.form['title'], request.form['message'], submit_time)
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('edit_question.html', questionz=question)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = [dict(row) for row in data_manager.get_answer_by_id(answer_id)][0].get('question_id')
    if request.method == 'POST':
        submit_time = util.current_time()
        data_manager.update_answer(answer_id, request.form['message'], submit_time)
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('edit_answer.html', answer=answer, question_id=question_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    data_manager.delete_answer(answer_id)
    return redirect(url_for('questions_page', criteria='id', direction='asc'))


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    image_name = [dict(row) for row in data_manager.get_individual_question(question_id)][0].get('image')
    util.delete_image(image_name)
    data_manager.delete_question(question_id)
    return redirect(url_for('questions_page', criteria='title', direction='asc'))


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    data_manager.increment_question_vote_number(question_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    data_manager.decrement_question_vote_number(question_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_up/<answer_id>')
def answer_vote_up(question_id, answer_id):
    data_manager.increment_answer_vote_number(answer_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_down/<answer_id>')
def answer_vote_down(question_id, answer_id):
    data_manager.decrement_answer_vote_number(answer_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


if __name__ == "__main__":
    app.run(debug=True)
