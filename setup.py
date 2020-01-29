from setuptools import setup, find_packages

setup(name='soulknight',
      version='0.1',
      description='The funniest joke in the world',
      long_description='Really, the funniest around.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      keywords='funniest joke comedy flying circus',
      url='https://github.com/9kin/soul-knight',
      author='9kin',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'pygame', 'pygame-menu',
      ],
      entry_points={
        'console_scripts':
            ['soulknight = soulknight:main']
      },

	  include_package_data=True,
      zip_safe=False
)