import os
import yaml, time, joblib
import numpy as np
from datetime import datetime
from enum import Enum, IntEnum
from collections import defaultdict
from .settings import settings
from .history import window


class Level(IntEnum):
    OK = 0
    INFO = 1
    WARN = 2
    CRIT = 3

    def __str__(self):
        return self.name

_state = defaultdict(lambda: Level.OK)
_last_alert = defaultdict(float)
_cfg_ts = 0
_cfg = {}

def _load_cfg():
    global _cfg, _cfg_ts
    mtime = os.path.getmtime(settings.THRESHOLD_FILE)
    if mtime > _cfg_ts:
        with open(settings.THRESHOLD_FILE) as f:
            _cfg = yaml.safe_load(f)
        _cfg_ts = mtime

def z(today: int, arr: np.ndarray) -> float:
    med = np.median(arr)
    mad = np.median(np.abs(arr - med))
    return 0.6745 * (today - med) / max(mad, 1)

def classify(z: float, part: str) -> Level:
    cfg = _cfg["partitions"].get(part, _cfg["global"])
    if z <= cfg["crit_z"]:
        return Level.CRIT
    elif z <= cfg["warn_z"]:
        return Level.WARN
    elif z <= cfg["info_z"]:
        return Level.INFO
    else:
        return Level.OK
    
def should_emit(part: str, level: Level) -> bool:
    now = time.time()
    if level > _state[part]:
        _last_alert[part] = now
        _state[part] = level
        return True
    
    if level <= Level.OK:
        _state[part] = Level.OK
    
    return False