path_source0=../data/vpalog_token/2020
path_target0=data_vpa_dialogue/
L0=(04 04 04 05 05)
L1=(26 28 30 02 04)
H=(00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23)
n=1
for((i=0;i<6;i++))
do
for((j=0;j<24;j++))
do
pathsource=$path_source0${L0[$i]}${L1[$i]}${H[$j]}.txt
pathtarget=$path_target0${L0[$i]}${L1[$i]}${H[$j]}.txt
split -b 100m $pathtarget data_vpa_dialogue1/$pathtarget
done
done