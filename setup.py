import setuptools

setuptools.setup(
    name="Pizdyuk",
    version="0.0.1",
    author="Jahangir Gasimov",
    description="Stock Market Simulation tool",
    url="https://github.com/aufdnb/Pizdyuk.git",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[

    ],
    python_requires=">=3.9"
)