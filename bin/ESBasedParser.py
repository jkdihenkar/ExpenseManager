from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, utils
import re

# TODO
def parse_date(str_date):
    """
    Sample input :: 07/03/17, 10:42 PM
    :param str_date: 
    :return: return datetime
    """
    pass


def get_record_details(line):
    """
    Sample input : 07/03/17, 10:42 PM - Jay Vora: Parakh, parth, kishan, hdk 110/5 to Jv roti
    :param line: 
    :return: 
    """
    if 'M -' in line:
        record_string = line.split('M -', maxsplit=1)[1]
        return record_string
    return None


def get_who_made_entry_and_entry(record_line):
    if ':' in record_line:
        record_user, record_line = record_line.split(':', maxsplit=1)
        return record_user, record_line

    return None


def ultimate_tokenizer(record_data):
    return re.findall(r"[\w\.\-']+", record_data)


def record_data_to_token(record_data):
    split = record_data.split('to', maxsplit=1)
    if len(split) > 1:
        return split
    split = record_data.split(']', maxsplit=1)
    if len(split) > 0:
        return split


def digits_only(str_amt):
    return re.findall(r"\d", str_amt)


def get_amount_from_record_string(record_data_from):
    # print("INPUT: {} , OUTPUT: {}".format(
    #     record_data_from, record_data_from.split(' ')[-1]
    # ))
    return record_data_from.split(' ')[-1]


def integration_test(es, data):
    step1 = get_record_details(
        data
    )

    print(step1)

    step2 = get_who_made_entry_and_entry(
        step1
    )

    print(step2)

    step3 = record_data_to_token(
        step2[1]
    )

    step3[0] = step3[0].rstrip()

    print(step3)

    amount_value = ultimate_tokenizer(get_amount_from_record_string(step3[0]))

    to_user = list(check_user_in_db(es, ultimate_tokenizer(step3[1])[0]))[0]

    if 'all' not in step3[0].lower():
        from_user_list = check_user_in_db(es, step3[0])
    else:
        try:
            from_user_list = check_user_in_db(es, step3[0])
            from_user_list = from_user_list - set([to_user])
            if '-' in step3[0]:
                removables =  check_user_in_db(es, step3[0].lower().replace('all', ''))
                from_user_list = from_user_list - removables
        except ValueError as ve:
            raise

    comment_string = ' '.join(ultimate_tokenizer(step3[1].lstrip(' '))[1:])

    operation_str = "split" if '/' in get_amount_from_record_string(step3[0]) else "group"

    if len(amount_value) > 1 and int(amount_value[1]) == len(from_user_list):
        operation_str = "group"
        amount_value[0] = str(
            float(amount_value[0]) / float(amount_value[1])
        )

    print("from : ",  from_user_list)
    print("amount : ", amount_value )
    print("to : ", to_user)
    print("comment : ", comment_string)
    print("operation : ", operation_str)

    out_file.write('./exec {} {} {} {} {}\n'.format(
        operation_str,
        ','.join(from_user_list),
        amount_value[0],
        to_user,
        comment_string
    ))

def check_user_in_db(es, user):
    search_q = Search(using=es, index='expense_manager', doc_type='user') \
        .query('match', username=user)

    result = search_q.scan()
    res = []
    for user_found in result:
        if isinstance(user_found.actual_username, utils.AttrList):
            res.extend(user_found.actual_username)
        else:
            res.append(user_found.actual_username)
    print(res)
    return set(res)

#integration_test("20/03/17, 10:13 PM - Jay Vora: jv kishan [9.4] to jd for perk")
if __name__ == "__main__":
    input_path = 'incoming_wa.txt'
    input_file = open(input_path, 'r+')
    out_file = open('commands.sh', 'w+')
    error_file = open('error_records.txt', 'w+')
    
    es = Elasticsearch(
        'http://127.0.0.1:9200',
        timeout=120
    )


    for line in input_file:
        try:
            integration_test(es, line)
        except Exception as e:
            print(e)
            error_file.write(line)

    out_file.close()
    error_file.close()
