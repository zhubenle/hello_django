import logging

from hello_django import utils
from hello_django.backend.vos import MenuVO


def test_str_format():
    print('this is test str format {0}'.format(1))


def test_boolean():
    print(not None)
    print(not 0)
    print(not False)
    print(not '')


def test_logging():
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    logging.debug("This is a debug log.")
    logging.info("This is a info log.")
    logging.warning("This is a warning log.")
    logging.error("This is a error log.")
    logging.critical("This is a critical log.")


def test_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    fm = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s')

    sh.setFormatter(fmt=fm)
    logger.addHandler(sh)
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')


def test_json():
    d = {'id': 1, 'parent_id': None, 'title': 'test'}
    test_vo = MenuVO()
    print(hasattr(test_vo, 'id'))
    print(utils.dict_to_obj(d, test_vo))
    print(test_vo)


def filter_dict():
    dict_list = [{'a': 1, 'b': '1b'}, {'a': 1, 'b': '2c'}, {'a': 0, 'b': '3d'}]
    print(list(filter(lambda d: d.get('a') == 1, dict_list)))


def test_str():
    print('0][search][regex]'.split('][', 1))


def test_map():
    test_list_param(*(map(lambda x: int(x) + 1, ['1', '2', '3'])))


def test_list_param(*kwargs):
    print(kwargs)


def test_bool():
    print(type(True))


if __name__ == '__main__':
    d = {'a': 1, 'b': 2}
