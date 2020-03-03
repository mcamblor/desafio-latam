import requests


def test_get_list_users_check_status_code_equals_200():
    response = requests.get("http://127.0.0.1:5000/get-people")
    assert response.status_code == 200

def test_get_list_users_check_content_type_equals_json():
    response = requests.get("http://127.0.0.1:5000/get-people")
    assert response.headers['Content-Type'] == "application/json"

def test_get_list_users_check_id_equals_0():
    response = requests.get("http://127.0.0.1:5000/get-people")
    response_body = response.json()
    assert response_body["people"][0]["id"] == 1

def test_get_list_users_check_firstname_equals_matias():
    response = requests.get("http://127.0.0.1:5000/get-people")
    response_body = response.json()
    assert response_body["people"][0]["first_name"] == "Matias"

def test_get_list_users_check_lastname_equals_camblor():
    response = requests.get("http://127.0.0.1:5000/get-people")
    response_body = response.json()
    assert response_body["people"][0]["lastname"] == "Camblot"

def test_get_list_users_check_format_date_equals_ddmmyy():
    response = requests.get("http://127.0.0.1:5000/get-people")
    response_body = response.json()
    assert response_body["people"][0]["new_birthday"] == "30/12/87"

def test_get_list_users_check_one_list_is_returned():
    response = requests.get("http://127.0.0.1:5000/get-people")
    response_body = response.json()
    assert len(response_body) == 1

def test_post_user_check_status_code_equals_200():
    response = requests.post(url='http://127.0.0.1:5000/birthday',data={'name':'basic_test2 postBirthday2','born':'02-02-1930'})
    assert response.status_code == 200

def test_post_user_check_status_code_equals_500():
    response = requests.post(url='http://127.0.0.1:5000/birthday',data={'name':'basic_test_fail postBirthday_fail','born':'02/02/1930'})
    assert response.status_code == 500
