# flake8: noqa
import os

import pytest
import yaml

from little_conf import LittleConfig

BASE_FILE_PATH = 'tests/conf/base.yaml'


@pytest.fixture(autouse=True)
def set_up_tear_down():

    yield

    os.environ.pop('service_yaml_conf_path', None)
    os.environ.pop('service_env', None)


def test_1():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            env = 'local'
            yaml_conf_path = 'tests/conf'
            env_prefix = 'my2_'

    assert Settings().dict() == {'var2': '123'}


def test_11():
    class Settings(LittleConfig):
        var2: str = '1'
        var3: int = 444

        class Config:
            env = 'local'
            yaml_conf_path = 'tests/conf'
            env_prefix = 'my2_'

    assert Settings().dict() == {'var2': '123', 'var3': 444}


def test_empty_conf():
    class Settings(LittleConfig):
        var2: str = '1'
        var3: int = 444

        class Config:
            env = 'empty'
            yaml_conf_path = 'tests/conf'
            env_prefix = 'my2_'

    assert Settings().dict() == {'var2': '1', 'var3': 444}


def test_empty_conf_set_by_env():
    class Settings(LittleConfig):
        var2: str = '1'
        var3: int = 444

    os.environ['service_yaml_conf_path'] = 'tests/conf'
    os.environ['service_env'] = 'empty'

    assert Settings().dict() == {'var2': '1', 'var3': 444}


def test_bad_file():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            yaml_conf_path = '/ttt'

    with pytest.raises(FileNotFoundError):
        Settings()


def test_no_file():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            yaml_conf_path = None

    assert Settings().dict() == {'var2': '1'}


def test_reload_by_env():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            yaml_conf_path = 'tests/conf'

    os.environ['service_var2'] = '2'
    assert Settings().dict() == {'var2': '2'}


def test_reload_by_env2():
    class Settings(LittleConfig):
        var2: int = 1

        class Config:
            env_prefix = 'my_'
            yaml_conf_path = 'tests/conf'

    os.environ['my_var2'] = '2'
    assert Settings().dict() == {'var2': 2}


def test_with_base():
    class Settings(LittleConfig):
        var2: str = '1'
        var3: int = 1

        class Config:
            env = 'local'
            yaml_conf_path = 'tests/conf'
            env_prefix = 'my2_'

    base_conf = {'var3': 123}
    with open(BASE_FILE_PATH, 'w') as fp:
        yaml.dump(base_conf, fp)

    assert Settings().dict() == {'var2': '123', 'var3': 123}

    os.unlink(BASE_FILE_PATH)


def test_is_env_local_default():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            yaml_conf_path = 'tests/conf'

    assert Settings().is_env_local == True


def test_is_env_local():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            env = 'local'
            yaml_conf_path = 'tests/conf'

    assert Settings().is_env_local == True


def test_is_env_local_false():
    class Settings(LittleConfig):
        var2: str = '1'

        class Config:
            env = 'empty'
            yaml_conf_path = 'tests/conf'

    assert Settings().is_env_local == False
