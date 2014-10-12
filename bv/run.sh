# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -file ./processTitles.py    -mapper ./processTitles.py \
# -input /data/bazaarvoice/combinedData.updated.csv -output /data/bazaarvoice/output1 \
# -reducer NONE

# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -mapper wc \
# -input /data/bazaarvoice/output1/part-* -output /data/bazaarvoice/output2 \
# -reducer NONE

# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -file ./upcMatcher.py    -mapper ./upcMatcher.py \
# -input /data/bazaarvoice/destination.tsv -output /data/bazaarvoice/output2 \
# -file /home/hadoop/BazaarVoice/source.tsv \
# -reducer NONE

# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -mapper wc \
# -input /data/bazaarvoice/output2/part-* -output /data/bazaarvoice/output3 \
# -reducer NONE

/apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
-file ./codeMatcher.py  \
-mapper ./codeMatcher.py \
-input /data/bazaarvoice/destinationRecords.tsv \
-output /data/bazaarvoice/output1 \
-file /home/hadoop/BazaarVoice/sourceRecords.tsv \
-reducer NONE

# /apps/hadoop/bin/hadoop jar /apps/hadoop/contrib/streaming/hadoop-streaming-2.0.0-mr1-cdh4.2.1.jar \
# -mapper wc \
# -input /data/bazaarvoice/output3/part-* -output /data/bazaarvoice/output4 \
# -reducer NONE
