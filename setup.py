from setuptools import setup

setup(
    name='minecraft-mods-downloader',
    version='0.5',
    description="Control minecraft mods download easily with this tool",
    py_modules=['mine_mods'],
    install_requires=[
        'click>=3.3',
        'PyYAML>=3.11'
    ],
    license="MIT",
    keywords='minecraft, download, mods, controll',
    entry_points="""
        [console_scripts]
        mine_mods=mine_mods:install_mods
    """,
    # test_suite='tests',
    # tests_require=test_requirements
)
