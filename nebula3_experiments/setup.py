from setuptools import setup, find_packages

setup(
    name='nebula3_experiments',
    packages=find_packages(),
    install_requires=[
        "cachetools",
        "opencv-python",
        "opencv-contrib-python"
    ], # add any additional packages that
    # needs to be installed along with your package. Eg: ''
    description='LLM experiments for nebula3',
    version='0.0.10',
    url='https://github.com/NEBULA3PR0JECT/nebula3_experiments',
    author='Hanoch',
    author_email='hanoch.kremer@gmail.com',
    keywords=['pip', 'pypi', 'microservice']
)
