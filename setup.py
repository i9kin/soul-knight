from setuptools import setup, find_packages

setup(
    name="soulknight",
    version="1.1",
    description="The funniest joke in the world",
    long_description="pygame",
    classifiers=["Programming Language :: Python :: 3.7",],
    keywords="game for yandex lyceum",
    url="https://github.com/9kin/soul-knight",
    author="9kin",
    license="MIT",
    packages=find_packages(),
    install_requires=["pygame", "pygame-menu",],
    dependency_links=["https://github.com/9kin/pytmxloader"],
    entry_points={"console_scripts": ["soulknight = soulknight:main"]},
    include_package_data=True,
    zip_safe=False,
)
