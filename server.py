from flask import Flask, render_template, request, redirect, url_for, session, escape, make_response, flash
import util
import data_manager
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/'
app.config['SECRET_KEY'] = 'BogdanBestProgrammerEver'


@app.route("/", methods=['GET', 'POST'])
def index_page():
    first_questions = data_manager.get_questions_by_time()
    return render_template('main.html', data=first_questions)


@app.route('/list', methods=['GET', 'POST'])
def questions_page():
    criteria = request.args.get('order_criteria', 'submission_time')
    direction = request.args.get('order_direction', 'DESC')
    sorted_data = data_manager.get_questions(criteria, direction)
    if request.method == 'POST':
        return redirect(url_for('search_results', search_phrase=request.form['search-input']))
    return render_template('new_list_questions.html', data=sorted_data, session=session)


@app.route('/question/<question_id>')
def individual_q_and_a(question_id):
    question = data_manager.get_individual_question(question_id)
    answer = data_manager.get_answers(question_id)
    question_tags = data_manager.get_question_tags(question_id)
    comments_question = data_manager.get_individual_comment(question_id)
    comments_answer = util.comments_linked_to_answers(answer)
    data_manager.increase_view_count(question_id)
    username = data_manager.get_user_by_id(util.get_user_id_by_question(question_id))
    return render_template('individual_question_and_answer_page.html', questions=question, answers=answer,
                           question_tags=question_tags, comments_question=comments_question,
                           comments_answer=comments_answer, session=session, username=username)


@app.route('/question/<question_id>/new-answer', methods=['GET', 'POST'])
def answer_page(question_id):
    if request.method == 'POST':
        img = request.files['img']
        submit_time = util.current_time()
        img_filename = str(uuid.uuid4())
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        data_manager.save_answer(submit_time, 0, question_id, request.form['message'], img_filename,
                                 session['user_id'])
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_answers.html', question_id=question_id, session=session)


@app.route('/add-question', methods=['GET', 'POST'])
def add_question_page():
    if request.method == 'POST':
        img = request.files['img']
        img_filename = str(uuid.uuid4())
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))
        data_manager.save_question(util.current_time(), 0, 0, request.form['title'], request.form['message'],
                                   img_filename, session['user_id'])
        new_id = data_manager.get_question_id(request.form['title'])[0].get('id')
        return redirect(url_for('individual_q_and_a', question_id=new_id))
    return render_template('add_question.html', session=session)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    user_id = util.get_user_id_by_question(question_id)
    question = data_manager.get_individual_question(question_id)
    if request.method == 'POST':
        data_manager.update_question(question_id, request.form['title'], request.form['message'], util.current_time())
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('edit_question.html', questionz=question, question_user_id=user_id, session=session)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    user_id = util.get_user_id_by_answer(answer_id)
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer[0].get('question_id')
    if request.method == 'POST':
        data_manager.update_answer(answer_id, request.form['message'], util.current_time())
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('edit_answer.html', answer=answer, question_id=question_id, session=session,
                           answer_user_id=user_id)


@app.route('/answer/<answer_id>/delete')
def delete_answer(answer_id):
    answer = data_manager.get_answer_by_id(answer_id)
    question_id = answer[0].get('question_id')
    if 'user' in session:
        user_id = data_manager.get_answer_by_id(answer_id)[0].get('user_id')
        if session['user_id'] == user_id:
            util.delete_question_or_answer(answer_id, 'answer')
            data_manager.delete_answer(answer_id)
            return redirect(url_for('individual_q_and_a', question_id=question_id))
    else:
        return render_template('access_denied.html', question_id=question_id)


@app.route('/question/<question_id>/delete')
def delete_question(question_id):
    if 'user' in session:
        user_id = util.get_user_id_by_question(question_id)
        if session['user_id'] == user_id:
            util.delete_question_or_answer(question_id, 'question')
        return redirect(url_for('questions_page'))
    else:
        return render_template('access_denied.html', question_id=question_id)


