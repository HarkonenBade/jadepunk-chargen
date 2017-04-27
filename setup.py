from distutils.core import setup

setup(
    name='jadepunk-chargen',
    version='0.0.1',
    packages=['jadepunk', 'jadepunk.engine'],
    requires=['pyyaml'],
    url='https://github.com/HarkonenBade/jadepunk-chargen',
    license='MIT',
    author='Harkonen Bade',
    author_email='jadepunk@harkonen.net',
    description='A simple char specification system for Jadepunk.'
)
