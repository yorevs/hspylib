#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-CFMan
   @package: cfman.core
      @file: cf_blue_green_checker.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from cfman.core.cf_application import CFApplication
from clitt.core.term.terminal import Terminal
from typing import Dict, List, Tuple

import re


class CFBlueGreenChecker:
    """Blue/Green deployment checker."""

    @staticmethod
    def _is_green(cf_application: CFApplication) -> bool:
        """TODO"""
        return bool(re.search(r".*-green", cf_application.name))

    @staticmethod
    def _is_blue(cf_application: CFApplication) -> bool:
        """TODO"""
        return bool(re.search(r".*-blue", cf_application.name))

    @staticmethod
    def _check_alerts(active_app: CFApplication, idle_app: CFApplication) -> list:
        """
        :param active_app: The dict representing the CF APP (name | state | processes | routes).
        :return: Any alerts about the active_app.
        """
        alerts = []
        if active_app is None or not active_app.name.endswith(("-green", "-blue")):
            alerts.append("  Status: %ORANGE%Invalid Blue/Green Deploy. Missing active app !")
        elif idle_app is None or not idle_app.name.endswith(("-green", "-blue")):
            alerts.append("  Status: %ORANGE%Invalid Blue/Green Deploy. Missing idle app !")
        elif not active_app.is_started and not idle_app.is_started:
            alerts.append("  Status: %ORANGE%Both blue & green stopped!")
        elif active_app.is_started and len(active_app.routes) < len(idle_app.routes):
            alerts.append("  Status: %ORANGE%Should be stopped!")
        elif not active_app.is_started and len(active_app.routes) > len(idle_app.routes):
            alerts.append("  Status: %ORANGE%Should be started!")
        else:
            alerts.append("  Status: %GREEN%OK")

        return alerts

    @classmethod
    def check(cls, org: str, space: str, apps: List[CFApplication]) -> None:
        mapped_apps = cls._group_apps(apps)
        cls._list_blue_green_pairs(org, space, mapped_apps)

    @classmethod
    def _group_apps(cls, apps: List[CFApplication]) -> dict:
        mapped_apps: Dict[str, Dict[str, CFApplication]] = {}
        green_apps = list(filter(cls._is_green, apps))
        blue_apps = list(filter(cls._is_blue, apps))

        for app_green in green_apps:
            green_info = list(filter(None, re.split(r"\s{2,}", app_green.name)))
            app_name = green_info[0].replace("-green", "")
            mapped_apps[app_name]: dict = (
                mapped_apps[app_name] if app_name in mapped_apps else {"green": None, "blue": None}
            )
            mapped_apps[app_name]["green"] = app_green

        for app_blue in blue_apps:
            blue_info = list(filter(None, re.split(r"\s{2,}", app_blue.name)))
            app_name = blue_info[0].replace("-blue", "")
            mapped_apps[app_name] = mapped_apps[app_name] if app_name in mapped_apps else {"green": None, "blue": None}
            mapped_apps[app_name]["blue"] = app_blue

        return mapped_apps

    @classmethod
    def _list_blue_green_pairs(cls, org: str, space: str, mapped_apps: Dict[str, Dict[str, CFApplication]]) -> None:
        """
        List all apps from current cf space, grouped by blue/green envs.
        :param mapped_apps: The dict containing all CF blue and green apps.
        :return: None
        """
        Terminal.echo(
            f"%BLUE%Listing '{org}::{space}' applications grouped by blue/green pairs ...%EOL%%WHITE%"
            f"{'-=' * 60 + '%EOL%'}"
            f"{'Color':^11}{'Status':<10}{'Instances (MEM)':<27}Routes:{'Alerts':>13}%EOL%"
        )
        for name, app in mapped_apps.items():
            app_green = app["green"]
            app_blue = app["blue"]
            Terminal.echo(f"%CYAN%\\-{name}")
            color, info = cls._match_green(app_green, app_blue)
            Terminal.echo(f"{color} |-GREEN: {info}")
            color, info = cls._match_blue(app_blue, app_green)
            Terminal.echo(f"{color} |-BLUE : {info}")
            Terminal.echo("%NC%%EOL%" + "-" * 120)

    @classmethod
    def _app_info(cls, active_app: CFApplication, idle_app: CFApplication) -> str:
        """
        :param active_app: the active cf application.
        :param idle_app: the inactive cf application.
        :return: Information about the active_app.
        """
        if not (alerts := cls._check_alerts(active_app, idle_app)):
            alerts_str = "  Status: %GREEN%OK%NC%"
        else:
            alerts_str = ",".join(alerts)

        app_routes = len(active_app.routes)

        return (
            f"{active_app.colored_state:<16}  "
            f"{active_app.instances + f' ({active_app.memory})':<25}  "
            f"ROUTES: ({app_routes}) {alerts_str:^2}"
        )

    @classmethod
    def _match_green(cls, app_green: CFApplication, app_blue: CFApplication) -> Tuple[str, str]:
        return (
            "%YELLOW%"
            if app_green is None or app_blue is None or len(app_green.routes) > len(app_blue.routes)
            else "%NC%",
            cls._app_info(app_green, app_blue) if app_green else "%RED%Missing green pair!",
        )

    @classmethod
    def _match_blue(cls, app_blue: CFApplication, app_green: CFApplication) -> Tuple[str, str]:
        return (
            "%YELLOW%"
            if app_green is None or app_blue is None or len(app_blue.routes) > len(app_green.routes)
            else "%NC%",
            cls._app_info(app_blue, app_green) if app_blue else "%RED%Missing blue pair!",
        )
