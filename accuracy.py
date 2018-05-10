
def compare_parses(parse1, parse2):
    if len(parse1) > len(parse2):
        parse1, parse2 = parse2, parse1
        
    offset = len(parse2) - len(parse1)
    o_to_correct = {}
    for o in range(offset):
        n_correct = 0
        for i in range(len(parse1)):
            if parse1[i + o] == parse2[i]:
                n_correct += 1
        o_to_correct[o] = n_correct

    max_correct = -1
    for o in o_to_correct:
        if o_to_correct[o] > max_correct:
            max_correct = o_to_correct[o]

    return max_correct, len(parse1)

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

if __name__ == '__main__':
    meters = [
        'kiparskyhanson_hopkins',
        'kiparskyhanson_shakespeare',
        'litlab',
        'meter_arto',
        'prose_rhythm_iambic',
        'prose_rhythm_iambic_inviolable',
        'prose_rhythm_iambic_violable',
    ]

    itad = [
        'iambic', 'trochaic', 'anapestic', 'dactylic'
    ]

    for meter in meters:
        for x in itad:
            accuracy = get_accuracy(meter, x)
            print(accuracy)
