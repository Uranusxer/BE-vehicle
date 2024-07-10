import datetime
def get_timestamp():
    return (datetime.datetime.now()).timestamp()

def to_millisecond_timestamp(dt: float) -> int:
    # 转换为毫秒级 UNIX 时间戳
    return int(dt * 1_000)
