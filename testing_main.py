import sys

from cvlac.testing.testing_cvlac.testing_cvlac import run_unittests_cvlac
from cvlac.testing.testing_gruplac.testing_gruplac import run_unittests_gruplac
from cvlac.util import get_lxml

sys.path.append(".")

#run_unittests_cvlac()
run_unittests_gruplac()

