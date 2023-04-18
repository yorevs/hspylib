from hspylib.core.enums.charset import Charset
from hqt.views.qt_view import QtView

from %APP_NAME%.__classpath__ import _Classpath


class MainQtView(QtView):
    """Main application view"""
    VERSION = _Classpath.get_source_path(".version").read_text(encoding=Charset.UTF_8.val)

    FORMS_DIR = str(_Classpath.resource_path() / "forms")

    def __init__(self):
        # Must come after the initialization above
        super().__init__(load_dir=self.FORMS_DIR)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI: Connect signals and Setup components"""
        self.window.resize(600, 400)
