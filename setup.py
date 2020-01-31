from setuptools import setup, find_packages

setup(
    name="soulknight",
    version="1.3",
    description="The funniest joke in the world",
    long_description="pygame",
    classifiers=["Programming Language :: Python :: 3.7"],
    keywords="game for yandex lyceum",
    url="https://github.com/9kin/soul-knight",
    author="9kin",
    license="MIT",
    packages=find_packages(),
    install_requires=["tiledtmxloader", "pygame", "pygame-menu"],
    entry_points={"console_scripts": ["soulknight = soulknight:main"]},
    include_package_data=True,
    setup_requires=["wheel"] ,
    zip_safe=False,
)
