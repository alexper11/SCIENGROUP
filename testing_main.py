from cvlac.testing import testing
from cvlac.util import get_lxml
import sys
sys.path.append(".")

prueba=testing.prueba_unitaria()
print(prueba.test_dfs(testing.df_auto1,testing.df_manu1))
print(prueba.test_dfs(testing.df_auto2,testing.df_manu2))
print(prueba.test_dfs(testing.df_auto3,testing.df_manu3))