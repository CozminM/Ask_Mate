from datetime import datetime
import os
import time
import jinja2
import data_manager


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


def convert_to_dict(value):
    return [dict(row) for row in value]


def highlight_searched_phrase(dict_input, search_phrase):
    for dictionary in dict_input:
        for key, text in dictionary.items():
            text = jinja2.escape(text)
            dictionary[key] = f'<b>{search_phrase}</b>'.join(text.split(search_phrase))
    return dict_input


def delete_question_or_answer(input_id, criteria):
    if criteria == 'question':
        image_name = data_manager.get_individual_question(input_id)[0].get('image')
        delete_image(image_name)
        data_manager.delete_question(input_id)
    else:
        image_name = data_manager.get_answer_by_id(input_id)[0].get('image')
        delete_image(image_name)
        data_manager.delete_answer(input_id)

def get_comment_by_answer(answer):
    comment_answer = []
    for i in range(len(answer)):
        one_comment = data_manager.get_comment_by_answer_id(answer[i].get('id'))
        for j in one_comment:
            comment_answer.append(j)
    return comment_answer