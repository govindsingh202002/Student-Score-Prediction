from setuptools import setup,find_packages
import os
from typing import List
requirement_file_path=os.path.join(os.getcwd(),'requirements.txt')

def get_requirements(file_path)->List[str]:
    'this function will return list of all the requirements from requirement.txt file'
    requirements=[]
    with open(file_path,'r') as file_object:
        requirements=file_object.readlines()
        requirements=[requirement.replace('\n','') for requirement in requirements]
        
    if '-e .' in requirements:
        requirements.remove('-e .')

    return requirements

setup(
    name='student_performance',
    version='0.0.1',
    author='Govind Singh',
    author_email='govindsingh202002@gmail.com',
    packages=find_packages(),
    install_requres=get_requirements(requirement_file_path)
)
