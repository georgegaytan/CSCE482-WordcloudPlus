# CSCE482-WordcloudPlus
Mining and animating Wordclouds (as a TAMU Computer Science Capstone)


# Installation
Under the assumption that the user uses python 2.7 with the pip installer, the following are the instructions to setup the project. *(In the absence of python 2.7 and pip, see https://www.python.org/ for instruction. Steps to follow are dependent on your system. If you are using python 3+, please use python2 and pip2 for installation.)*
1. Go to our github at https://github.com/ggaytan00/CSCE482-WordcloudPlus and download the zip of the project/or clone it from the repo link
2. In the environment, be sure to install all packages using setup.py. Assuming these are not already installed. 
    1. For python 2.7 users
        1. python setup.py
    2. For python 3+ users
        1. python2 setup.py
3. For nltk, there is a second step for installation (WARNING: Can take up to 10 or 15 minutes depending on download speed)
    1. For python 2.7 users
        1. pip install nltk
        2. python
        3. \>>> import nltk
        4. \>>> nltk.download()
        5. Downloader> d
        6. Identifier> all
    2. For python 3+ users
        1. pip2 install nltk
        2. python2
        3. \>>> import nltk
        4. \>>> nltk.download()
        5. Downloader> d
        6. Identifier> all
4. Once these are installed correctly, go to \CSCE482-WordcloudPlus-landingpage\wordcloudplus. In the python window, run the command python manage.py runserver. 
    1. This should run the application on your localhost server at port 8000, or whichever URL Django returns
