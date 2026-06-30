import msprime
from collections import defaultdict
import demes
import demesdraw
import matplotlib.pyplot as plt
import argparse
import numpy as np 

# -----------------------------------------------------------------------------------------------------
# Parameters for demography (plot with demes)
# -----------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("-demography", metavar='',help="File with demography", type=str, required=True)
parser.add_argument("-outfile", metavar='',help="outplot name", type=str, default = '/dev/stdout')

args = parser.parse_args()


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

graph = demes.load(args.demography)
demography = msprime.Demography.from_demes(graph)



# Plot demography
fig, ax = plt.subplots()  
demesdraw.tubes(graph, ax=ax, seed=1)
plt.tight_layout()
plt.savefig('Demography.pdf')


SAMPLES = {}
SAMPLES['NonAfrican'] = 1
for population_name in demography:
    if population_name.startswith('Seq_'):
        SAMPLES[population_name] = 1





CHROM_SIZE = 10_000_000
gen_time = 29.0 
rec_rate = 1.45e-8
mutation_rate = 1.45e-8

with open(args.outfile, 'w') as out:
    print('iteration', 'haplotype', 'pop', 'start', 'end','length', 'admix_event', 'admixtime', 'snps', 'shared', sep = '\t', file = out)

    for iteration in range(1):

        print(iteration)

        # Simulate
        ts = msprime.sim_ancestry(
            samples=SAMPLES, 
            demography=demography,
            sequence_length=CHROM_SIZE,
            recombination_rate=rec_rate,
            record_migrations=True,
            random_seed=iteration + 1)

        introgressed_segments = get_introgressed_segments(ts)
        introgressed_segments_temp = defaultdict(int)

        mts = msprime.sim_mutations(ts, rate=mutation_rate, random_seed=1234)

        for var in mts.variants():
            
            snp_time = var.site.mutations[0].time
            if snp_time < 45000/gen_time or snp_time > 575000/gen_time:
                continue 

            ingroup = var.genotypes[0:2]
            if np.sum(ingroup) == 0:
                continue


            pos = int(var.site.position)
            archaic = np.sum(var.genotypes[2:])

            #print(pos, ingroup, archaic, var.genotypes)
            for haplotype_genotype_matrix, genotype in enumerate(ingroup):

                if genotype == 0:
                    continue

                
                for (haplotype, pop, start, end,  admix_event, admixtime) in introgressed_segments:
                    if haplotype == haplotype_genotype_matrix and start < pos < end:
                        ID = f'{haplotype}|{pop}|{start}|{end}'
                        introgressed_segments_temp[ID, 'snps'] += 1
                        
                        if archaic > 0:
                            introgressed_segments_temp[ID, 'archaic'] += 1
                            

            
            
        for (haplotype, pop, start, end,  admix_event, admixtime) in introgressed_segments:
            ID = f'{haplotype}|{pop}|{start}|{end}'
            snps = introgressed_segments_temp[ID, 'snps']
            shared = introgressed_segments_temp[ID, 'archaic']
            
            print(iteration, haplotype, pop, start, end, end-start, admix_event, admixtime, snps, shared, sep = '\t', file = out)



