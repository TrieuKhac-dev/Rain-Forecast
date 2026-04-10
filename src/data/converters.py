from typing import cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray


def dataframe_to_numpy(df: pd.DataFrame) -> NDArray[np.float64]:
    """Convert DataFrame to NumPy array"""
    return cast(NDArray[np.float64], df.to_numpy(dtype=np.float64))
