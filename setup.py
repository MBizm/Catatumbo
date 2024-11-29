try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='catatumbo',
    url='"https://github.com/MBizm/Catatumbo"',
    description='"Catatumbo is an Adaptive Smart Home Lightning project that lets your home indicate information like stock prices, weather forecasts, social media states on your LED strip."',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        'requests==2.31.0',
        'ipinfo==3.0.0',
        'Adafruit_Blinka==3.0.1',
        'astral==1.10.1',
        'adafruit_circuitpython_neopixel==3.4.0',
        'pytz==2019.1',
        'numpy==1.17.1',
        'pyowm==2.10.0',
        'board==1.0',
    ],
    py_modules=[
        '"catatumbo.controller.forecast.adafruit_forecast"',
    ],
)