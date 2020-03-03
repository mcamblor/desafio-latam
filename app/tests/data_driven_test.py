import requests
import pytest
import csv
import os

base_dir = os.path.dirname(os.path.realpath(__file__))

test_data_correct_id = [
    ("1","Faltan 303 días para tu cumpleaños"),
    ("5","Faltan 336 días para tu cumpleaños"),
    ("10","Faltan 303 días para tu cumpleaños")
]

test_data_incorrect_id = [
    ("100","No se encontró persona con ese id!"),
    ("-1","No se encontró persona con ese id!")
]


@pytest.mark.parametrize("id_user, expected_message", test_data_correct_id)
def test_using_test_data_object_get_user_check_correct_message(id_user, expected_message):
    response = requests.get(f"http://127.0.0.1:5000/get-people-id/{id_user}")
    response_body = response.json()
    if response_body["person"]['id'] == id_user:
        assert response_body["person"]['id']["message"] == expected_message


@pytest.mark.parametrize("id_user, expected_message", test_data_incorrect_id)
def test_using_test_data_object_get_user_check_incorrect_message(id_user, expected_message):
    response = requests.get(f"http://127.0.0.1:5000/get-people-id/{id_user}")
    response_body = response.json()
    assert response_body["message"] == expected_message


def read_test_data_from_csv():
    test_data = []
    with open('{}/test_data.csv'.format(base_dir), newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)  # skip header row
        for row in data:
            test_data.append(row)
    return test_data


@pytest.mark.parametrize("name, born, expected_message", read_test_data_from_csv())
def test_using_csv_get_location_data_check_place_name(name, born, expected_message):
    response = requests.post(url="http://127.0.0.1:5000/birthday",data={'name':name,'born':born})
    response_body = response.json()
    assert response_body["message"] == expected_message