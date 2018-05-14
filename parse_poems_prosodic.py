import glob
import prosodic as p
import string
import sys

def parse_files(meter, path='*.txt'):
    files = glob.glob(path)
    
    for f in files: 
        terminal_out = sys.stdout
        sys.stdout = open('parses/parse_{}_{}'.format(meter, f), 'w')
    
        printable = set(string.printable)
        file_text = '\n'.join([ line.rstrip().split('\t')[0]
                                for line in open(f, 'r') ])
        file_text = filter(lambda x: x in printable, file_text)
        
        t = p.Text(file_text, meter=meter)
        t.parse()
        t.scansion()
        
        sys.stdout.close()
        sys.stdout = terminal_out

if __name__ == '__main__':
    meters = [
        'litlab',
        'optimized_binary',
        'optimized_ternary',
    ]

    for meter in meters:
        print(meter)
        parse_files(meter)
