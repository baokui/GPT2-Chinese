hadoopclients=ml_research,3evrqV2R
for((i=0;i<10;i++))
do
hadoop fs -Dhadoop.client.ugi=$hadoopclients -get VpaOutput_guobk/dabaigou_train/202001/000$i data/202001/
done