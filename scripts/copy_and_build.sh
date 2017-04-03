#!/bin/bash

rm -rf /mnt/rts_vm/lab1
mkdir /mnt/rts_vm/lab1
cp ../Lab1/*.c /mnt/rts_vm/lab1
cp ../Lab1/*.h /mnt/rts_vm/lab1
cp ../Lab1/Makefile /mnt/rts_vm/lab1

# ssh wasp@192.168.56.102 make -C ~/lab1


# ssh wasp@192.168.56.102:~/lab1 make
# ssh wasp@192.168.56.102 cd ~/lab1 && wsim-iclbsn2 --ui --trace=sched.trc --mode=time --modearg=5s SchedTest.elf
# ssh wasp@192.168.56.102 cd ~/lab1 && wtracer --in=sched.trc --out=wsim.vcd --format=vcd

#gtkwave wsim.vcd