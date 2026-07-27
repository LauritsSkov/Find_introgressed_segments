import msprime
from collections import defaultdict
import demes
import demesdraw
import matplotlib.pyplot as plt
import argparse
import numpy as np 
import json 

# -----------------------------------------------------------------------------------------------------
# Parameters for demography (plot with demes)
# -----------------------------------------------------------------------------------------------------

def get_introgressed_segments(ts):
    """
    Optimized version: loops through trees once and processes overlapping migrations.
    """

    pop_to_number = {x.metadata['name']: x.id for x in ts.populations()}
    number_to_pop = {x.id: x.metadata['name'] for x in ts.populations()}

    excluded_times = defaultdict(lambda: ['None',['None']])
    for event in demography.events:
        if type(event) == msprime.demography.PopulationSplit:
            derived_pop = event.derived
            ancestral_pop = event.ancestral
            excluded_times[event.time] = [event.derived, event.ancestral]


    sample_to_pop = defaultdict(str)
    for pop in ts.populations():
        for sample in ts.get_samples(pop.id):
            sample_to_pop[sample] = pop.metadata['name']

    introgressed_seg = defaultdict(list)

    # ---- 1. collect relevant migrations ----
    mig_events = []

    for mr in ts.migrations():
        if number_to_pop[mr.source] in excluded_times[mr.time][0] and number_to_pop[mr.dest] == excluded_times[mr.time][1]:
            continue

        mig_events.append(mr)

    # sort by left coordinate
    mig_events.sort(key=lambda m: m.left)

    mig_idx = 0
    active_migs = []

    # ---- 2. single pass through trees ----
    for tree in ts.trees(leaf_lists=True):
        tree_left, tree_right = map(int, tree.interval)

        # add migrations that start before this tree ends
        while mig_idx < len(mig_events) and mig_events[mig_idx].left < tree_right:
            active_migs.append(mig_events[mig_idx])
            mig_idx += 1

        # remove migrations that end before this tree starts
        active_migs = [
            mr for mr in active_migs if mr.right > tree_left
        ]

        if not active_migs:
            continue

        # ---- 3. process overlapping migrations ----
        for mr in active_migs:
            from_pop = number_to_pop[mr.dest]
            into_pop = number_to_pop[mr.source]
            time = round(mr.time,1)
            admixinfo = f'{from_pop}|{into_pop}|{time}'

            # descendant leaves of the migrant node
            leaves = [x for x in tree.leaves(mr.node)]

            for l in leaves:
                #if l in Testpopulation:
                introgressed_seg[l, admixinfo].append([tree_left, tree_right])

    
    def merge_overlapping(temp_tuple):
        temp_tuple.sort(key=lambda interval: interval[0])
        merged = [temp_tuple[0]]

        for current in temp_tuple:
            previous = merged[-1]
            if current[0] <= previous[1]:
                previous[1] = max(previous[1], current[1])
            else:
                merged.append(current)

        return merged
    

    merged_introgressed_segs = []
    for (haplotype, admix_event), segments in introgressed_seg.items():
        from_pop, to_pop, admixtime = admix_event.split('|')
        for start, end in merge_overlapping(segments):
            merged_introgressed_segs.append((haplotype, sample_to_pop[haplotype], start, end, f'{from_pop}>{to_pop}', admixtime))

    return sorted(merged_introgressed_segs)




# -----------------------------------------------------------------------------------------------------
# Parameters for demography (plot with demes)
# -----------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-demography",  help="File with demography", type=str, required=True)
parser.add_argument("-samples",  help="Which individuals to sample", type=str, required=True)
parser.add_argument("-outfile",  help="outplot name", type=str, default = '/dev/stdout')
parser.add_argument("-printdemography", help='print demography and save to pdf', type=str, default = '')
parser.add_argument("-seed",  help="outplot name", type=int, default = 1234)
parser.add_argument("-iterations",  help="number of independent iterations", type=int, default = 1)

parser.add_argument("-genomesize",  help="outplot name", type=int, default = 10_000_000)
parser.add_argument("-mutation_rate",  help="outplot name", type=float, default = 1.45e-8)
parser.add_argument("-recombination_rate",  help="outplot name", type=float, default = 1.45e-8)

parser.add_argument("-extrainfo", help='print snp positions and ages', action='store_true', default = False)
parser.add_argument("-keepevents", help='filter events', type=str, default = '')

args = parser.parse_args()

# Plot demography
graph = demes.load(args.demography)
demography = msprime.Demography.from_demes(graph)

if args.printdemography != '':
    fig, ax = plt.subplots()  
    demesdraw.tubes(graph, ax=ax, seed=1)
    plt.tight_layout()
    plt.savefig(args.printdemography)


# Sample information
with open(args.samples) as json_file:
    data = json.load(json_file)

SAMPLES = []
INGROUP_GENOME_SAMPLES = []
ARCHAIC_GENOME_SAMPLES = []
OUTGROUP_GENOME_SAMPLES = []

