# Find_introgressed_segments
Find introgressed segments from an msprime simulation. Here are two examples you can run:

```note
usage: Keeptrack_of_introgressed.py [-h] -demography DEMOGRAPHY -samples
                                    SAMPLES [-outfile] [-printdemography]
                                    [-seed] [-iterations] [-genomesize]
                                    [-mutation_rate] [-recombination_rate]
                                    [-extrainfo] [-keepevents]

optional arguments:
  -h, --help            show this help message and exit
  -demography           yaml file with demography (default: None) < REQUIRED
  -samples              json file with samples (default: None)    < REQUIRED
  -outfile              output name (default: /dev/stdout)
  -printdemography      print demography and save to pdf (default: )
  -seed                 set seed (default: 1234)
  -iterations           number of independent iterations (default: 1)
  -genomesize           size of genome (default: 10000000)
  -mutation_rate        genome wide mutation rate (default: 1.45e-08)
  -recombination_rate   genomewide recombination rate (default: 1.45e-08)
  -extrainfo            print snp positions and ages (default: False)
  -keepevents           filter events containing this word (or more words
                        comma separated like Nea,Den) (default: )
```



```note
# try this
python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml

# or this 
python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -keepevents=Den,Nea
```

The program needs two files to run. A Demography file in yaml format and a list of samples in json format. 
The list of samples needs to be in 3 types of classes: Ingroup, Sequenced_Archaics and Outgroup:

```json
{
	"Ingroup":
		[{"num_samples":1, "population": "Ingroup", "time": 0, "ploidy": 2}],
	"Sequenced_Archaics":
		[{"num_samples":1, "population": "Seq_DEN", "time": 0, "ploidy": 2}],
	"Outgroup":
		[{"num_samples":1, "population": "Outgroup", "time": 0, "ploidy": 2}]
}
```

Below is an example output from the first scenario (first 10 lines):

```note
> python Keeptrack_of_introgressed.py -samples=samples.json -demography=Demography1.yaml

iteration  haplotype  pop      start    end       length  admix_event          admixtime  snps  Seq_DEN
0          0          Ingroup  126443   158290    31847   Distant_DEN>Ingroup  1551.7     7     5
0          0          Ingroup  206139   223580    17441   Distant_DEN>Ingroup  1551.7     8     4
0          0          Ingroup  1006542  1007305   763     Distant_DEN>Ingroup  1551.7     0     0
0          0          Ingroup  1180240  1290919   110679  Distant_DEN>Ingroup  1551.7     27    13
0          0          Ingroup  1342407  1344305   1898    Distant_DEN>Ingroup  1551.7     2     0
0          0          Ingroup  1458530  1459883   1353    Distant_DEN>Ingroup  1551.7     0     0
0          0          Ingroup  1823533  1897035   73502   Distant_DEN>Ingroup  1551.7     23    16
0          0          Ingroup  2100370  2230879   130509  Close_DEN>Ingroup    1517.2     31    24
0          0          Ingroup  2533876  2713571   179695  Distant_DEN>Ingroup  1551.7     51    29
0          0          Ingroup  2744458  2797000   52542   Distant_DEN>Ingroup  1551.7     14    11
```
And here is the output from the second example:

