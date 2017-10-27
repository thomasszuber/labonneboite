import sys
from labonneboite.importer import util as import_util


if __name__ == "__main__":
    filename = import_util.detect_runnable_file("etablissements")
    if filename:
        with open(import_util.JENKINS_ETAB_PROPERTIES_FILENAME, "w") as f:
            f.write("LBB_ETABLISSEMENT_INPUT_FILE=%s\n" % filename)
        sys.exit(0)
    else:
        sys.exit(-1)
