import setuptools

setuptools.setup(
    name="Pizdyuk",
    version="0.0.1",
    author="Jahangir Gasimov",
    description="Stock Market Simulation tool",
    url="https://github.com/aufdnb/Pizdyuk.git",
    package_dir={"": "pizdyuk"},
    packages=setuptools.find_packages(where="pizdyuk"),
    install_requires=[

    ],
    setup_requires=["pytest-runner"],
    test_suite="tests",
    tests_require=[
        "pytest",
        "pytest-mock",
    ],
    python_requires=">=3.9"
)