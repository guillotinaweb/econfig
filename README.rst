Env Config
==========

Python package to manage configuration from environment variables.

This package is designed to be used to help in configuration management with
python docker containers.


Defining configuration
----------------------

envconfig provides simple data types to define configuration with::

    import envconfig
    envconfig.register(
      name='MY_CONFIGURATION_NUMBER',
      type=envconfig.types.int,
      destination='foo.bar')
    envconfig.register(
        name='MY_CONFIGURATION_NUMBER',
        type=envconfig.types.json,
        destination='foo.json')
    errors, settings = envconfig.parse()
    settings == {
      "foo": {
        "bar": 5
      },
      "json": {
        "some": "value"
      }
    }


Types
-----

- int
- float
- bool
- exists
- json
- when_exists: callable type that will provide value when env variable exists


Destination types
-----------------

- `foo.bar`: automatic key value dictionary creation
- `foo[]`: append value to list
- `foo[0]`: address item in list
- `foo[0].bar`: address dictionary item in list
