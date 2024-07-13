from setuptools import find_packages,setup
from typing import List


HYPHEN_E_DOT = '-e .' #created constraint so -e . is not read by get_requirements()

#this function will return a list of requirements
def get_requirements(file_path:str) -> List[str]:
    requirements=[]
    with open(file_path) as file_obj: #temp obj
        requirements = file_obj.readlines() #one element read at a time but \n will be added each time therefore we have to replace it
        requirements = [req.replace("\n", "") for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
name='student_performance_indicator',
version='0.0.1',
author='Fagun',
author_email='saraswatfagun@gmail.com',
packages=find_packages(),
install_requires= get_requirements('requirements.txt')
)
