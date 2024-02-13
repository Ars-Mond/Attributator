from setuptools import setup, find_packages

setup(
    name='Releazer',
    version='0.0.1',
    description='',
    packages=find_packages(),
    install_requires=[
        'dearpygui',
        # 'mutagen',
        # 'hachoir',
        'xdialog',
        'PyYaml',
        'PyExifTool',
        'numpy',
        # 'tqdm',
    ],
)
