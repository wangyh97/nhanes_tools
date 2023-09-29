import logging
log_path = 'example.log'
log = logging.getLogger('recorder')
log.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_path,mode='a+')
handler1 = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
handler1.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
formatter1 = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
handler.setFormatter(formatter)
handler1.setFormatter(formatter1)
log.addHandler(handler)
log.addHandler(handler1)

log.info('an info')