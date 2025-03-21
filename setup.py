from setuptools import setup, find_packages

setup(
    name="dvmcp",
    version="0.1.0",
    description="Damn Vulnerable Model Context Protocol - An educational tool for ML security",
    author="Security Researcher",
    author_email="researcher@example.com",
    packages=find_packages(),
    install_requires=[
        'flask==2.0.1',
        'numpy==1.21.0',
        'torch==1.9.0',
        'transformers==4.11.0',
        'scikit-learn==0.24.2',
        'requests==2.26.0',
        'python-dotenv==0.19.0',
        'werkzeug==2.0.1',
        'jsonschema==3.2.0',
        'pyjwt==2.1.0'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Security',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
    python_requires='>=3.8',
) 