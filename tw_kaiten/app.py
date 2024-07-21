from tw_kaiten.logger import Logger
from tw_kaiten.schemas import Config, TimeTrackingItemDC
from tw_kaiten.kaiten_accessor import KaitenAccessor


def app(stdin: str) -> None:
    summary_time = 0
    raw_configuration, raw_timetracks = stdin.split("\n\n")

    config = Config(raw_configuration)
    logger = Logger()
    yt_accessor = KaitenAccessor(config, logger)

    yt_accessor.check_connection()

    timetracks = TimeTrackingItemDC.load_many(raw_timetracks, config)

    for timetrack in timetracks:
        yt_accessor.check_issue(timetrack)
    #
    for timetrack in timetracks:
        yt_accessor.load_time_track(timetrack)
        summary_time += timetrack.minutes

    logger(f"Summary: {summary_time}mins")
