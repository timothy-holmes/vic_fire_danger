import sys
import logging
import traceback

logging.basicConfig(
    filename=r'.\vic_fire_danger.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG
)

def custom_excepthook(exc_type, exc_value, exc_traceback):
    # Do not print exception when user cancels the program
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logging.error("An uncaught exception occurred:")
    logging.error("Type: %s", exc_type)
    logging.error("Value: %s", exc_value)

    if exc_traceback:
        format_exception = traceback.format_tb(exc_traceback)
        for line in format_exception:
            logging.error(repr(line))

sys.excepthook = custom_excepthook


from history import HistoryClient, HistoryConfig
from parse_feed import ForecastClient, ForecastConfig

def main():
    hc = HistoryClient(HistoryConfig)
    fc = ForecastClient(ForecastConfig)
    hc.load_history()
    pub_date, items = fc.get_latest_data()
    new_forecasts = fc.get_forecasts(items)
    hc.update_history(pub_date, new_forecasts)
    hc.save_history()

if __name__ == '__main__':
    main()