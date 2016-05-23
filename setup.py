from setuptools import find_packages, setup


version = '0.1.5'


setup(
    name='django-user-deletion',
    packages=find_packages(),
    include_package_data=True,
    version=version,
    license='BSD',
    description='Management commands to notify and delete inactive django users',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    author='Incuna Ltd',
    author_email='admin@incuna.com',
    url='https://github.com/incuna/django-user-deletion',
)
