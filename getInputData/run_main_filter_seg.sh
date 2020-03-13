mkdir log
Month=202002
for((k=0;k<4;k++))
do
    for((i=0;i<9;i++))
    do
        idx=$k$i
        input=zhangfeixue/shurufa/st_data/$Month/00$idx*
        output=VpaOutput_guobk/dabaigou_train_filter_seg/$Month/00$idx
        nohup sh run_join_filter_seg.sh $input $output >> log/filter-seg-$Month-00$idx-.log 2>&1 &
        echo $input
    done
    i=9
    idx=$k$i
    input=zhangfeixue/shurufa/st_data/$Month/00$idx*
    output=VpaOutput_guobk/dabaigou_train_filter_seg/$Month/00$idx
    nohup sh run_join_filter_seg.sh $input $output >> log/filter-seg-$Month-00$idx-.log 2>&1
    echo $input
done
