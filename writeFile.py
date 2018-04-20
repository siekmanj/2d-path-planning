import pickle

def writeFile(fileName, data):
  #print('Writing to file {}'.format(fileName))
  outputFile = open(fileName, 'wb')
  pickle.dump(data, outputFile)
  outputFile.close()
