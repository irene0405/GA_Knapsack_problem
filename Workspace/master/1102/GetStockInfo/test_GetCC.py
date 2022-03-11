import numpy as np
import pandas as pd

a = pd.Series([2.0, 4.0, 3.0, 5.0, 4.0, 6.0])
b = pd.Series([5.0, 3.0, 4.0, 2.0, 3.0, 1.0])
c = pd.Series([4.0, 6.0, 5.0, 7.0, 6.0, 8.0])
x = np.vstack((a, b, c))
r = np.corrcoef(x)
print(r)
