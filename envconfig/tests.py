import envconfig
import os
import pytest


@pytest.fixture()
def env():
    envconfig.reset()


def test_parse(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        type=envconfig.types.int,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = '200'
    errors, settings = envconfig.parse()
    assert len(errors) == 0
    assert settings['foo']['bar'] == 200


def test_parse_error(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        type=envconfig.types.int,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = 'hello'
    errors, settings = envconfig.parse()
    assert len(errors) == 1
    assert 'foo' not in settings


def test_parse_json(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        type=envconfig.types.json,
        destination='foo.bar')
    os.environ['MY_CONFIGURATION'] = '{"foo": "bar"}'
    errors, settings = envconfig.parse()
    assert len(errors) == 0
    assert settings['foo']['bar']['foo'] == 'bar'


def test_list_append_addressing(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        destination='foo.bar[]')
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = envconfig.parse()
    assert len(errors) == 0
    assert len(settings['foo']['bar']) == 1
    assert settings['foo']['bar'][0] == 'foobar'


def test_list_value_assignment_list(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        destination='foo.bar[0].foo.bar')
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = envconfig.parse()
    assert len(errors) == 0
    assert len(settings['foo']['bar']) == 1
    assert settings['foo']['bar'][0]['foo']['bar'] == 'foobar'


def test_when_exists(env):
    envconfig.register(
        name='MY_CONFIGURATION',
        destination='foo',
        type=envconfig.types.when_exists({'foo': 'bar'}))
    envconfig.register(
        name='MY_CONFIGURATION_MISSING',
        destination='bar',
        type=envconfig.types.when_exists({'foo': 'bar'}))
    os.environ['MY_CONFIGURATION'] = 'foobar'
    errors, settings = envconfig.parse()
    assert len(errors) == 0
    assert settings['foo'] == {'foo': 'bar'}
    assert 'bar' not in settings


def test_format_options(env):
    envconfig.register(
        name='MY_CONFIGURATION_1',
        destination='foo')
    envconfig.register(
        name='MY_CONFIGURATION_2',
        destination='bar',
        type=envconfig.types.when_exists({'foo': 'bar'}))

    formatting = envconfig.format_options()
    assert "<when_exists: {'foo': 'bar'}>" in formatting
