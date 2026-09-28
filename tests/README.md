So it seems like the iteration and length columns aren't actually being recorded. So before I make any more changes to the code I am going to run the following tests from the root directory:
```bash
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml -outfile=tests/Demography1_columns_test_precommit.txt -iterations=5
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -outfile=tests/PapuansOutOfAfrica_10J19_columns_test_precommit.txt -iterations=5
```
Then I will verify that the iterations and length columns are not being recorded in `tests.ipynb`.

Now that I have verified and fixed the bug, I run the following tests from the root directory:
```bash
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml -outfile=tests/Demography1_columns_test_postcommit.txt -iterations=5
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -outfile=tests/PapuansOutOfAfrica_10J19_columns_test_postcommit.txt -iterations=5
```