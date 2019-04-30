# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name = "EP_BHC",
    package = ["EP_BHC"]
    version = "1.0",
    license = "MIT",
    description = "A Python package to generate Bayesian hierarchical clusters to a supplied data",
    authors = "Eric Su and Min Chul Kim",
    author_email = "minchel93@gmail.com"
    url = https://github.com/Eric-Su-2718/STA663-Final-Project,
    download_url = 'https://github.com/Eric-Su-2718/STA663-Final-Project/archive/v_01.tar.gz',
    keywords = ["BHC", "merge_nodes", "likelihood"]
    install_requires = [
        "numpy", 
        "itertools",
        "scipy.special"
    ]
)

