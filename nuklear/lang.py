import os
from pathlib import Path

import i18n
from babel import Locale

LANGS_PATH = Path.cwd() / 'locale'

i18n.load_path.append(str(LANGS_PATH.resolve()))
locale = Locale.parse(os.environ.get('LANG', 'en_US'))
i18n.set('locale', locale.language)
