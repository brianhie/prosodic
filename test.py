import prosodic as p
t = p.Text('sonnet1.txt')
t.parse(meter='prose_rhythm_iambic_violable')

for a in t.allParses():
    print(a)

for a in t.stats():
    print(a)
