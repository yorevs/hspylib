import logging as log
from typing import Optional

from argostranslate import translate, package
from argostranslate.translate import ITranslation
from hspylib.core.metaclass.singleton import Singleton

from askai.lang.language import Language


class MultilingualTranslator(metaclass=Singleton):
    """TODO"""

    INSTANCE = None

    @staticmethod
    def _get_argos_model(source: Language, target: Language) -> Optional[ITranslation]:
        """Retrieve ARGOS model from source to target languages.
        :param source: The source language.
        :param target: The target language.
        """
        lang = f"{source.shortname} -> {target.shortname}"
        log.debug(f"Translating from: {source} to: {target}")
        source_lang = [
            model
            for model in translate.get_installed_languages()
            if lang in map(repr, model.translations_from)
        ]
        target_lang = [
            model
            for model in translate.get_installed_languages()
            if lang in map(repr, model.translations_to)
        ]
        if len(source_lang) <= 0 or len(target_lang) <= 0:
            log.warning("No installed translations found!")
            return None

        return source_lang[0].get_translation(target_lang[0])

    def __init__(self, from_idiom: Language, to_idiom: Language):
        self._from_idiom: Language = from_idiom
        self._to_idiom: Language = to_idiom
        self._argos_model = self._get_argos_model(from_idiom, to_idiom)
        if not self._argos_model:
            self._install_translator()
            self._argos_model = self._get_argos_model(from_idiom, to_idiom)

    def translate(self, text: str) -> str:
        """Translate text using Argos translator.
        :param text: Text to translate.
        """
        return (
            text
            if self._from_idiom == self._to_idiom
            else self._argos_model.translate(text)
        )

    def _install_translator(self) -> bool:
        """Install the Argos translator if it's not yet installed on the system."""
        package.update_package_index()
        required_package = next(
            filter(
                lambda x: x.from_code == self._from_idiom.mnemonic
                and x.to_code == self._to_idiom.mnemonic,
                package.get_available_packages(),
            )
        )
        log.debug("Downloading and installing package %s", required_package)
        package.install_from_path(required_package.download())
        return True
