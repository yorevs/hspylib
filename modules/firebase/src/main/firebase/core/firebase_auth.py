#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HSPyLib-Firebase
   @package: firebase.core
      @file: firebase_auth.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2022, HSPyLib team
"""
import os
from abc import ABC
from typing import Optional

import firebase_admin
from firebase_admin import auth, credentials
from firebase_admin.auth import UserNotFoundError, UserRecord
from firebase_admin.exceptions import FirebaseError
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import sysout

from firebase.exception.exceptions import FirebaseAuthenticationError, FirebaseException, InvalidFirebaseCredentials


class FirebaseAuth(ABC):
    """Firebase authentication utils
    Ref: https://www.youtube.com/watch?v=esqNgnayVE8
    """

    @staticmethod
    def _credentials(project_id: str) -> credentials.Certificate:
        """TODO"""

        certificate_file = os.environ.get(
            "HHS_FIREBASE_CERT_FILE", f"{os.environ.get('HOME')}/firebase-credentials.json")
        check_not_none(certificate_file, project_id)
        try:
            creds = credentials.Certificate(certificate_file.format(project_id=project_id))
        except (IOError, ValueError) as err:
            raise InvalidFirebaseCredentials("Invalid credentials provided") from err

        return creds

    @staticmethod
    def authenticate(project_id: str, uuid: str) -> Optional[UserRecord]:
        """TODO"""

        firebase_admin.initialize_app(FirebaseAuth._credentials(project_id))
        try:
            user = auth.get_user(uuid)
            if user:
                sysout("%ORANGE%Firebase authentication succeeded%EOL%")
                return user
            raise FirebaseAuthenticationError("Failed to authenticate to Firebase")
        except UserNotFoundError as err:
            raise FirebaseAuthenticationError(f"Failed to authenticate to Firebase => {err}") from err
        except (ValueError, FirebaseError) as err:
            raise FirebaseException(f"An error occurred authenticating Firebase user => {err}") from err
