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

Great, with that bug fixed, now I want to actually compare how Skov's method calls segments vs my own method. Note that I don't really care about the mutation tracking since I assume Skov is doing that for hmmix given the `max_time` check.To compare the segments called by the two methods, I will only use the tree sequence files to call segments, by running the following commands from the root directory:
```bash
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml -outfile=tests/Demography1_segment_test.txt -iterations=10 -tsfile=tests/Demography1
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -outfile=tests/PapuansOutOfAfrica_10J19_segment_test.txt -iterations=10 -tsfile=tests/PapuansOutOfAfrica_10J19
```

So, our two methods call the same number of segments, but `Keeptrack_of_introgressed.py` calls slightly longer segments when the migrating tract does not fully overlap the marginal tree (see `tests.ipynb` for more details). I believe the fix is to simply change `introgressed_seg[l, admixinfo].append([tree_left, tree_right])` (on line 81 in commit `104fa43`) to `introgressed_seg[l, admixinfo].append([max(tree_left, int(mr.left)), min(tree_right, int(mr.right))])`. I validate this by running the following commands from the root directory:
```bash
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml -outfile=tests/Demography1_segment_fixed.txt -iterations=10
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -outfile=tests/PapuansOutOfAfrica_10J19_segment_fixed.txt -iterations=10
```