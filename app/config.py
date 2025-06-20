"""
Check this
* "https://rednafi.com/python/config_management_with_pydantic/"
* "https://rednafi.com/python/patch_pydantic_settings_in_pytest/"
"""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    """
    Here are the environment variables that are common to all environments.
    """

    # Put the `ENV_STATE` variable in your .env file to set the environment.
    ENV_STATE: str | None = None  # 'dev', 'test', 'prod'

    TIMEZONE: str = "Asia/Taipei"

    # Check if .env file exists, if not, get the settings from the environment variables.
    _env_file: str | None = ".env" if os.path.exists(".env") else None

    # Loads the dotenv file. Including this is necessary to get pydantic to load a .env file.
    model_config = SettingsConfigDict(env_file=_env_file, extra="ignore")


class GlobalConfig(BaseConfig):
    """
    Here are the environment variables that need to be prefixed either with 'DEV_', 'TEST_', or 'PROD_'.
    """


class DevConfig(GlobalConfig):
    """
    development environment variables, each developer should have their own development settings.
    """

    model_config = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    """
    test environment variables, used for running unit tests.
    """

    model_config = SettingsConfigDict(env_prefix="TEST_")


class ProdConfig(GlobalConfig):
    """
    production environment variables
    """

    model_config = SettingsConfigDict(env_prefix="PROD_")


@lru_cache()
def get_config(env_state: str) -> BaseConfig:
    """
    Instantiate config based on the environment.

    :param env_state: 'dev', 'test' or 'prod'
    :return: BaseConfig object
    :raises ValueError: if env_state is not 'dev', 'test', or 'prod'
    """
    configs = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
    if env_state not in configs:
        raise ValueError(f"Invalid env_state: {env_state}. Expected one of: 'dev', 'test', 'prod'.")

    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
