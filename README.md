# NT2 Syntactic Development Analysis & Assessment

This repository contains the scripts developed for my MA thesis on the assessment of the syntactic complexity and writing quality development of early learners of Dutch as a L2 (NT2/DSL).

The scripts assume that:
  * the raw datasets are stored in a `*.csv` file. The original text should be found under a column titled "TypedText".
  * the Alpino output is stored in a folder in the same directory as the scripts called `xml`
    - In this folder, each text has its own `text_n.txt` folder, where `n = text id number`
    - Each `text_n.txt` folder contains __one__ file titled `1.xml`
