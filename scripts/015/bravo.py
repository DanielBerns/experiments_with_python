import logging
from alpha import create, read, update, delete

logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

logger = logging.getLogger()


def main():
   logger.debug('This message should go to the log file')
   try:
       create("1", {"a": 0, "b": 1})
   except Exception as e:
       logger.info(str(e))
   try:
       create("2", {"a": 3, "b": -1})
   except Exception as e:
       logger.info(str(e))
   logger.info('So should this')
   try:
       create("1", {"a": 0, "b": 1})
   except Exception as e:
       logger.info(str(e))
   try:
       create("2", {"a": 3, "b": -1})
   except Exception as e:
       logger.info(str(e))
   logger.warning('And this, too')
   try:
       aa = read("3")
   except Exception as e:
       logger.info(str(e))
   try:
       bb = read("2")
   except Exception as e:
       logger.info(str(e))
   logger.error('And non-ASCII stuff, too, like Øresund and Malmö')

if __name__ == "__main__":
    main()
