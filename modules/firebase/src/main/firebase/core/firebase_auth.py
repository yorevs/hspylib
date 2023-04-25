#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
   @project: HsPyLib-Firebase
   @package: firebase.core
      @file: firebase_auth.py
   @created: Tue, 4 May 2021
    @author: <B>H</B>ugo <B>S</B>aporetti <B>J</B>unior"
      @site: https://github.com/yorevs/hspylib
   @license: MIT - Please refer to <https://opensource.org/licenses/MIT>

   Copyright 2023, HsPyLib team
"""
from abc import ABC
from firebase.exception.exceptions import FirebaseAuthenticationError, FirebaseException, InvalidFirebaseCredentials
from firebase_admin import auth, credentials
from firebase_admin.auth import UserNotFoundError, UserRecord
from firebase_admin.exceptions import FirebaseError
from hspylib.core.preconditions import check_not_none
from hspylib.core.tools.commons import sysout
from typing import Optional

import firebase_admin
import os


class FirebaseAuth(ABC):
    """Firebase authentication utils
    Ref: https://www.youtube.com/watch?v=esqNgnayVE8
    """

    @staticmethod
    def _credentials(project_id: str) -> credentials.Certificate:
        """Create Firebase credentials based on the configured credentials file.
        :param project_id: the Firebase Realtime database project ID.
        """

        creds_file = os.environ.get("HHS_FIREBASE_CREDS_FILE", f"{os.environ.get('HOME')}/firebase-credentials.json")
        check_not_none(creds_file, project_id)
        try:
            creds = credentials.Certificate(creds_file.format(project_id=project_id))
        except (IOError, KeyError, ValueError) as err:
            raise InvalidFirebaseCredentials(f'Invalid credentials or credential file "{creds_file}"') from err

        return creds

    @staticmethod
    def authenticate(project_id: str, uid: str) -> Optional[UserRecord]:
        """Authenticate to Firebase using valid credentials.
        :param project_id: the Firebase Realtime database project ID.
        :param uid: the Firebase User ID.
        """
        sysout("%BLUE%Authenticating to Firebase ...%NC%")
        firebase_admin.initialize_app(FirebaseAuth._credentials(project_id))
        try:
            if user := auth.get_user(uid):
                sysout("%GREEN%Firebase authentication succeeded!")
                return user
            raise FirebaseAuthenticationError(f'Failed to authenticate to Firebase. User ID "{uid}" not found.')
        except UserNotFoundError as err:
            raise FirebaseAuthenticationError(f"Failed to authenticate to Firebase => {err}") from err
        except (ValueError, FirebaseError) as err:
            raise FirebaseException(f"An error occurred authenticating Firebase user => {err}") from err
