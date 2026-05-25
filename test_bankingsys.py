from fastapi.testclient import TestClient
from bankingsys import app
import uuid

client = TestClient(app)

def test_wrong_login():

    response = client.post(
        "/login",
        data={
            "username":"aarush",
            "password":"wrongpassword"
        }
    )

    assert response.status_code == 401

def test_login():
    response= client.post(
        "/login",
        data = {
            "username" :"aarush",
            "password":"aarushpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_user_not_found():
    response = client.post(
        "/login",
        data={
            "username": "nobody",
            "password": "nobodypassword"
        }
    )
    assert response.status_code == 404

def test_no_token():
    response = client.post(
        "/users/",

    )
    assert response.status_code == 401

def get_token():
    response = client.post(
        "/login",
        data={
            "username":"aarush",
            "password":"aarushpassword"
        }
    )
    return response.json()["access_token"]
import uuid

def get_normal_user_token():

    admin_token = get_token()

    username = f"user_{uuid.uuid4().hex[:8]}"

    client.post(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {admin_token}"
        },
        json={
            "UserName":username,
            "UserPassword":"Test123",
            "UserBalance":"1000",
            "UserEmail":f"{username}@test.com"
        }
    )

    response = client.post(
        "/login",
        data={
            "username":username,
            "password":"Test123"
        }
    )

    return response.json()["access_token"]


def test_create_user():

    token = get_token()

    username = f"pytest_{uuid.uuid4().hex[:8]}"
    useremail = f"pytest_{uuid.uuid4().hex[:8]}"
    response = client.post(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "UserName": username,
            "UserPassword":"Test123",
            "UserBalance":"1000",
            "UserEmail":useremail
        }
    )

    assert response.status_code == 200

def test_deposit():

    token = get_token()

    response = client.post(
        "/deposit/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "Amount":"500"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["Amount"] == "500.00"

def test_negative_deposit():

    token = get_token()

    response = client.post(
        "/deposit/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "Amount":"-500"
        }
    )

    assert response.status_code == 400
def test_withdrawal():

    token = get_token()

    response = client.post(
        "/withdrawal/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "Amount":"100"
        }
    )

    assert response.status_code == 200
def test_insufficient_withdrawal():

    token = get_token()

    response = client.post(
        "/withdrawal/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "Amount":"999999999"
        }
    )

    assert response.status_code == 400

def test_transaction():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "RecieverID":5,
            "TransactionAmount":"100"
        }
    )

    assert response.status_code == 200
def test_invalid_receiver():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "RecieverID":99999,
            "TransactionAmount":"100"
        }
    )

    assert response.status_code == 404
def test_negative_transaction():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "RecieverID":5,
            "TransactionAmount":"-100"
        }
    )

    assert response.status_code == 400
def test_insufficient_transaction_balance():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "RecieverID":5,
            "TransactionAmount":"999999999"
        }
    )

    assert response.status_code == 400
def test_sender_same_as_receiver():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "RecieverID":1,
            "TransactionAmount":"100"
        }
    )

    assert response.status_code == 400

def test_non_admin_view_users():

    user_token = get_normal_user_token()

    response = client.get(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 403
import uuid

def test_old_token_invalid_after_password_change():

    token = get_token()

    username = f"token_{uuid.uuid4().hex[:8]}"

    client.post(
        "/users/",
        headers={
            "Authorization":f"Bearer {token}"
        },
        json={
            "UserName":username,
            "UserPassword":"Test123",
            "UserBalance":"1000",
            "UserEmail":f"{username}@test.com"
        }
    )

    login = client.post(
        "/login",
        data={
            "username":username,
            "password":"Test123"
        }
    )

    old_token = login.json()["access_token"]

    client.put(
        "/users/",
        headers={
            "Authorization":f"Bearer {old_token}"
        },
        json={
            "UserName":username,
            "UserPassword":"Changed123",
            "UserEmail":f"{username}@test.com"
        }
    )

    response = client.get(
        "/transactions/",
        headers={
            "Authorization":f"Bearer {old_token}"
        }
    )

    assert response.status_code == 401
def test_transaction_history():

    token = get_token()

    response = client.get(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        }
    )

    assert response.status_code == 200
def test_deposit_history():

    token = get_token()

    response = client.get(
        "/deposits/",
        headers={
            "Authorization":
            f"Bearer {token}"
        }
    )

    assert response.status_code == 200
def test_withdrawal_history():

    token = get_token()

    response = client.get(
        "/withdrawal/",
        headers={
            "Authorization":
            f"Bearer {token}"
        }
    )

    assert response.status_code == 200
def test_missing_deposit_amount():

    token = get_token()

    response = client.post(
        "/deposit/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={}
    )

    assert response.status_code == 422
def test_missing_withdrawal_amount():

    token = get_token()

    response = client.post(
        "/withdrawal/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={}
    )

    assert response.status_code == 422
def test_missing_receiver():

    token = get_token()

    response = client.post(
        "/transactions/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "TransactionAmount":"100"
        }
    )

    assert response.status_code == 422
def test_large_deposit():

    token = get_token()

    response = client.post(
        "/deposit/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "Amount":"1000000"
        }
    )

    assert response.status_code == 200
def test_empty_username():

    token = get_token()

    response = client.post(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "UserName":"",
            "UserPassword":"Test123",
            "UserBalance":"1000",
            "UserEmail":"test@test.com"
        }
    )

    assert response.status_code in [400,422]

def test_non_admin_view_users():

    user_token = get_normal_user_token()

    response = client.get(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 403


def test_non_admin_create_user():

    user_token = get_normal_user_token()

    response = client.post(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {user_token}"
        },
        json={
            "UserName":"abc",
            "UserPassword":"123",
            "UserBalance":"1000",
            "UserEmail":"abc@test.com"
        }
    )

    assert response.status_code == 403


def test_non_admin_view_transactions():

    user_token = get_normal_user_token()

    response = client.get(
        "/transanctions/",
        headers={
            "Authorization":
            f"Bearer {user_token}"
        }
    )

    assert response.status_code == 403
def test_delete_nonexistent_user():

    token = get_token()

    response = client.delete(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        params={
            "userID":999999
        }
    )

    assert response.status_code == 404


def test_delete_self():

    token = get_token()

    response = client.delete(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        params={
            "userID":1
        }
    )

    assert response.status_code == 400
import uuid

def test_update_user():

    token = get_normal_user_token()

    new_username = f"updated_{uuid.uuid4().hex[:8]}"

    response = client.put(
        "/users/",
        headers={
            "Authorization":
            f"Bearer {token}"
        },
        json={
            "UserName":new_username,
            "UserPassword":"NewPassword123",
            "UserEmail":"updated@test.com"
        }
    )

    assert response.status_code == 200

    assert response.status_code == 200

    assert response.status_code == 200