```note
> python Keeptrack_of_introgressed.py -samples=samples_10J19.json -demography=PapuansOutOfAfrica_10J19.yaml -keepevents=Den,Nea

iteration  haplotype  pop     start    end       length  admix_event  admixtime  snps  DenA  NeaA
0          0          Papuan  1614304  1675141   60837   Nea1>CHB     1566.0     17    0     8
0          0          Papuan  3517329  3520336   3007    Nea1>Ghost   1853.0     2     0     2
0          0          Papuan  4018822  4021827   3005    Nea1>CHB     1566.0     0     0     0
0          0          Papuan  4335527  4345463   9936    Den2>Papuan  1575.9     3     0     0
0          0          Papuan  4737087  4758341   21254   Nea1>Ghost   1853.0     1     0     1
0          0          Papuan  8205564  8220378   14814   Den2>Papuan  1575.9     2     1     0
0          0          Papuan  8234794  8264856   30062   Den1>Papuan  1027.6     5     3     0
0          0          Papuan  8264856  8299847   34991   Den2>Papuan  1575.9     8     2     0
0          0          Papuan  9342040  9393543   51503   Nea1>Ghost   1853.0     17    0     8
0          1          Papuan  1929893  2257426   327533  Den1>Papuan  1027.6     108   56    7
0          1          Papuan  3527426  3537340   9914    Nea1>Ghost   1853.0     2     0     1
0          1          Papuan  4437003  4537228   100225  Den2>Papuan  1575.9     29    14    2
0          1          Papuan  4572355  4607718   35363   Den2>Papuan  1575.9     9     1     0
0          1          Papuan  8394955  8437184   42229   Den2>Papuan  1575.9     11    3     1
0          1          Papuan  8813714  8900024   86310   Den1>Papuan  1027.6     28    17    1
0          1          Papuan  9984824  10000000  15176   Den1>Papuan  1027.6     3     3     0
0          2          CHB     1491724  1524147   32423   Nea1>CHB     1566.0     12    0     8
0          2          CHB     2916318  2934384   18066   Nea1>CHB     1566.0     12    0     6
0          3          CHB     208367   211476    3109    Nea1>Ghost   1853.0     1     0     1
0          3          CHB     513855   579950    66095   Nea1>CHB     1566.0     18    0     12
0          3          CHB     1225849  1305600   79751   Nea1>Ghost   1853.0     26    0     9
0          3          CHB     1652698  1663466   10768   Nea1>Ghost   1853.0     1     0     1
0          3          CHB     3545699  3584760   39061   Nea1>Ghost   1853.0     11    0     0
0          3          CHB     4036931  4067929   30998   Nea1>Ghost   1853.0     4     1     2
0          3          CHB     4617903  4620830   2927    Nea1>CHB     1566.0     1     0     0
0          3          CHB     6431441  6518062   86621   Nea1>Ghost   1853.0     25    3     8
0          3          CHB     7707750  7723727   15977   Nea1>CHB     1566.0     3     0     1
0          3          CHB     9619011  9665197   46186   Nea1>Ghost   1853.0     2     0     2
0          4          CEU     0        43424     43424   Nea1>Ghost   1853.0     9     0     1
0          4          CEU     718461   820321    101860  Nea1>Ghost   1853.0     27    0     8
0          4          CEU     1098900  1366652   267752  Nea1>Ghost   1853.0     74    0     27
0          4          CEU     1426047  1495098   69051   Nea1>CHB     1566.0     24    0     9
0          4          CEU     1727433  1769000   41567   Nea1>Ghost   1853.0     13    0     4
0          4          CEU     2058427  2086293   27866   Nea1>Ghost   1853.0     9     1     3
0          5          CEU     631308   780476    149168  Nea1>Ghost   1853.0     50    1     13
0          5          CEU     1098900  1165393   66493   Nea1>Ghost   1853.0     12    0     3
0          5          CEU     1840668  1859572   18904   Den2>Papuan  1575.9     4     3     0
0          5          CEU     2385634  2453869   68235   Nea1>CHB     1566.0     23    2     14
0          5          CEU     3339230  3352266   13036   Nea1>Ghost   1853.0     4     0     0
0          5          CEU     4574214  4588251   14037   Nea1>Ghost   1853.0     4     0     1
0          5          CEU     6774061  6832111   58050   Nea1>Ghost   1853.0     16    0     2
0          5          CEU     6875101  6878610   3509    Nea1>Ghost   1853.0     1     0     0
0          5          CEU     8029793  8042483   12690   Nea1>Ghost   1853.0     2     0     1
0          5          CEU     8107710  8125727   18017   Nea1>Ghost   1853.0     5     0     3
0          10         YRI     5343820  5348248   4428    Nea1>Ghost   1853.0     2     0     1
0          11         YRI     1966468  1971167   4699    Nea1>Ghost   1853.0     1     0     1
0          11         YRI     7999041  8063034   63993   Nea1>Ghost   1853.0     21    2     3
```


Note please feel free to play around with the parameters in the yaml file and use this for your own simulations.
