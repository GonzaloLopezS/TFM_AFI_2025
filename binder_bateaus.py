import numpy as np
import pandas as pd
from marinetrafficapi import MarineTrafficApi

api = MarineTrafficApi(api_key="565b636b073b55b4de19a39b55c2a3cde88c4f3f")
vessel_positions = api.vessel_historical_track()