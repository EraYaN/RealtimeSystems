import re
import sys


if len(sys.argv) < 2:
    print('Not enough arguments')
    file = "X:\lab2\wsim_intr_num.raw"
else:
    file = sys.argv[1]

period = 0
number_of_periods = 0
prog = re.compile('([0-9]+)\s?:\s?([0-9+])')
last_was_high = False
last_timestamp = 0
last_value = 0
with open(file, 'r',encoding='utf-8',newline=None) as f:
    for line in f:
        match = prog.search(line)
        if match:
            timestamp = int(match.group(1))
            value = int(match.group(2))
            if value == 0 and last_was_high:
                period += ( timestamp - last_timestamp )
                number_of_periods+=1
            last_was_high = (value > 0)
            last_value = value
            last_timestamp = timestamp
        else:
            pass
            #print('Skipped line: {}'.format(line))
       

    if number_of_periods > 0:
        print('total time: {} ns; periods: {}; time per period: {} ns'.format(period,number_of_periods,period/number_of_periods))
    else:
        print('No data')
        