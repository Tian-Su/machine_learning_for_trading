# machine\_learning\_for\_trading
This repo host the code of Georgia Tech Computer Science Master Degree #7646 (ml4t)


# ML4T_2017Summer
Course website:
http://quantsoftware.gatech.edu/CS7646_Summer_2017

Information on cloning this repository and using the autograder on buffet0x servers:
http://quantsoftware.gatech.edu/ML4T_Software_Setup

# Clone a private repo from command line

git clone https://username:password@github.com/Tian-Su/machine\_learning\_for\_trading.git

# commands to run the test scripts

```
PYTHONPATH=../:. python testlearner.py Data/Istanbul.csv

PYTHONPATH=../:. python grade_learners.py 

PYTHONPATH=../:. python grade_best4.py

PYTHONPATH=..:. ORDERS_DATA_DIR=. python grade_marketsim.py
```