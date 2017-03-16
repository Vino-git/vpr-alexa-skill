"""
Tests for VPR's Amazon Alexa Skill
"""
from vpr_alexa.webapp import create_app
import tests.requests as requests
import pytest
import json

app = create_app()
app.config['ASK_VERIFY_REQUESTS'] = False
app.config['TESTING'] = True


@pytest.fixture(name='client')
def setup_client():
    return app.test_client()


def post(flask_client, request):
    response = flask_client.post('/ask', data=request)
    assert response.status_code == 200
    return json.loads(response.data.decode('utf-8'))


def test_welcome(client):
    response = post(client, requests.launch())

    assert response['response']['shouldEndSession'] is False
    assert 'Welcome to Vermont Public Radio' \
           in response['response']['outputSpeech']['text']
    assert 'You can say ' \
           in response['response']['reprompt']['outputSpeech']['text']
    assert 'Play the latest Vermont Edition or List Programs' \
           in response['response']['reprompt']['outputSpeech']['text']


def test_program_list(client):
    response = post(client, requests.list_programs())

    assert response['response']['shouldEndSession'] is False
    assert 'You can listen to the following programs' \
           in response['response']['outputSpeech']['text']
    assert 'Which would you like to listen to? ' \
           'You can say the name of the program or cancel.'\
           in response['response']['outputSpeech']['text']


def test_play_program(client):
    response = post(client, requests.play_program('vermont edition'))

    assert 'Playing Vermont Edition' \
           in response['response']['outputSpeech']['text']
    assert 'AudioPlayer.Play' in response['response']['directives'][0]['type']


def test_request_bad_program(client):
    response = post(client, requests.play_program())

    assert 'Sorry' in response['response']['outputSpeech']['text']
