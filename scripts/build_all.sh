make
wsim-iclbsn2 --ui --trace=sched.trc --mode=time --modearg=5s SchedTest.elf
wtracer --in=sched.trc --out=wsim.vcd --format=vcd
gtkwave wsim.vcd