for population_function, pop_to_sample in data.items():

    for pop in pop_to_sample:

        if population_function == 'Sequenced_Archaics' and pop['population'] not in ARCHAIC_GENOME_SAMPLES:
            ARCHAIC_GENOME_SAMPLES.append(pop['population'])

        if population_function == 'Ingroup' and pop['population'] not in INGROUP_GENOME_SAMPLES:
            INGROUP_GENOME_SAMPLES.append(pop['population'])

        if population_function == 'Outgroup' and pop['population'] not in OUTGROUP_GENOME_SAMPLES:
            OUTGROUP_GENOME_SAMPLES.append(pop['population'])

        SAMPLES.append(msprime.SampleSet(num_samples=pop['num_samples'], 
                                         population=pop['population'], 
                                         time=pop['time'], 
                                         ploidy=pop['ploidy']))

# remove really deep coal times
max_time = 0
for event in demography.events:
    if type(event) == msprime.demography.PopulationSplit:
        if event.ancestral in OUTGROUP_GENOME_SAMPLES and event.time > max_time:
            max_time = event.time


# seach for some admixture events only
if args.keepevents != '':
    keywords = [x for x in args.keepevents.split(',')]
else:
    keywords = ['']


with open(args.outfile, 'w') as out:

    HEADER = ['iteration', 'haplotype', 'pop', 'start', 'end','length', 'admix_event', 'admixtime', 'snps', '\t'.join(ARCHAIC_GENOME_SAMPLES)]
    if args.extrainfo:
        HEADER += ['snp_positions', 'snp_ages' , 'matches']

    print(*HEADER, sep = '\t', file = out)

    for iteration in range(args.iterations):

        # Simulate
        ts = msprime.sim_ancestry(
            samples=SAMPLES, 
            demography=demography,
            sequence_length=args.genomesize,
            recombination_rate=args.recombination_rate,
            record_migrations=True,
            random_seed=iteration + args.seed)

        introgressed_segments = get_introgressed_segments(ts)
        introgressed_segments_dict = defaultdict(int)
        introgressed_snp_ages = defaultdict(list)

        Individuals_from_pop = defaultdict(list)
        for pop in ts.populations():
            Individuals_from_pop[pop.metadata['name']] = ts.get_samples(pop.id)

        mts = msprime.sim_mutations(ts, rate=args.mutation_rate, random_seed=args.seed)

        # sort by left coordinate
        introgressed_segments.sort(key=lambda x: x[2])

        intro_segment_idx = 0
        overlapping_introgressed_segmets = []

        for var in mts.variants():

            snp_time = var.site.mutations[0].time
            if snp_time > max_time: 
                continue 

            pos = int(var.site.position)

            # add migrations that start before this tree ends
            while intro_segment_idx < len(introgressed_segments) and introgressed_segments[intro_segment_idx][2] < pos:
                overlapping_introgressed_segmets.append(introgressed_segments[intro_segment_idx])
                intro_segment_idx += 1

            # remove migrations that end before this tree starts
            overlapping_introgressed_segmets = [x for x in overlapping_introgressed_segmets if x[3] > pos]

            if not overlapping_introgressed_segmets:
                continue

            archaic_match_rates = {x: np.sum(var.genotypes[Individuals_from_pop[x]]) for x in ARCHAIC_GENOME_SAMPLES}

            for (haplotype, pop, start, end,  admix_event, admixtime) in overlapping_introgressed_segmets:

                if var.genotypes[haplotype] == 0:
                    continue

                #print(haplotype, pop, start, end,  admix_event, admixtime)
                ID = f'{haplotype}|{pop}|{admix_event}|{admixtime}|{start}|{end}'
                

                which_archaic_matches = []

                for seq_arch in ARCHAIC_GENOME_SAMPLES:
                    if archaic_match_rates[seq_arch] > 0:
                        introgressed_segments_dict[ID, seq_arch] += 1
                        which_archaic_matches.append(seq_arch)

                if which_archaic_matches:
                    which_archaic_matches = '|'.join(which_archaic_matches)
                else:
                    which_archaic_matches = 'none'


                introgressed_segments_dict[ID, 'snps'] += 1
                introgressed_snp_ages[ID, 'snp_ages'].append(str(int(snp_time)))
                introgressed_snp_ages[ID, 'snp_positions'].append(str(pos))
                introgressed_snp_ages[ID, 'match'].append(which_archaic_matches)


        introgressed_segments.sort(key=lambda x: (x[0], x[2]))
        for (haplotype, pop, start, end,  admix_event, admixtime) in introgressed_segments:
            

            OUTPUT = [haplotype, pop, start, end,  admix_event, admixtime]
            ID = f'{haplotype}|{pop}|{admix_event}|{admixtime}|{start}|{end}'
            
            snps = introgressed_segments_dict[ID, 'snps']
            shared = [str(introgressed_segments_dict[ID, seq_arch]) for seq_arch in ARCHAIC_GENOME_SAMPLES]
            OUTPUT += [snps, '\t'.join(shared)]

            if args.extrainfo:
                snp_ages = ','.join([x for x in introgressed_snp_ages[ID, 'snp_ages']])
                snp_position = ','.join([x for x in introgressed_snp_ages[ID, 'snp_positions']])
                matches = ','.join([x for x in introgressed_snp_ages[ID, 'match']])

                OUTPUT += [snp_position, snp_ages, matches]

            if any([keyword in admix_event for keyword in keywords]):
                print(*OUTPUT, sep = '\t', file = out)