@app.route('/question/<question_id>/vote_up')
def vote_up_question(question_id):
    data_manager.increment_question_vote_number(question_id)
    user_id = util.get_user_id_by_question(question_id)
    data_manager.increase_user_rep_by_question(user_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_down')
def vote_down_question(question_id):
    data_manager.decrement_question_vote_number(question_id)
    user_id = util.get_user_id_by_question(question_id)
    data_manager.decrease_user_reputation(user_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_up/<answer_id>')
def answer_vote_up(question_id, answer_id):
    data_manager.increment_answer_vote_number(answer_id)
    user_id = util.get_user_id_by_answer(answer_id)
    data_manager.increase_user_rep_by_answer(user_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/vote_down/<answer_id>')
def answer_vote_down(question_id, answer_id):
    data_manager.decrement_answer_vote_number(answer_id)
    user_id = util.get_user_id_by_answer(answer_id)
    data_manager.decrease_user_reputation(user_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/question/<question_id>/new-tag', methods=['GET', 'POST'])
def add_new_tag(question_id):
    user_id = util.get_user_id_by_question(question_id)
    current_tags = data_manager.get_existing_tags()
    if request.method == 'POST':
        if request.form['building'] == 'casinos':
            data_manager.insert_tag(request.form['tag-name'])
            return redirect(url_for('add_new_tag', question_id=question_id))
        if request.form['building'] == 'caves':
            for row in current_tags:
                if row['name'] == request.form['tag-select']:
                    tag_id = row.get('id')
            data_manager.insert_questions_tag(question_id, tag_id)
            return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_tag.html', current_tags=current_tags, question_id=question_id, session=session,
                           tag_user_id=user_id)


@app.route('/question/<question_id>/tag/<tag_id>/delete')
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/search?q=<search_phrase>')
def search_results(search_phrase):
    modified_search_phrase = '%' + search_phrase + '%'
    question_results = data_manager.search_in_questions(modified_search_phrase)
    answer_results = data_manager.search_in_answers(modified_search_phrase)
    question_results = util.highlight_searched_phrase(question_results, search_phrase)
    answer_results = util.highlight_searched_phrase(answer_results, search_phrase)
    return render_template('search_results.html', questions=question_results, search_phrase=search_phrase,
                           answers=answer_results)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_comment_question(question_id):
    if request.method == 'POST':
        submit_time = util.current_time()
        data_manager.save_comment(submit_time, question_id, None, 0, request.form['message'], session['user_id'])
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_comment.html', question_id=question_id)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_answer(answer_id):
    question = data_manager.get_question_id_by_answer_id(answer_id)
    question_id = question[0].get('question_id')
    if request.method == 'POST':
        submit_time = util.current_time()
        data_manager.save_comment(submit_time, None, answer_id, 0, request.form['message'], session['user_id'])
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('add_comment.html', question_id=question_id)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment_user_id = data_manager.get_comment_by_id(comment_id)[0].get('user_id')
    comment = data_manager.get_comment_by_id(comment_id)
    edit_count = comment[0].get('edited_count') + 1
    question_id = util.get_parent_question_id(comment)
    if request.method == 'POST':
        data_manager.update_comment(comment_id, request.form['message'], edit_count, util.current_time())
        return redirect(url_for('individual_q_and_a', question_id=question_id))
    return render_template('edit_comment.html', comment=comment, question_id=question_id,
                           comment_user_id=comment_user_id,
                           session=session)


@app.route('/comment/<comment_id>/delete')
def delete_comment(comment_id):
    comment = data_manager.get_comment_by_id(comment_id)
    question_id = util.get_parent_question_id(comment)
    if 'user' in session:
        user_id = data_manager.get_comment_userid(comment_id)[0].get('user_id')
        if session['user_id'] == user_id:

            data_manager.delete_comment(comment_id)
            return redirect(url_for('individual_q_and_a', question_id=question_id))
    else:
        return render_template('access_denied.html', question_id=question_id)


@app.route('/register', methods=['GET', 'POST'])
def registration_page():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        user_id = data_manager.get_user_id(username)
        if user_id is not None:
            flash('This username has been taken')
            return render_template('register.html')
        hashed_password = util.hash_password(request.form['password'])
        data_manager.add_user(username, hashed_password, util.current_time())
        return redirect(url_for('questions_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'user' in session:
        return redirect(url_for('questions_page'))
    else:
        if request.method == 'POST':
            data = data_manager.get_user_credentials(request.form['username'])
            if len(data) == 0:
                flash('Incorrect username and password')
            else:
                hashed_password = data[0].get('password')
                if util.verify_password(request.form['password'], hashed_password):
                    session['user'] = request.form['username']
                    session['user_id'] = data[0].get('user_id')
                    return redirect(url_for('questions_page'))
                else:
                    flash('Incorrect username and password')
        return render_template('login.html')


@app.route('/tags')
def tags_page():
    tags_list = data_manager.get_tags()
    return render_template('list_tags.html', tags_list=tags_list)


@app.route('/logout')
def logout_page():
    if 'user' in session:
        session.pop('user', None)
        session.pop('user_id', None)
    return redirect(url_for('questions_page'))


@app.route("/question/<question_id>/answer/<answer_id>/accept")
def accept_answer(question_id, answer_id):
    if 'user' in session:
        user_id = util.get_user_id_by_question(question_id)
        if session['user_id'] == user_id:
            data_manager.accept_answer(answer_id)
            user_id = util.get_user_id_by_answer(answer_id)
            data_manager.increase_rep_accepted_answer(user_id)
        else:
            flash('You do not have permission to do that')
    return redirect(url_for('individual_q_and_a', question_id=question_id))


@app.route('/users')
def users_page():
    if 'user' in session:
        users = data_manager.get_all_users()
        users = util.link_questions_answers_and_comments_to_users(users)
        return render_template('users.html', users=users, session=session)
    else:
        return redirect(url_for('login_page'))


@app.route('/user/<user_id>')
def individual_user(user_id):
    if 'user' in session:
        user = data_manager.get_user_by_id(user_id)
        user = util.link_questions_answers_and_comments_to_user(user)
        questions = data_manager.get_questions_by_user_id(user_id)
        answers = data_manager.get_answers_by_user_id(user_id)
        comments = util.link_question_id_to_comment(user_id)
        return render_template('individual_user.html', user=user, questions=questions, answers=answers,
                               comments=comments, session=session)


if __name__ == "__main__":
    app.run(debug=True)
