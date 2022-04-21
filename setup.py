from setuptools import setup
  
setup(
    name='draw_connectogram',
    version='0.0.1a1',
    description='a command line tool to draw connectogram visualisations of symmetric adjacency matrices',
    url='https://github.com/eilidhmacnicol/draw_connectograms',
    author='Eilidh MacNicol',
    author_email='eilidhmacnicol@gmail.com',
    license='GPL',
    packages=['draw_connectograms'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Utilities',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=['matplotlib', 'networkx', 'numpy', 'nxviz', 'pandas'],
    python_requires='>=3.9',
    entry_points={'console_scripts': ['draw_connectogram = draw_connectograms.cli:main']}
)