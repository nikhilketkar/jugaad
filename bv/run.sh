# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -file /home/hadoop/BazaarVoice/processTitles.py    -mapper /home/hadoop/BazaarVoice/processTitles.py \
# -input /data/bazaarvoice/combinedData.updated.csv -output /data/bazaarvoice/output1 \
# -reducer NONE

/apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
-mapper wc \
-input /data/bazaarvoice/output1/part-* -output /data/bazaarvoice/output2 \
-reducer NONE
