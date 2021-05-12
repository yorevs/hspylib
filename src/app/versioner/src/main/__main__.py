import sys

from versioner.src.main.core.versioner import Versioner

if __name__ == '__main__':
    files = sys.argv[1:]
    v = Versioner('0.10.4', '/Users/hugo/GIT-Repository/GitHub/Python/hspylib', files)
    v.patch()
    v.save()
    print(v.version)
