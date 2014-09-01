import sys

def url2Store(url):
    return url.split('/')[2]

def reader(filename):
    header = ['Url', 'PromotionFrequencyScore', 'PromotionMagnitudeScore','PromotionDurationScore',
              'PriceChangeFrequencyScore', 'PriceChangeMagnitudeScore', 'BrandScore', 'StoreScore',
              'NoOfTimesAvailableScore', 'NoOfStoresScore']
    with open(filename) as inputFile:
        for line in inputFile:
            words = line.split('\t')
            record = {}
            for i in xrange(0, len(header)):
                if i == 0:
                    record[header[i]] = float(words[i])
                else:
                    record[header[i]] = words[i]
            record["Store"] = url2Store(record['Url'])
            yield record














