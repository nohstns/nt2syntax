# Tool for Automatic Assessment of the Writing of DSL Learners

## About the project
This repository contains the scripts developed for my MA thesis on the assessment of the syntactic complexity and writing quality development of early learners of Dutch as a L2 (NT2/DSL).

### Abstract
The study of the automatic assessment of writing quality and development has been carried out extensively in the context of English as a Second Language (ESL), less so in other languages. This exploratory study is an attempt to open up the discussion in the field of Dutch as a Second Language (DSL) and of less proficient language learners.
Syntactic complexity features have shown to be informative of writing quality for ESL learners. The question then arises whether similar features can be used to assess a DSL text’s quality and development as well. We developed a tool to automatically assess a Dutch text’s syntactic complexity inspired on the fine-grained features identified by Crossley and McNamara (2014) in their study of ESL writing development. This system extracts several T-Scan (Pander Maat et al. 2014) and also relies on information from the Dutch dependency parser Alpino Van Noord and others (2006).
An exploratory study was carried out to test whether these features are capable of distinguishing between a text written by native speakers and early DSL learners relying on both statistical analysis and machine learning techniques. Our findings suggest that syntactic variability and indices of nominal complexity as computed by our system are indicative of text quality and could therefore be used as a proxy when assessing the quality of academic-oriented DSL learners.

**KEYWORDS** Writing quality, Dutch as a Second Language, L2 Writing

### References
Crossley, Scott A. and Danielle S. McNamara. 2014. Does writing development equal writing quality? A computational investigation of syntactic complexity in L2 learners. _Journal of Second Language Writing_, 26:66–79.

Pander Maat, H. L. W., R. L. Kraf, Antal van den Bosch, Maarten van Gompel, S. Kleijn, T. J. M. Sanders, and Ko van der Sloot. 2014. T-Scan: a new tool for analyzing Dutch text. Accepted: 2015-11-12T11:00:11Z ISSN: 2211-4009 Pages: 53-74 Volume: 4.

van Noord, Gertjan. 2006. At last parsing is now operational. In _TALN06. Verbum Ex Machina. Actes de la 13e conference sur le traitement automatique des langues naturelles_, pages 20–42.


## Getting started
### Assumptions
The scripts assume that:
  * the raw datasets are stored in a `*.csv` file.
    - The original text should be found under a column titled "TypedText".
    - The participants' ids are stored under a column titled "participantnummer".
    - All other columns in the `*.csv` file will be ignored.
  * the Alpino output is stored in a folder in the same directory as the scripts called `alpino_output`
    - In this folder, each text has its own `text_n.txt` folder, where `n = text id number`
    - Each `text_n.txt` folder contains a file for each sentence as parsed by Alpino, named `n.xml` where `n = sentence number`.
  * the T-Scan output is stored in two files within a folder in the same directory as the scripts called `tscan_output`
    - T-Scan's analysis for all texts at the document level is stored in file `/tscan_output/{filename}_total.doc.csv`, where `filename = name of the raw *.csv dataset`
    - T-Scan's analysis for all texts at the sentence level is stored in file `tscan_output/{filename}_total.sen.csv`, where `filename = name of the raw *.csv dataset`


### Requirements
  * Requires Python 3.7+
  * The scripts require the preinstallation of the following modules
    - pandas
    - regex
    - xml.etree
    - apted
    - stanza
    - numpy

**Note**: A `setup.py` script will be added in the future to prevent having to install these packages manually


## Usage
* As for now, the scripts require the user to run Alpino and T-Scan separately.

### Preprocessing
* Required for proper analysis by Alpino and T-Scan
* `python preprocessing.py <dataset path> <dataset label>`
  - Dataset label is optional; can be useful when generating multiple outputs

This returns one `*.txt` file with all preprocessed texts split by a blank line, a directory containing a `*.txt` file for each text named with the number according to the order in which they were found in the `*.csv` file and a `*.csv` with all the preprocessed texts.

## Alpino & T-Scan
* Currently not supported within the tool itself; needs to be run separately
* See https://webservices.cls.ru.nl/tscan/index/ and https://www.let.rug.nl/vannoord/alp/Alpino/
* Store the tools' outputs in their correct directories as specified in [link](### Assumptions)

### Feature extraction
* `python analysis.py <preprocessed dataset.csv filename> <new dataset label>`
* Returns two `*.csv` files:
    - The measured features for each text at the document level: `vectorized_{filename}{dataset_label}.doc.csv`; where
        + Each row corresponds to one text
        + Each column contains one total value for each feature

   ![image](https://user-images.githubusercontent.com/58168916/122470066-f02a3a80-cfbd-11eb-828c-876eb0006c0c.png)


    - The measured features for each text at the sentence level: `vectorized_{filename}{dataset_label}.sen.csv`; where
        + Each row corresponds to one text
        + Each column contains a list with the index' score for each sentence
        
   ![image](https://user-images.githubusercontent.com/58168916/122469837-accfcc00-cfbd-11eb-96c3-1c3487dd1e94.png)

**Note**: A modification of the sentence level output is planned where the tool will return one row for each sentence:

![image](https://user-images.githubusercontent.com/58168916/122470220-17810780-cfbe-11eb-9654-148134e95d45.png)


## Contact
Nafal Ossandón Hostens - @nafalohstns - nafal.ossandonhostens@student.uantwerpen.be

Project Link: https://github.com/nohstns/nt2syntax
