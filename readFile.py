import pickle

def readFile(fileName):
  #print('Reading from file {}'.format(fileName))
  inputFile = open(fileName, 'rb')
  data = pickle.load(inputFile)
  inputFile.close()
  return data
