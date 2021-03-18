from datetime import datetime
import os
import time
import jinja2
import data_manager
import bcrypt


def sort_data(data, sort_criteria, order):
    # if sort criteria is vote-number or view-count, the data gets so it can be sorted
    if data[0].get(sort_criteria).isnumeric():
        for sub in data:
            for key in sub:
                if key == sort_criteria:
                    sub[key] = int(sub[key])
    if order == 'desc':
        sorted_data = sorted(data, key=lambda k: k[sort_criteria], reverse=True)
    else:
        sorted_data = sorted(data, key=lambda k: k[sort_criteria])
    return sorted_data


def single_value_dateconverter(value):
    result = datetime.utcfromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
    return result


def delete_image(image_name):
    os.remove('static/images/' + image_name)


def current_time():
    return single_value_dateconverter(round(time.time()))


def highlight_searched_phrase(dict_input, search_phrase):
    for dictionary in dict_input:
        for key, text in dictionary.items():
            text = jinja2.escape(text)
            dictionary[key] = f'<b>{search_phrase}</b>'.join(text.split(search_phrase))
    return dict_input


def delete_question(question_id):
    # deletes question and it's related items
    data_manager.delete_tags_by_question_id(question_id)
    answers = data_manager.get_answers(question_id)
    for answer in answers:
        delete_image(answer.get('image'))
    comments_answer = comments_linked_to_answers(answers)
    for comment in comments_answer:
        data_manager.delete_comment(comment.get('id'))
    data_manager.delete_answers_by_question_id(question_id)
    data_manager.delete_comments_by_question_id(question_id)
    data_manager.delete_question(question_id)


def delete_question_or_answer(input_id, criteria):
    if criteria == 'question':
        image_name = data_manager.get_individual_question(input_id)[0].get('image')
        delete_image(image_name)
        delete_question(input_id)
    else:
        image_name = data_manager.get_answer_by_id(input_id)[0].get('image')
        delete_image(image_name)
        data_manager.delete_answer(input_id)


def comments_linked_to_answers(answers):
    comment_answer = []
    for item in range(len(answers)):
        comments = data_manager.get_comment_by_answer_id(answers[item].get('id'))
        for comment in comments:
            comment_answer.append(comment)
    return comment_answer


def get_parent_question_id(comment):
    question_id = comment[0].get('question_id')
    answer_id = comment[0].get('answer_id')
    if question_id:
        return question_id
    else:
        question = data_manager.get_question_id_by_answer_id(answer_id)
        question_id = question[0].get('question_id')
        return question_id


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


def get_user_id_by_question(question_id):
    return data_manager.get_individual_question(question_id)[0].get('user_id')


def get_user_id_by_answer(answer_id):
    return data_manager.get_answer_by_id(answer_id)[0].get('user_id')


def comments_linked_to_users(users):
    for i in range(len(users)):
        users[i]['num_of_com'] = 0
    for item in range(len(users)):
        comments = data_manager.get_comments_by_user_id(users[item].get('user_id'))
        users[item]['num_of_com'] = len(comments)
    return users


def answers_linked_to_users(users):
    for i in range(len(users)):
        users[i]['num_of_ans'] = 0
    for item in range(len(users)):
        answers = data_manager.get_answers_by_user_id(users[item].get('user_id'))
        users[item]['num_of_ans'] = len(answers)
    return users


def questions_linked_to_users(users):
    for i in range(len(users)):
        users[i]['num_of_q'] = 0
    for item in range(len(users)):
        questions = data_manager.get_questions_by_user_id(users[item].get('user_id'))
        users[item]['num_of_q'] = len(questions)
    return users


def comments_linked_to_user(users):
    users['num_of_com'] = 0
    comments = data_manager.get_comments_by_user_id(users.get('user_id'))
    users['num_of_com'] = len(comments)
    return users


def answers_linked_to_user(users):
    users['num_of_ans'] = 0
    answers = data_manager.get_answers_by_user_id(users.get('user_id'))
    users['num_of_ans'] = len(answers)
    return users


def questions_linked_to_user(users):
    users['num_of_q'] = 0
    questions = data_manager.get_questions_by_user_id(users.get('user_id'))
    users['num_of_q'] = len(questions)
    return users


def link_questions_answers_and_comments_to_user(users):
    users = comments_linked_to_user(users)
    users = answers_linked_to_user(users)
    users = questions_linked_to_user(users)
    return users


def link_questions_answers_and_comments_to_users(users):
    users = comments_linked_to_users(users)
    users = answers_linked_to_users(users)
    users = questions_linked_to_users(users)
    return users


def link_question_id_to_comment(user_id):
    comments = data_manager.get_comments_by_user_id(user_id)
    for i in range(len(comments)):
        question_id = comments[i].get('question_id')
        answer_id = comments[i].get('answer_id')
        if question_id is None:
            question = data_manager.get_question_id_by_answer_id(answer_id)
            question_id = question[0].get('question_id')
            comments[i]['question_id'] = question_id
    return comments