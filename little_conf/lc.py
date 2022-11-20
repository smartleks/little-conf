import functools
import os
import signal
from typing import Any, Dict, Optional

import yaml
from deepmerge import always_merger
from pydantic import BaseSettings, PrivateAttr

SERVICE_ENV_PREFIX = 'env_prefix'


def yaml_config_settings_source(
    settings: BaseSettings, base_path: str, env: str, ret_conf: dict
) -> dict[str, Any]:

    if base_path is not None:
        if ret_conf is None:
            ret_conf = {}
            base_conf = {}
            base_conf_file = os.path.join(base_path, 'base.yaml')
            if os.path.exists(base_conf_file):
                with open(base_conf_file, 'r') as fp:
                    base_conf = yaml.safe_load(fp) or {}

            ret = {}
            if env is not None:
                with open(os.path.join(base_path, f'{env}.yaml'), 'r') as fp:
                    ret = yaml.safe_load(fp) or {}

            ret_conf = always_merger.merge(base_conf, ret)

        return ret_conf
    else:
        return {}


class LittleConfig(BaseSettings):
    _hook_on_reconfig = PrivateAttr()
    _reinit = PrivateAttr()
    _old_sig_handler = PrivateAttr()

    def __init__(self, *args, on_init=None, **kwargs):
        super().__init__(*args, **kwargs)

        self._reinit = functools.partial(
            self.__init__, *args, on_init=on_init, **kwargs
        )
        self._hook_on_reconfig = lambda x: None

        self._old_sig_handler = signal.getsignal(signal.SIGHUP)
        signal.signal(signal.SIGHUP, self.signal_handler)

        if on_init is not None:
            on_init(self)

    @property
    def is_env_local(self):
        return self.__config__.env == 'local'

    def on_reconfig(self, func):
        self._hook_on_reconfig = func

    def reload(self):
        on_reconf = self._hook_on_reconfig
        self._reinit()

        self.on_reconfig(on_reconf)
        self._hook_on_reconfig(self)

    def signal_handler(self, signum: Any, frame: Any) -> None:
        try:
            signal.signal(signum, signal.SIG_IGN)  # ignore additional signals
            self.reload()
        finally:
            signal.signal(signum, self.signal_handler)

    class Config:
        env_prefix = os.environ.get(SERVICE_ENV_PREFIX, 'service_')
        yaml_conf_path = os.environ.get(env_prefix + 'yaml_conf_path', 'config')
        env = os.environ.get(env_prefix + 'env', 'local')

        _ret_conf: Optional[Dict[str, Any]] = None

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):

            env_prefix = os.environ.get(SERVICE_ENV_PREFIX, cls.env_prefix)
            env = os.environ.get(env_prefix + 'env', cls.env)
            yaml_conf_path = os.environ.get(
                env_prefix + 'yaml_conf_path', cls.yaml_conf_path
            )

            return (
                init_settings,
                env_settings,
                functools.partial(
                    yaml_config_settings_source,
                    base_path=yaml_conf_path,
                    env=env,
                    ret_conf=cls._ret_conf,
                ),
                file_secret_settings,
            )
