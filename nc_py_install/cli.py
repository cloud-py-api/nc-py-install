"""CLI interface for usage."""

import logging
import platform
import sys
from typing import List, Optional
from argparse import ArgumentParser
from getpass import getuser
from json import dumps as to_json
from urllib.parse import unquote_plus

from .api import OPTIONS, update_pip_info, update_pip, get_userbase_for_app, pckg_check, pckg_install, pckg_delete


LOGS_CONTAINER = []
Log = logging.getLogger("pyfrm.install")
Log.propagate = False
logging.addLevelName(30, "WARN")
logging.addLevelName(50, "FATAL")


class InstallLogHandler(logging.Handler):
    """Used when calling this package as a script."""

    __log_levels = {"DEBUG": 0, "INFO": 1, "WARN": 2, "ERROR": 3, "FATAL": 4}

    def emit(self, record):
        self.format(record)
        __content = (
            record.message if record.funcName == "<module>" else record.funcName + ": " + record.message
        )
        if record.exc_text is not None:
            __content += "\n" + record.exc_text
        __log_lvl = self.__log_levels.get(record.levelname)
        __module = record.module if record.name == "root" else record.name
        if OPTIONS.dev:
            LOGS_CONTAINER.append(
                {
                    "log_lvl": record.levelname,
                    "module": f"{record.filename}:{record.lineno}",
                    "content": __content,
                }
            )
        else:
            LOGS_CONTAINER.append({"log_lvl": __log_lvl, "module": __module, "content": __content})


def main(args: Optional[List[str]] = None):
    parser = ArgumentParser(
        description="Module for checking/installing packages for NC Python Framework.", add_help=True
    )
    parser.add_argument(
        "--appdata",
        dest="appdata",
        type=str,
        help="Path to framework app data folder in quoted format. Use `urllib.parse.quote_plus`",
        required=True,
    )
    parser.add_argument(
        "--appname",
        dest="appname",
        type=str,
        help=(
            "App name if `requirements` will be installed for it"
            "(app folder will be created in `appdata` if it is not exist),"
            " or if omitted they will be installed in root framework folder."
        ),
        default="",
    )
    parser.add_argument(
        "--target",
        dest="target",
        type=str,
        help="`nc_py_frm`, or any other python package name. Can be `-r abs(file) for installing from file.",
        required=True,
    )
    parser.add_argument(
        "--loglvl", dest="loglvl", type=str, help="One of: DEBUG,INFO,WARN,ERROR", default="INFO"
    )
    parser.add_argument("--dev", dest="dev", action="store_true", default=False)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--check", dest="check", action="store_true", help="Get installation info of specified target."
    )
    group.add_argument(
        "--install",
        dest="install",
        action="store_true",
        help="Perform installation of specified target's package(s).",
    )
    group.add_argument(
        "--update",
        dest="update",
        action="store_true",
        help="Perform update of specified target's package(s).",
    )
    group.add_argument(
        "--delete",
        dest="delete",
        action="store_true",
        help="Perform delete of specified target's package(s).",
    )
    args = parser.parse_args(args)
    OPTIONS.dev = args.dev
    args.target = str(args.target).lower()
    OPTIONS.app_data = unquote_plus(args.appdata)
    Log.setLevel(level=args.loglvl)
    Log.addHandler(InstallLogHandler())
    exit_code = 0
    result = False
    r_ok = []
    r_not_ok = []
    r_not_ok_opt = []
    try:
        print_debug_info(args.target)
        update_pip_info()
        Log.info("Python: %s : %s", sys.executable, sys.version)
        Log.info("Pip version: %s, local: %r", OPTIONS.pip_version, OPTIONS.pip_local)
        if args.install:
            result = pckg_install(args.target, get_userbase_for_app(args.appname))
        elif args.update:
            if update_pip():
                result = pckg_install(args.target, get_userbase_for_app(args.appname), ["--upgrade"])
        elif args.delete:
            result = pckg_delete(args.target, get_userbase_for_app(args.appname))
        r_ok, r_not_ok, r_not_ok_opt = pckg_check(args.target, get_userbase_for_app(args.appname))
        if args.check and not r_not_ok:
            result = True
        if not result:
            exit_code = 1
    except Exception as exception_info:  # pylint: disable=broad-except
        Log.exception("Exception: %s", type(exception_info).__name__)
        exit_code = 2
    result = {
        "Logs": LOGS_CONTAINER,
        "Installed": r_ok,
        "NotInstalled": r_not_ok,
        "NotInstalledOpt": r_not_ok_opt,
        "Result": result,
    }
    if OPTIONS.dev:
        result.pop("Logs")
        for log_record in LOGS_CONTAINER:
            print(log_record["log_lvl"] + " : " + log_record["module"] + " : " + log_record["content"])
    print(to_json(result, indent=4 if OPTIONS.dev else None))
    return exit_code


def print_debug_info(target: str) -> None:
    try:
        Log.debug("User name: %s", getuser())
    except (AttributeError, ImportError, OSError) as _exception:
        Log.warning("Exception during `getuser`: %s", str(_exception))
    Log.debug("target: %s", target)
    Log.debug("Platform: %s", platform.platform())
    Log.debug("app_data: %s", OPTIONS.app_data)
    Log.debug("core_userbase: %s", OPTIONS.core_userbase)
