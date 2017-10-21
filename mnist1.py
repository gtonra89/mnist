
import gzip
from PIL import Image
import numpy as np
import os

# Problem 1 

def readLabelsFromFile(filename): # For reading a label file
    # Using "with" for files limits the scope of variables to within the block. No file closing means no forgetting to close = good.
    with gzip.open(filename, 'rb') as f:
        magic = f.read(4) # First 4 bytes = magic number
        magic = int.from_bytes(magic, 'big') # Convert bytes to int format, 'big' = big-endian / most significant byte first
        print("Magic: ", magic)

        # Pointer now at 3 (4th pos)
        numberLabels = f.read(4) # Next 4 bytes = number of items in the file
        numberLabels = int.from_bytes(numberLabels, 'big')
        print("Num of labels: ", numberLabels)

        labelsArray = [f.read(1) for i in range(numberLabels)] # Read file byte by byte and store items in array
        labelsArray = [int.from_bytes(label, 'big') for label in labelsArray] # Overwrite the labels array with ints instead of bytes (same data different format)
    return labelsArray

print("Label Files -------------")
# Pass filenames into the read labels function
trainLabels = readLabelsFromFile('train-labels-idx1-ubyte.gz')
testLabels = readLabelsFromFile('t10k-labels-idx1-ubyte.gz')

def readImagesFromFile(filename): # For reading an image file (not the same structure as a label file)
    with gzip.open(filename, 'rb') as f:
        # Same as label function, read magic number
        magic = f.read(4)
        magic = int.from_bytes(magic, 'big')
        print("Magic: ", magic)

        # Next 4 bytes = number of items (images)
        numberImages = f.read(4)
        numberImages = int.from_bytes(numberImages, 'big')
        print("Num of Images: ", numberImages)

        # Next 4 = number of rows
        numberRows = f.read(4)
        numberRows = int.from_bytes(numberRows, 'big')
        print("Num of Rows: ", numberRows)

        # Next 4 = number of columns
        numCols = f.read(4)
        numCols = int.from_bytes(numCols, 'big')
        print("Num of Cols: ", numCols)

        # Inefficient / Messy Way (but simplest)
        images = []
        for i in range(numberImages):
            rows = []
            for r in range(numberRows):
                cols = []
                for c in range(numCols):
                    cols.append(int.from_bytes(f.read(1), 'big'))
                rows.append(cols) 
            images.append(rows) 
    return images # Return the  array

print()
print("Image Files -------------")
# Pass filenames to read images function
trainImages = readImagesFromFile('train-images-idx3-ubyte.gz')
testImages = readImagesFromFile('t10k-images-idx3-ubyte.gz')


# Problem 2 .

for row in trainImages[2]: # For each row in 3rd image (looks like a 4?)
    for col in row: # For each column in each row
        print('. ' if col<= 127 else '# ', end='') # Output either . or #, end result should look somewhat like a 4
        # Spacing after . and # make output more accurate
    print() # New line for a new row



# Problem 3 

def saveImages(imgType, imNum):

    limit = 1999

    
    if imNum == 0:
        imName, labels, images, filepath = 'test', testLabels, testImages,"PNGs/TestImages/"
        
        directory = os.path.dirname(filepath)

        if not os.path.exists(directory):
            os.makedirs(directory)

    
    if imNum == 1:
        imName, labels, images, filepath = 'train', trainLabels, trainImages, "PNGs/TrainingImages/"
        directory = os.path.dirname(filepath)

        if not os.path.exists(directory):
            os.makedirs(directory)

    print('Saving ' + str(imName) + ' images...')

   
    for index, item in enumerate(imgType):
        label = labels[index]

       
        imfile = filepath + imName + '-' + str(index).zfill(5) + '-' + str(label) + '.png'
        name = imName + '-' + str(index).zfill(5) + '-' + str(label) + '.png'
        print ('saving ' + name + '...')

        img = Image.fromarray(np.array(images[index])*255)  
        img.convert('RGB')
        img.save(imfile, 'PNG')

        print (name + ' saved')

        if index == limit:
            break

    print(str(imName + ' images saved.'))


run = input('Save files as PNGs? y/n ')
if run.lower() == 'y':
    
    filepath = "PNGs/"
    directory = os.path.dirname(filepath)

    if not os.path.exists(directory):
        os.makedirs(directory)

    saveImages(testImages, 0)
    saveImages(trainImages, 1)
