"""
Test fixtures for simulating JSON input from Alexa
"""
import os
import io
import six

requests_dir = os.path.realpath(os.path.join(os.path.realpath(__file__),
                                             '../fixtures/'))


def _read_request_json(filename):
    with open(requests_dir + '/' + filename, 'r') as f:
        body = f.read()
        return io.StringIO(six.u(body))


def launch():
    return _read_request_json('launch.json')


def list_programs():
    return _read_request_json('list_programs.json')


def play_program(program='totally not a program'):
    json = _read_request_json('play_program.json').read()
    return io.StringIO(json.replace('{{VALUE}}', program))


def cancel():
    return _read_request_json('cancel.json')


def help():
    return _read_request_json('help.json')


def say_nothing():
    return _read_request_json('say_nothing.json')


def playback_started(token):
    json = _read_request_json('playback_started.json').read()
    return io.StringIO(json.replace('{{TOKEN}}', token))

