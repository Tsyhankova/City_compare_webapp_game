import pytest
from flask import Flask
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """
    Test if the home page loads successfully.
    returns a response with a status code of 200
    and contains the expected content
    """
    response = client.get('/')
    assert response.status_code == 200
    assert b"Compare cities" in response.data

def test_play_game_correct_answer(client):
    """Test the game's behavior when the user selects the correct answer."""
    response = client.post('/',
                           data={'score': '0', 'continuation': 'y', 'choice': 'A', 'a': '1000', 'b': '500'}
                           )
    assert response.status_code == 200
    assert b"Score: 1" in response.data
    assert b"It's true." in response.data

def test_play_game_incorrect_answer(client):
    """Test the game's behavior when the user selects the incorrect answer."""
    response = client.post('/',
                           data={'score': '0', 'continuation': 'y', 'choice': 'B', 'a': '1000', 'b': '500'}
                           )
    assert response.status_code == 200
    assert b"Score: 0" in response.data
    assert b"Sorry, it's wrong." in response.data

def test_stop_game_with_score(client):
    """
    Test the behavior when the user chooses to stop the game
    and has a non-zero score.
    """
    response = client.post('/stop', data={'score': '5'})
    assert response.status_code == 200
    assert b"Final Score: 5" in response.data

def test_stop_game_no_score(client):
    """
    Test the behavior when the user chooses to stop the game
    and has a score of zero.
    """
    response = client.post('/stop', data={'score': '0'})
    assert response.status_code == 200
    assert b"Final Score: 0" in response.data
