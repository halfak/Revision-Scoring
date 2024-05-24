[![Build Status](https://travis-ci.org/wikimedia/revscoring.svg?branch=master)](https://travis-ci.org/wikimedia/revscoring)
[![Test coverage](https://codecov.io/gh/wikimedia/revscoring/branch/master/graph/badge.svg)](https://codecov.io/gh/wikimedia/revscoring)
[![GitHub license](https://img.shields.io/github/license/wikimedia/revscoring.svg)](./LICENSE)
[![PyPI version](https://badge.fury.io/py/revscoring.svg)](https://badge.fury.io/py/revscoring)
# Revision Scoring

<blockquote>
⚠️ Warning: As of late 2023, the ORES infrastructure is being deprecated by the
WMF Machine Learning team, please check https://wikitech.wikimedia.org/wiki/ORES for more info.

While the code in this repository may still work, it is unmaintained, and as
such may break at any time. Special consideration should also be given to
machine learning models seeing drift in quality of predictions.

The replacement for ORES and associated infrastructure is Lift Wing:
https://wikitech.wikimedia.org/wiki/Machine_Learning/LiftWing

Some Revscoring models from ORES run on the Lift Wing infrastructure, but they
are otherwise unsupported (no new training or code updates).

They can be downloaded from the links documented at:
https://wikitech.wikimedia.org/wiki/Machine_Learning/LiftWing#Revscoring_models_(migrated_from_ORES)

In the long term, some or all these models *may* be replaced by newer models
specifically tailored to be run on modern ML infrastructure like Lift Wing.

If you have any questions, contact the WMF Machine Learning team:
https://wikitech.wikimedia.org/wiki/Machine_Learning
</blockquote>

A generic, machine learning-based revision scoring system designed to help automate critical wiki-work — for example, vandalism detection and removal. This library powers [ORES](https://ores.wikimedia.org).

## Example


Using a scorer_model to score a revision::
```python
  import mwapi
  from revscoring import Model
  from revscoring.extractors.api.extractor import Extractor

  with open("models/enwiki.damaging.linear_svc.model") as f:
       scorer_model = Model.load(f)

  extractor = Extractor(mwapi.Session(host="https://en.wikipedia.org",
                                          user_agent="revscoring demo"))

  feature_values = list(extractor.extract(123456789, scorer_model.features))

  print(scorer_model.score(feature_values))
  {'prediction': True, 'probability': {False: 0.4694409344514984, True: 0.5305590655485017}}
  ```


# Installation

The easiest way to install is via the Python package installer
(pip).

``pip install revscoring``

You may find that some of the dependencies fail to compile (namely
`scipy`, `numpy` and `sklearn`).  In that case, you'll need to install some
dependencies in your operating system.

### Ubuntu & Debian:
  *  Run ``sudo apt-get install python3-dev g++ gfortran liblapack-dev libopenblas-dev enchant``
  *  Run ``sudo apt-get install aspell-ar aspell-bn aspell-el aspell-id aspell-is aspell-pl aspell-ro aspell-sv aspell-ta aspell-uk myspell-cs myspell-de-at myspell-de-ch myspell-de-de myspell-es myspell-et myspell-fa myspell-fr myspell-he myspell-hr myspell-hu myspell-lv myspell-nb myspell-nl myspell-pt-pt myspell-pt-br myspell-ru myspell-hr hunspell-bs hunspell-ca hunspell-en-au hunspell-en-us hunspell-en-gb hunspell-eu hunspell-gl hunspell-it hunspell-hi hunspell-sr hunspell-vi voikko-fi``
<!-- ### Windows:
<i>TODO</i>
-->
### MacOS:
Some of the `revscoring` dependencies doesn't have wheel for python version > 3.7, thus it is required to install it with a python 3.7 version.
  
Using Homebrew and pip, installing `revscoring` and `enchant` can be accomplished as follows:

```bash
brew install aspell
brew install enchant
pip install revscoring
```
#### Apple Silicon (M1)
As for now (2022/01/13), some of the dependencies of `revscoring` cannot be installed on the native `arm64` Apple Silicon (M1) architecture. Thus, the installation must be performed using the `-x86_64` Rosetta2 simulator.

#### Adding languages in aspell (MacOS only)

```bash
cd /tmp
wget http://ftp.gnu.org/gnu/aspell/dict/pt/aspell-pt-0.50-2.tar.bz2
bzip2 -dc aspell-pt-0.50-2.tar.bz2 | tar xvf -
cd aspell-pt-0.50-2
./configure
make
sudo make install
```

 Caveats: <br>
  <b><u> The differences between the `aspell` and `myspell` dictionaries can cause </b>
    <b> <u>some of the tests to fail </b>


Finally, in order to make use of language features, you'll need to download
some NLTK data.  The following command will get the necessary corpora.

``python -m nltk.downloader omw sentiwordnet stopwords wordnet``

You'll also need to install [enchant](https://en.wikipedia.org/wiki/Enchant_(software))-compatible
dictionaries of the languages you'd like to use.  We recommend the following:

* languages.arabic: aspell-ar
* languages.basque: hunspell-eu
* languages.bengali: aspell-bn
* languages.bosnian: hunspell-bs
* languages.catalan: myspell-ca
* languages.czech: myspell-cs
* languages.croatian: myspell-hr
* languages.dutch: myspell-nl
* languages.english: myspell-en-us myspell-en-gb myspell-en-au
* languages.estonian: myspell-et
* languages.finnish: voikko-fi
* languages.french: myspell-fr
* languages.galician: hunspell-gl
* languages.german: myspell-de-at myspell-de-ch myspell-de-de
* languages.greek: aspell-el
* languages.hebrew: myspell-he
* languages.hindi: aspell-hi
* languages.hungarian: myspell-hu
* languages.icelandic: aspell-is
* languages.indonesian: aspell-id
* languages.italian: myspell-it
* languages.latvian: myspell-lv
* languages.norwegian: myspell-nb
* languages.persian: myspell-fa
* languages.polish: aspell-pl
* languages.portuguese: myspell-pt-pt myspell-pt-br
* languages.serbian: hunspell-sr
* languages.spanish: myspell-es
* languages.swedish: aspell-sv
* languages.tamil: aspell-ta
* languages.russian: myspell-ru
* languages.ukrainian: aspell-uk
* languages.vietnamese: hunspell-vi

# Development
To contribute, ensure to install the dependencies:
```bash
$ pip install -r requirements.txt
```

Install necessary NLTK data:

``python -m nltk.downloader omw sentiwordnet stopwords wordnet``

## Running tests
Make sure you install test dependencies:

```bash
$ pip install -r test-requirements.txt
```

Then run:

```bash
$ pytest . -vv
```
# Reporting bugs
To report a bug, please use [Phabricator](https://phabricator.wikimedia.org/maniphest/task/edit/form/1/?projects=revscoring)

# Authors
  *   [Aaron Halfaker](http://halfaker.info)
  *   [Helder](https://github.com/he7d3r)
  *   [Adam Roses Wight](https://mediawiki.org/wiki/User:Adamw)
  *   [Amir Sarabadani](https://github.com/Ladsgroup)
