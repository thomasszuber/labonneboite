import sys
from labonneboite.importer import settings
from labonneboite.common.env import get_current_env, ENV_LBBDEV

def get_dpae_filename():
    with open(settings.JENKINS_DPAE_PROPERTIES_FILENAME, "r") as f:
        dpae_filename = f.read().strip().split('=')[1]
    return dpae_filename

def get_etablissement_filename():
    with open(settings.JENKINS_ETAB_PROPERTIES_FILENAME, "r") as f:
        # file content looks like this:
        # LBB_ETABLISSEMENT_INPUT_FILE=/srv/lbb/labonneboite/importer/data/LBB_ETABLISSEMENT_2016-12-19_2015-11-19.bz2\n
        etablissement_filename = f.read().strip().split('=')[1]
    return etablissement_filename
