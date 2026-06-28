import logging
import logging.handlers
from alpha import create, read, update, delete

logger = logging.getLogger()
logger.setLevel(logging.INFO)

foxtrot_handler = logging.handlers.RotatingFileHandler(
    "foxtrot.log",
    maxBytes=16*1024,
    backupCount=5)
foxtrot_handler.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to foxtrot_handler
foxtrot_handler.setFormatter(formatter)

# add ch to logger
logger.addHandler(foxtrot_handler)

def main():
   logger.debug('This message should go to the console')
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
