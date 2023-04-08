import sys

from cvlac.testing.testing_cvlac.testing_cvlac import run_unittests_cvlac
from cvlac.testing.testing_gruplac.testing_gruplac import run_unittests_gruplac
from cvlac.util import get_lxml

sys.path.append(".")

#Ejecutar todas las pruebas de verificación para cvlac y gruplac
print('**************************************')
print('***PRUEBAS DE VERIFICACIÓN DE CVLAC***')
print('**************************************')
run_unittests_cvlac()
print('**************************************')
print('**PRUEBAS DE VERIFICACIÓN DE GRUPLAC**')
print('**************************************')
run_unittests_gruplac()

