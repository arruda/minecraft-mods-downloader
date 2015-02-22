from setuptools import setup

setup(
    name='minecraft-mods-downloader',
    version='0.6.1',
    description="Control minecraft mods download easily with this tool",
    author='Felipe Arruda Pontes',
    author_email='contato@arruda.blog.br',
    url='https://github.com/arruda/minecraft-mods-downloader',
    py_modules=['mine_mods'],
    install_requires=[
        'click>=3.3',
        'PyYAML>=3.11'
    ],
    license="MIT",
    keywords='minecraft, download, mods, control',
    entry_points="""
        [console_scripts]
        mine_mods=mine_mods:install_mods
    """,
    # test_suite='tests',
    # tests_require=test_requirements
)
