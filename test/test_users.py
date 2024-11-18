from fastapi import status

from .utils import *
from ..routers.users import get_current_user, get_db

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[get_db] = override_get_db


def test_return_user(test_user):
    response = client.get('/user')
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == 'surya'
    assert response.json()['email'] == 'test@test.com'
    assert response.json()['first_name'] == 'Surya'
    assert response.json()['last_name'] == 'Singh'
    assert response.json()['role'] == 'admin'
    assert response.json()['phone_number'] == '(05461)-211112'


def test_change_password_success(test_user):
    response = client.put('/user/password', json={'password': 'testpassword',
                                                  'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_change_password_invalid_password(test_user):
    response = client.put('/user/password', json={'password': 'wrong_password',
                                                  'new_password': 'newpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect password.'}


def test_change_phone_number_success(test_user):
    response = client.put('/user/phonenumber/05461211112')
    assert response.status_code == 204
