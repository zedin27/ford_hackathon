from setuptools import find_packages, setup

setup(
    name="car_client",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-sqlalchemy"
    ],
)
