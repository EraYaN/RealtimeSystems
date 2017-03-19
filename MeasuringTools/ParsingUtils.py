import re
import sys
import TraceFile as tf


if len(sys.argv) < 2:
    print('Not enough arguments')
    file = "X:\lab3\wsim_all.raw"
else:
    file = sys.argv[1]

trace = tf.TraceFile(file)


res = trace.get_high_period('intr_num',3)

if res['n'] > 0:
    print('PeriodHigh: t: {} us; n: {}; t/n: {} us'.format(res['t']/1000,res['n'],res['t']/res['n']/1000))
else:
    print('PeriodHigh: No data')

res = trace.get_low_period('intr_num',3)

if res['n'] > 0:
    print('PeriodLow: t: {} us; n: {}; t/n: {} us'.format(res['t']/1000,res['n'],res['t']/res['n']/1000))
else:
    print('PeriodLow: No data')

evt_lat = trace.get_event_latency('blue','intr_num',0,3)

if evt_lat['n'] > 0:
    print('EvtLatYellow: t: {} us; n: {}; t/n: {} us'.format(evt_lat['t']/1000,evt_lat['n'],evt_lat['t']/evt_lat['n']/1000))
else:
    print('EvtLatYellow:No data')

evt_lat = trace.get_event_latency('green','intr_num',0,3)

if evt_lat['n'] > 0:
    print('EvtLatGreen: t: {} us; n: {}; t/n: {} us'.format(evt_lat['t']/1000,evt_lat['n'],evt_lat['t']/evt_lat['n']/1000))
else:
    print('EvtLatGreen:No data')
