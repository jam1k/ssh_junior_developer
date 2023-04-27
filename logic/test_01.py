from backend import app
import json

def test_post_board_format():
    # Should fail if is not string
    data = {
        "board": 123
        }
    response = app.test_client().post(
        '/api/v1/games',
        data = json.dumps(data),
        headers = {"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "must be of string type"
    assert response.status_code == 400


def test_post_board_wronglength_short():
    # Should fail if the board string is not 9 char
    data = {
        "board": "---"
        } #too short
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == 'min length is 9'
    assert response.status_code == 400


def test_post_board_wronglength_long():
    # Should fail if the board string is not 9 char
    data = {
        "board": "---------------------"
        } # board too long
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == 'max length is 9'
    assert response.status_code == 400


def test_post_board_not_allowed_chars():
    # Should fail if contains not allowed chars
    data = {
        "board": "--------Y"
        } # not allowed Y
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "value does not match regex '[OX-]+'"
    assert response.status_code == 400


def test_post_board_more_O():
    # Should fail if contains more than one O
    data = {
        "board": "-------OO"
        } # more O
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "Initial board should have all - or one O move"
    assert response.status_code == 400


def test_post_board_O_X():
    # Should fail if contains one O and one X
    data = {
        "board": "-------XO"
        } # one O and one X
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "Initial board should have all either one X or one Y"
    assert response.status_code == 400


def test_post_board_more_X():
    # Should fail if contains more than one X
    data = {
        "board": "-------XX"
        } # more X
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "Initial board should have all - or one X move"
    assert response.status_code == 400


def test_put_board_format():
    # Should fail if board is not string
    data = {
        "board": 123
        }
    response = app.test_client().put(
        '/api/v1/games/<game_id>',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "must be of string type"
    assert response.status_code == 400


def test_put_board_wronglength_short():
    # Should fail if the board string is not 9 char
    data = {
        "board": "---"
        } #too short
    response = app.test_client().put(
        '/api/v1/games/<game_id>',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == 'min length is 9'
    assert response.status_code == 400


def test_put_board_wronglength_long():
    # Should fail if the board string is not 9 char
    data = {
        "board": "------------------"
        } #too long
    response = app.test_client().put(
        '/api/v1/games/<game_id>',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == 'max length is 9'
    assert response.status_code == 400


def test_put_board_not_allowed_chars():
    # Should fail if the board string contains not allowed chars
    data = {
        "board": "--------Y"
        } #not allowed Y
    response = app.test_client().put(
        '/api/v1/games/<game_id>',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "value does not match regex '[OX-]+'"
    assert response.status_code == 400


def test_put_board_not_found():
    # game not found
    data = {
        "board": "-------XO"
        } 
    response = app.test_client().put(
        '/api/v1/games/d00d0ad3-d04a-45c0-b2af-93e41c70fc9b',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    res = json.loads(response.data.decode('utf-8'))
    assert res["reason"] == "game not found"
    assert response.status_code == 404

def test_correct_data():
    # sending correct data
    data = {
        "board": "---------"
        }
    response = app.test_client().post(
        '/api/v1/games',
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
        )
    assert response.status_code == 201

