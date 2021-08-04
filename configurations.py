from configparser import ConfigParser, NoOptionError, NoSectionError
import os

def load_conf(config: ConfigParser, section: str, name: str, default=None) -> str:
    try:
        output = config.get(section, name)
    except (NoOptionError, NoSectionError):
        output = default
    return output

def config() -> None:
    config_parse = ConfigParser()
    config_parse.read("settings.ini")
    DATABASE = "DATABASE"
    SYSTEM = "SYSTEM"
    BOT = "BOT"

    #DATABASE
    os.environ.setdefault("DATABASE_NAME", load_conf(config_parse, DATABASE, "NAME", "pokemon"))
    os.environ.setdefault("DATABASE_USER", load_conf(config_parse, DATABASE, "USER", "user"))
    os.environ.setdefault("DATABASE_PASSW", load_conf(config_parse, DATABASE, "PASSWORD", "root"))
    os.environ.setdefault("DATABASE_HOST", load_conf(config_parse, DATABASE, "HOST", "localhost"))
    os.environ.setdefault("DATABASE_PORT", load_conf(config_parse, DATABASE, "PORT", "5432"))

    #SYSTEM
    os.environ.setdefault("DJANGO_DEBUG", load_conf(config_parse, SYSTEM, "DEBUG", "false"))
    os.environ.setdefault("DJANGO_KEY", load_conf(config_parse, SYSTEM, "DJANGO_KEY", "root"))

    #BOT
    os.environ.setdefault("TOKEN", load_conf(config_parse, BOT, "BOT_TOKEN", None))
    os.environ.setdefault("TG_NAME", load_conf(config_parse, BOT, "APP_NAME", "root"))
