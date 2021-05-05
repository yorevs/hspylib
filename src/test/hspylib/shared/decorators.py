import os
import unittest

from hspylib.core.tools.commons import str_to_bool

it_disabled = str_to_bool(os.environ.get('HSPYLIB_IT_DISABLED', 'True'))

integration_test = unittest.skipIf(
    it_disabled,
    f'Disabled = {it_disabled} :integration tests because it needs docker container running'
)
