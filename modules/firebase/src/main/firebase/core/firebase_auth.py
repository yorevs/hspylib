#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   TODO Purpose of the file
   @project: HSPyLib
   @package: hspylib.app.firebase.core
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
from hspylib.core.tools.commons import syserr, sysout
from hspylib.core.tools.preconditions import check_not_none
from requests.structures import CaseInsensitiveDict

from exception.exceptions import FirebaseAuthenticationError, FirebaseException, InvalidFirebaseCredentials


class FirebaseAuth(ABC):
    """Firebase authentication utils
    Ref: https://www.youtube.com/watch?v=esqNgnayVE8
    """

    @classmethod
    def _credentials(cls, config: CaseInsensitiveDict) -> credentials.Certificate:
        """TODO"""
        project_id = config['PROJECT_ID']
        certificate_file = os.environ.get("HOME", '~') + f"/.ssh/{project_id}-firebase-credentials.json"
        check_not_none(config)

        try:
            creds = credentials.Certificate(certificate_file)
        except (IOError, ValueError) as err:
            raise InvalidFirebaseCredentials('Invalid credentials provided') from err

        return creds

    @classmethod
    def authenticate(cls, config: CaseInsensitiveDict) -> Optional[UserRecord]:
        """TODO"""
        firebase_admin.initialize_app(cls._credentials(config))

        try:
            user = auth.get_user(config['UID'])
            if user:
                sysout('Firebase authentication succeeded')
                return user
            else:
                syserr('Failed to authenticate to Firebase')
                return None
        except UserNotFoundError as err:
            raise FirebaseAuthenticationError('Failed to authenticate to Firebase') from err
        except (ValueError, FirebaseError) as err:
            raise FirebaseException('An error occurred authenticating Firebase user') from err

