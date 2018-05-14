import sys

from accuracy2 import *

def compare_parses(parse1, parse2):
    if len(parse1) == 0 or len(parse2) == 0:
        return 0, 0
    
    if len(parse1) > len(parse2):
        parse1, parse2 = parse2, parse1

    offset = len(parse2) - len(parse1)
    o_to_correct = {}
    o = 0
    while True:
        n_correct = 0
        for i in range(len(parse1)):
            if parse1[i] == parse2[i + o]:
                n_correct += 1
        o_to_correct[o] = n_correct
        if o == offset:
            break
        o += 1

    max_correct = -1
    for o in o_to_correct:
        if o_to_correct[o] > max_correct:
            max_correct = o_to_correct[o]
    assert(max_correct != -1)

    return max_correct, len(parse2)

def get_accuracy(meter, itad):
    parsed_human = [
        (line.rstrip().split('\t')[1], line.rstrip().split('\t')[2])
        for line in open(itad + '.txt')
    ]
    parsed_human1 = [ ph[0] for ph in parsed_human ]
    parsed_human2 = [ ph[1] for ph in parsed_human ]

    with open('parses/parse_{}_{}.txt'.format(meter, itad)) as f:
        line = '>>'
        while line.startswith('>>'):
            line = f.readline().rstrip()
        header = line

        syl_total1, syl_total2 = 0, 0
        syl_correct1, syl_correct2 = 0, 0
        for idx, line in enumerate(f):
            fields = line.rstrip().split('\t')
            parsed = fields[2]

            correct1, total1 = compare_parses(parsed, parsed_human1[idx])
            correct2, total2 = compare_parses(parsed, parsed_human2[idx])

            syl_correct1 += correct1
            syl_correct2 += correct2
            syl_total1 += total1
            syl_total2 += total2

    return float(syl_correct1) / syl_total1

def parses_to_scores(meter, itad):
    with open('parses/parse_{}_{}.txt'.format(meter, itad)) as f:
        line = '>>'
        while line.startswith('>>'):
            line = f.readline().rstrip()
        header = line

        parsed_score = []
        for idx, line in enumerate(f):
            fields = line.rstrip().split('\t')
            parsed = fields[2]
            score = int(fields[3])
            parsed_score.append((parsed, score))
            
    return parsed_score

def ensemble_accuracy(meter1, meter2, itad, supervised=False):
    parsed_human = [
        (line.rstrip().split('\t')[1], line.rstrip().split('\t')[2])
        for line in open(itad + '.txt')
    ]
    parsed_human1 = [ ph[0] for ph in parsed_human ]
    parsed_human2 = [ ph[1] for ph in parsed_human ]

    parsed_score1 = parses_to_scores(meter1, itad)
    parsed_score2 = parses_to_scores(meter2, itad)
    assert(len(parsed_score1) == len(parsed_score2))

    syl_total1, syl_total2 = 0, 0
    syl_correct1, syl_correct2 = 0, 0
    for idx in range(len(parsed_score1)):
        parsed1 = parsed_score1[idx][0]
        parsed2 = parsed_score2[idx][0]
        score1 = parsed_score1[idx][1]
        score2 = parsed_score2[idx][1]

        if supervised:
            parsed = parsed2 if (itad == 'anapestic' or itad == 'dactylic') else parsed1
        else:
            parsed = parsed2 if score1 > score2 else parsed1

        correct1, total1 = compare_parses(parsed, parsed_human1[idx])
        correct2, total2 = compare_parses(parsed, parsed_human2[idx])

        syl_correct1 += correct1
        syl_correct2 += correct2
        syl_total1 += total1
        syl_total2 += total2

    return float(syl_correct1) / syl_total1

if __name__ == '__main__':
    meters = [
        'litlab',
        'optimized_binary',
        'optimized_ternary',
   ]

    itad = [
        'iambic', 'trochaic', 'anapestic', 'dactylic'
    ]

    for meter in meters:
        print(meter)
        for x in itad:
            accuracy = get_accuracy(meter, x)
            sys.stdout.write(str(accuracy) + '\t')
        sys.stdout.write('\n')

    print('Ensemble supervised')
    for x in itad:
        accuracy = ensemble_accuracy(
            'litlab_footmin2', 'litlab_footminnos2', x
        )
        sys.stdout.write(str(accuracy) + '\t')
    sys.stdout.write('\n')

    print('Ensemble unsupervised')
    for x in itad:
        accuracy = ensemble_accuracy(
            'litlab_footmin2', 'litlab_footminnos2', x
        )
        sys.stdout.write(str(accuracy) + '\t')
    sys.stdout.write('\n')
