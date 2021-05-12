from versioner.src.main.core.versioner import Versioner
from versioner.src.main.entity.version import Version

if __name__ == '__main__':
    v = Version.of('0.9.0-SNAPSHOT')
    vr = Versioner()
    vr.patch(v), '-> Patch'
    vr.minor(v), '-> Minor'
    vr.major(v), '-> Major'
    vr.promote(v)
    vr.promote(v)
    vr.demote(v)
    vr.demote(v)
