from setuptools import setup

setup(
	name='ohsheet',
	version='0.1',
	description='A small spreadsheet editor',
	author='Brian Cruz',
	license='MIT',
	packages=['ohsheet'],
	entry_points={
		'console_scripts': [
			'ohsheet=ohsheet.sheet:main',
		],
	},
)

