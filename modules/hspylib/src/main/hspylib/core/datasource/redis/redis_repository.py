#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib
   @Package: main.hspylib.core.datasource.postgres
      @file: postgres_repository.py
   @created: Sat, 12 Nov 2022
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import contextlib
import logging as log
from abc import abstractmethod
from typing import Generic, List, Optional, Tuple, TypeVar

import redis
from redis.client import Pipeline
from retry import retry

from hspylib.core.datasource.crud_entity import CrudEntity
from hspylib.core.datasource.db_repository import Connection, Cursor
from hspylib.core.datasource.redis.redis_configuration import RedisConfiguration
from hspylib.core.enums.charset import Charset
from hspylib.core.exception.exceptions import DatabaseConnectionError, DatabaseError
from hspylib.core.preconditions import check_not_none

T = TypeVar('T', bound=CrudEntity)


class RedisRepository(Generic[T]):
    """Implementation of a data access layer for a postgres persistence store.
    Ref.: https://github.com/redis/redis-py
    Ref.: https://docs.redis.com/latest/rs/references/client_references/client_python/
    """

    def __init__(self, config: RedisConfiguration):
        self._config = config

    def __str__(self):
        return f"{self.hostname}:{self.port}/{self.database}"

    def __repr__(self):
        return str(self)

    @property
    def logname(self) -> str:
        """TODO"""
        return self.__class__.__name__.split('_')[0]

    @property
    def hostname(self) -> str:
        return self._config.hostname

    @property
    def port(self) -> int:
        return self._config.port

    @property
    def database(self) -> str:
        return self._config.database

    @property
    def password(self) -> str:
        return self._config.password

    @property
    def ssl(self) -> bool:
        return self._config.ssl

    @retry(tries=3, delay=2, backoff=3, max_delay=30)
    def _create_session(self) -> Tuple[Connection, Cursor]:
        """TODO"""
        log.debug(f"{self.logname} Attempt to connect to database: {str(self)}")
        conn = redis.Redis(
            ssl=self.ssl,
            host=self.hostname,
            port=self.port,
            password=self.password)
        log.debug(f"{self.logname} Connection info: {conn.config_get('databases')}")
        return conn, conn.pipeline()

    @contextlib.contextmanager
    def pipeline(self) -> Pipeline:
        """TODO"""
        conn, pipe = None, None
        try:
            conn, pipe = self._create_session()
            log.debug(f"{self.logname} Successfully connected to database: {str(self)} [ssid={hash(pipe)}]")
            yield pipe
        except redis.exceptions.ConnectionError as err:
            raise DatabaseConnectionError(f"Unable to open/execute-on database session => {err}") from err
        except redis.exceptions.ResponseError as err:
            log.error(f"{self.logname} Pipeline failed with: {err}")
        except Exception as err:
            raise DatabaseError(f"{self.logname} Unable to execute pipeline -> {err}") from err
        finally:
            if pipe:
                pipe.close()

    def delete(self, *keys: str) -> int:
        """TODO"""
        check_not_none(keys)
        with self.pipeline() as pipe:
            pipe.delete(*keys)
            ret_val = pipe.execute() or []
            log.debug(f"{self.logname} "
                      f"Executed a pipelined 'DEL' command and returned: {ret_val}")
            return ret_val[0] or 0

    def get(self, *keys: str) -> List[T]:
        """TODO"""
        check_not_none(keys)
        with self.pipeline() as pipe:
            result = []
            pipe.mget(keys)
            count = len(pipe)
            ret_val = list(filter(None, pipe.execute()))
            if ret_val:
                list(map(lambda e: result.append(self.to_entity_type(e)), ret_val[0]))
            log.debug(f"{self.logname} "
                      f"Executed '{count}' pipelined 'GET' command(s) and returned {len(result)} entries")
            return result

    def get_one(self, key: str) -> Optional[T]:
        """TODO"""
        check_not_none(key)
        with self.pipeline() as pipe:
            pipe.get(key)
            ret_val = list(filter(None, pipe.execute()))
            log.debug(f"{self.logname} "
                      f"Executed a pipelined 'GET' command and returned: {ret_val}")
            return self.to_entity_type(ret_val[0]) if ret_val else None

    def set(self, *entities: T) -> None:
        """TODO"""
        check_not_none(entities)
        with self.pipeline() as pipe:
            list(map(lambda e: pipe.set(self.build_key(e), str(e.as_dict())), entities))
            count = len(pipe)
            pipe.execute()
            log.debug(f"{self.logname} "
                      f"Executed '{count}' pipelined 'SET' command(s)")

    def flush_all(self) -> None:
        """TODO"""
        with self.pipeline() as pipe:
            pipe.flushall()
            pipe.execute()
            log.debug(f"{self.logname} "
                      f"Executed a FLUSHALL command")

    def keys(self, pattern: str) -> List[str]:
        """TODO"""
        with self.pipeline() as pipe:
            pipe.keys(pattern)
            ret_val = list(filter(None, pipe.execute()))
            result = list(map(lambda k: str(k, Charset.UTF_8.value), ret_val[0])) if ret_val else []
            log.debug(f"{self.logname} "
                      f"Executed a KEYS command and returned: {len(ret_val)} entries")
            return result

    @abstractmethod
    def build_key(self, entity: T) -> str:
        """TODO"""

    @abstractmethod
    def to_entity_type(self, entity_string: bytes) -> T:
        """TODO"""
