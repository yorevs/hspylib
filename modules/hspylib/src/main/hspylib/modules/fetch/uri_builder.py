#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: hspylib
   @package: hspylib.modules.fetch
      @file: uri_builder.py
   @created: Mon, 12 Dec 2022
    @author: "<B>H</B>ugo <B>S</B>aporetti <B>J</B>unior")"
      @site: "https://github.com/yorevs/hspylib")
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""

from collections import namedtuple
from hspylib.modules.fetch.uri_scheme import UriScheme
from typing import Any, Dict, List
from urllib.parse import parse_qs, SplitResult, urlencode, urlsplit, urlunparse

URI = namedtuple(typename="URI", field_names=["scheme", "netloc", "url", "path", "query", "fragment"])


class UriBuilder:
    """URI template-aware utility class for building URIs from their components.
        uri: <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
     netloc: [username[:<password>]@]<domain>[:<port>]

    Breaking this format down syntactically:

      scheme: The protocol name, usually http/https
      netloc: Contains the network location - which includes the domain itself (and subdomain if present),
              the port number, along with an optional credentials in form of username:password. Together it
              may take form of username:password@example.com:80.
        path: Contains information on how the specified resource needs to be accessed.
      params: Element which adds fine tuning to path. (optional)
       query: Another element adding fine grained access to the path in consideration. (optional)
    fragment: Contains bits of information of the resource being accessed within the path. (optional)
    """

    @classmethod
    def ensure_scheme(cls, url_string: str, scheme: str | UriScheme = UriScheme.HTTP) -> str:
        """Ensure the URL string contains the URI Scheme."""
        if not url_string.startswith(tuple(UriScheme.values())):
            url_string = f"{scheme if isinstance(scheme, str) else str(scheme)}://{url_string}"
        return url_string

    @classmethod
    def parse(cls, url_string: str) -> "UriBuilder":
        """Parse a URL string into a URI builder."""
        uri_parts: SplitResult = urlsplit(cls.ensure_scheme(url_string))
        return (
            UriBuilder()
            .scheme(uri_parts.scheme or UriScheme.HTTP)
            .hostname(uri_parts.hostname)
            .port(uri_parts.port)
            .query({k: v[0] for k, v in parse_qs(uri_parts.query).items()})
            .user_info(uri_parts.username, uri_parts.password)
            .add_path(uri_parts.path.split("/"))
            .fragment(uri_parts.fragment)
        )

    def __init__(self) -> None:
        self._scheme: UriScheme = UriScheme.HTTP
        self._host: str = "localhost"
        self._port: int = 8080
        self._username: str = ""
        self._password: str = ""
        self._path: List[str] = []
        self._query: Dict[str, Any] = {}
        self._fragment: str = ""

    def __str__(self) -> str:
        return str(self.get_uri())

    def __repr__(self) -> str:
        return str(self)

    def scheme(self, scheme: str | UriScheme) -> "UriBuilder":
        """Set the URI scheme."""
        self._scheme = scheme if isinstance(scheme, UriScheme) else UriScheme.of(scheme)
        return self

    def hostname(self, host: str) -> "UriBuilder":
        """Set the URI host."""
        self._host = host
        return self

    def port(self, port: int) -> "UriBuilder":
        """Set the URI port."""
        self._port = port
        return self

    def user_info(self, username: str, password: str | None = None) -> "UriBuilder":
        """Set the URI user-info."""
        if username:
            self._username = username
            self._password = password
        return self

    def add_path(self, path: str | List[str]) -> "UriBuilder":
        """Add paths to the existing URI."""
        self._path.extend(path if isinstance(path, List) else [path])
        return self

    def path(self, path: str) -> "UriBuilder":
        """Set the URI path."""
        self._path = [path]
        return self

    def add_query(self, key: str, value: Any) -> "UriBuilder":
        """Add query to the existing URI."""
        self._query.update({key: value})
        return self

    def query(self, query: Dict[str, Any]) -> "UriBuilder":
        """Set the URI query."""
        self._query = query
        return self

    def fragment(self, fragment: str) -> "UriBuilder":
        """Set the URI fragment."""
        self._fragment = fragment
        return self

    def build(self) -> str:
        """Build a URI using the supplied attributes."""
        return urlunparse(self.get_uri())

    def get_uri(self) -> URI:
        """Return a URI object using the supplied attributes."""
        return URI(
            scheme=str(self._scheme),
            netloc=self.get_netloc(),
            url="/".join(self._path),
            query=urlencode(self._query),
            path="",
            fragment=self._fragment,
        )

    def get_netloc(self) -> str:
        """Return the network location on the form:
        [username[:<password>]@]<domain>[:<port>]
        """
        return (
            f"{self._username}{':' + self._password if self._password else ''}"
            f"{'@' if self._username else ''}"
            f"{self._host}{':' + str(self._port) if self._port else ''}"
        )
