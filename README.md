# Textifai
A web-based and social text analyzation project aiming to provide insights about language and its usage. 
http://textifai.herokuapp.com

## General Dependencies: 
- NLTK
- Pillow
- Indicoio 
- Whitenoise

Install these dependencies using pip by typing the following commands in a terminal: 
```
pip install nltk 
pip install pillow
pip install indicoio 
pip install whitenoise
```

## NLTK Dependencies 
1 - After installing NLTK, you need to install a few NLTK-specific packages for everything to work properly. 
Type the following in the python3 interactive shell: 
```
import nltk 
nltk.download() 
```
2 - The NLTK Downloader GUI should display. Click the "All Packages" tab, and install the following:  
- averaged_perceptron_tagger
- punkt 
- vader_lexicon

If a NLTK Downloader GUI didn't display in step 2, type the following commands in a terminal: 
``` 
python -m nltk.downloader averaged_perceptron_tagger
python -m nltk.downloader punkt
python -m nltk.downloader vader_lexicon
```
