'''data.py
Reads CSV files, stores data, access/filter data by variable name
Emerson Wright
CS 251 Data Analysis and Visualization
Spring 2021

Reusing 
Emerson Wright
MSU REU Grumstrup Group
Summer 2021
'''
import numpy as np

class Data:
    def __init__(self, filepath=None, headers=None, data=None, header2col=None):
        '''Data object constructor

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file
        headers: Python list of strings or None. List of strings that explain the name of each
            column of data.
        data: ndarray or None. shape=(N, M).
            N is the number of data samples (rows) in the dataset and M is the number of variables
            (cols) in the dataset.
            2D numpy array of the dataset’s values, all formatted as floats.
            NOTE: In Week 1, don't worry working with ndarrays yet. Assume it will be passed in
                  as None for now.
        header2col: Python dictionary or None.
                Maps header (var str name) to column index (int).
                Example: "sepal_length" -> 0
        '''
        #Assigning Feilds
        self.filepath = filepath
        self.headers = headers
        self.data = data
        self.header2col = header2col
        self.label = ""

        #Reading in file if there is one
        if self.filepath != None:
            self.read(self.filepath)

        return

    def read(self, filepath):
        '''Read in the .csv file `filepath` in 2D tabular format. Convert to numpy ndarray called
        `self.data` at the end (think of this as 2D array or table).

        Format of `self.data`:
            Rows should correspond to i-th data sample.
            Cols should correspond to j-th variable / feature.

        Parameters:
        -----------
        filepath: str or None. Path to data .csv file

        Returns:
        -----------
        None. (No return value).
            NOTE: In the future, the Returns section will be omitted from docstrings if
            there should be nothing returned

        TODO:
        - Read in the .csv file `filepath` to set `self.data`. Parse the file to only store
        numeric columns of data in a 2D tabular format (ignore non-numeric ones). Make sure
        everything that you add is a float.
        - Represent `self.data` (after parsing your CSV file) as an numpy ndarray. To do this:
            - At the top of this file write: import numpy as np
            - Add this code before this method ends: self.data = np.array(self.data)
        - Be sure to fill in the fields: `self.headers`, `self.data`, `self.header2col`.

        NOTE: You may wish to leverage Python's built-in csv module. Check out the documentation here:
        https://docs.python.org/3/library/csv.html

        NOTE: In any CS251 project, you are welcome to create as many helper methods as you'd like.
        The crucial thing is to make sure that the provided method signatures work as advertised.

        NOTE: You should only use the basic Python library to do your parsing.
        (i.e. no Numpy or imports other than csv).
        Points will be taken off otherwise.

        TIPS:
        - If you're unsure of the data format, open up one of the provided CSV files in a text editor
        or check the project website for some guidelines.
        - Check out the test scripts for the desired outputs.
        '''
        #Opening file
        try:
            file = open(filepath, "r")
        except:
            print("Could not read file, please check file path")
            exit()

        self.filepath = filepath
    
        #Reading in headers
        tempHeaders = file.readline().split(",")
        #removing \n from end of the line
        tempHeaders[-1] = tempHeaders[-1][0:-1]
        self.headers = []
        self.header2col = {}
        types = file.readline().split(",")
        #removing \n from end of the line
        types[-1] = types[-1][0:-1]
        #Checking to make sure types are valid
        typesRef = ["numeric", "enum", "date", "string"]
        for t in types:
            if t.strip().lower() not in typesRef:
                print(t)
                print("Error reading types, second line of csv should contain type lables: numeric, enums, string, date")
                exit()

        rawIDX = 0
        dataIDX = 0
        numericIDXs = []
        for rawIDX in range(len(tempHeaders)):
            if types[rawIDX].lower().strip() == "numeric":
                self.headers.append(tempHeaders[rawIDX].strip().lower())
                self.header2col[tempHeaders[rawIDX].strip().lower()] = dataIDX
                numericIDXs.append(rawIDX)
                dataIDX += 1

        #Reading in Data
        line = file.readline()
        tempData = []
        tempRow = []
        while len(line) != 0:
            nums = line.split(",")
            #removing the \n
            nums[-1] = nums[-1][0:-1]
            for i in numericIDXs:
                tempRow.append(nums[i])
            tempData.append(tempRow.copy())
            tempRow.clear()
            line = file.readline()

        #Converting data to nparray
        
        
        self.data = np.array(tempData, np.float)
        return

    def __str__(self):
        '''toString method

        (For those who don't know, __str__ works like toString in Java...In this case, it's what's
        called to determine what gets shown when a `Data` object is printed.)

        Returns:
        -----------
        str. A nicely formatted string representation of the data in this Data object.
            Only show, at most, the 1st 5 rows of data
            See the test code for an example output.
        '''
        masterSTR = ""
        #Number of lines displayed
        numLines = 5
        #checking to make sure there are enough lines
        if self.data.shape[0] < numLines:
            numLines = self.data.shape[0]
            print("changed num lines")
            for i in range(numLines):
                print(i)

        masterSTR += "-------------------------------\n"
        masterSTR += f"data/iris.csv ({self.data.shape[0]}x{self.data.shape[1]})\n"
        masterSTR += "Headers:\n"
        headersSTR = "   "
        for h in self.headers:
            headersSTR += h + "     "
        masterSTR += headersSTR + "\n"
        masterSTR += "-------------------------------\n"
        masterSTR += f"Showing first {numLines}/{self.data.shape[0]} rows\n"
        dataSTR = ""
        for l in range(numLines):
            for k in range(self.data.shape[1]):
                dataSTR += str(self.data[l][k])
                for i in range(7 - len(str(self.data[l][k]))):
                    dataSTR += " "
            dataSTR += "\n"
        masterSTR += dataSTR
        masterSTR += "-------------------------------\n"
        return masterSTR

    def get_headers(self):
        '''Get method for headers

        Returns:
        -----------
        Python list of str.
        '''
        return self.headers

    def get_label(self):
        return self.label

    def get_mappings(self):
        '''Get method for mapping between variable name and column index

        Returns:
        -----------
        Python dictionary. str -> int
        '''
        return self.header2col

    def get_num_dims(self):
        '''Get method for number of dimensions in each data sample

        Returns:
        -----------
        int. Number of dimensions in each data sample. Same thing as number of variables.
        '''
        return len(self.headers)

    def get_num_samples(self):
        '''Get method for number of data points (samples) in the dataset

        Returns:
        -----------
        int. Number of data samples in dataset.
        '''
        return self.data.shape[0]

    def get_sample(self, rowInd):
        '''Gets the data sample at index `rowInd` (the `rowInd`-th sample)

        Returns:
        -----------
        ndarray. shape=(num_vars,) The data sample at index `rowInd`
        '''
        return self.data[rowInd]

    def get_header_indices(self, headers):
        '''Gets the variable (column) indices of the str variable names in `headers`.

        Parameters:
        -----------
        headers: Python list of str. Header names to take from self.data

        Returns:
        -----------
        Python list of nonnegative ints. shape=len(headers). The indices of the headers in `headers`
            list.
        '''
        idx = []
        for h in headers:
            try:
                idx.append(self.header2col[h])
            except:
                print("invalid header search")
                exit

        return idx

    def get_all_data(self):
        '''Gets a copy of the entire dataset

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(num_data_samps, num_vars). A copy of the entire dataset.
            NOTE: This should be a COPY, not the data stored here itself.
            This can be accomplished with numpy's copy function.
        '''
        return self.data.copy()

    def head(self):
        '''Return the 1st five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). 1st five data samples.
        '''
        return self.data[:5,:].copy()

    def tail(self):
        '''Return the last five data samples (all variables)

        (Week 2)

        Returns:
        -----------
        ndarray. shape=(5, num_vars). Last five data samples.
        '''
        return self.data[-5:, :].copy()

    def limit_samples(self, start_row, end_row):
        '''Update the data so that this `Data` object only stores samples in the contiguous range:
            `start_row` (inclusive), end_row (exclusive)
        Samples outside the specified range are no longer stored.

        (Week 2)

        '''
        self.data = self.data[start_row:end_row, :]
        return

    def select_data(self, headers, rows=[]):
        '''Return data samples corresponding to the variable names in `headers`.
        If `rows` is empty, return all samples, otherwise return samples at the indices specified
        by the `rows` list.

        (Week 2)

        For example, if self.headers = ['a', 'b', 'c'] and we pass in header = 'b', we return
        column #2 of self.data. If rows is not [] (say =[0, 2, 5]), then we do the same thing,
        but only return rows 0, 2, and 5 of column #2.

        Parameters:
        -----------
            headers: Python list of str. Header names to take from self.data
            rows: Python list of int. Indices of subset of data samples to select.
                Empty list [] means take all rows

        Returns:
        -----------
        ndarray. shape=(num_data_samps, len(headers)) if rows=[]
                 shape=(len(rows), len(headers)) otherwise
            Subset of data from the variables `headers` that have row indices `rows`.

        Hint: For selecting a subset of rows from the data ndarray, check out np.ix_
        '''
        #Getting the indices for the headers needed
        dataNeeded = []
        if type(headers) != str:
            for h in headers:
                dataNeeded.append(self.header2col[h])

            #Returnign either all the data or the requested data
            #NOTE: Data will be returned in the order of the headers in the parameters, not self.data
            if rows == []:
                return self.data[:,dataNeeded].copy()
            else:
                return self.data[np.ix_(rows,dataNeeded)].copy()
        else:
            #If only one header is passed
            if rows == []:
                return self.data[:,self.header2col[headers]].copy()
            else:
                return self.data[np.ix_(rows,self.header2col[headers])].copy()