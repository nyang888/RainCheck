# Import necessary libraries
from scipy import stats
import csv
import numpy

# Define constants
TOTAL_ELEMENTS = 391109
MAX_DEPARTMENTS = 99
LIN_REG_ELEMENTS = 5

# Prepare files to read/write
iFile = open('Output.csv', "r")
oFile = open('LinReg.csv', "w")
csvReader = list(csv.reader(iFile))
writer = csv.writer(oFile, delimiter=',', quotechar='"', lineterminator = '\n', quoting=csv.QUOTE_NONNUMERIC)

# Initialize empty arrays to store number of elements as well as linReg line
numElements = numpy.zeros(shape=(MAX_DEPARTMENTS), dtype=int) 
linReg = numpy.zeros(shape=(MAX_DEPARTMENTS, LIN_REG_ELEMENTS), dtype=float)
        
# Populate numElements with the number of elements in 'row' store 'col' department
isFirstLine = True
for element in csvReader:
    if isFirstLine == True:
        isFirstLine = False
    else:
        index = int(float(element[1]))
        numElements[index-1] += 1

# Calculate linReg[0]=slope, [1]=intercept, [2]=r-val, [3]=p-val, [4]=stdErr
department = 0
while department<99:
    sales = numpy.zeros(shape=(numElements[department]), dtype=float)
    temp = numpy.zeros(shape=(numElements[department]), dtype=float)
    index = 0
    isFirstLine = True
    for row in csvReader:
        if isFirstLine == True:
            isFirstLine = False
        elif (department+1)==int(float(row[1])):
            sales[index] = float(row[3])
            temp[index] = float(row[4])
            index += 1
    if index != 0:
        linReg[department, 0], linReg[department, 1], linReg[department, 2], linReg[department, 3], linReg[department, 4] = stats.linregress(temp, sales)       
    # Make sure it is running properly
    # print(str(linReg[department,1])+"+"+str(linReg[department,0])+"x")
    department += 1

# Write linReg lines to file
department = 0
writer.writerow(["Dept", "NumPoints", "Slope", "Intercept", "R-Val", "P-Val", "StdError"])
while department<99:
    writer.writerow([str(department+1), numElements[department], linReg[department, 0], linReg[department, 1], linReg[department, 2], linReg[department, 3], linReg[department, 4]])
    department += 1

# Complete Program
iFile.close
oFile.close
print("Done")