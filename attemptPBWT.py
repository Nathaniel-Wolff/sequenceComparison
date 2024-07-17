import numpy
"""Collaborating Note: Aiden Dempsey and I worked on P4 together. """

"""The following uses Python to challenge you to create an algorithm for finding
matches between a set of aligned strings. Minimal familiarity with Python is 
necessary, notably list and Numpy array slicing. 

Do read the accompanying Durbin et al. paper before attempting the challenge!
"""

"""Problem 1.

Let X be a list of M binary strings (over the alphabet { 0, 1 }) each of length 
N. 

For integer 0<=i<=N we define an ith prefix sort as a lexicographic sort 
(here 0 precedes 1) of the set of ith prefixes: { x[:i] | x in X }.
Similarly an ith reverse prefix sort is a lexicographic sort of the set of
ith prefixes after each prefix is reversed.

Let A be an Mx(N+1) matrix such that for all 0<=i<M, 0<=j<=N, A[i,j] is the 
index in X of the ith string ordered by jth reverse prefix. To break ties 
(equal prefixes) the ordering of the strings in X is used. 

Complete code for the following function that computes A for a given X.

Here X is a Python list of Python strings. 
To represent A we use a 2D Numpy integer array.

Example:

>>> X = getRandomX() #This is in the challenge1UnitTest.py file
>>> X
['110', '000', '001', '010', '100', '001', '100'] #Binary strings, M=7 and N=3
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> 

Hint:
Column j (0 < j <= N) of the matrix can be constructed from column j-1 and the 
symbol in each sequence at index j-1.  

Question 1: In terms of M and N what is the asymptotic cost of your algorithm?

Is it O(NM). 
"""

def constructReversePrefixSortMatrix(X):
    #Creates the Mx(N+1) matrix
    M = len(X)
    N = len(X[0])
    A = numpy.empty(shape=[len(X), 1 if len(X) == 0 else len(X[0])+1 ], dtype=int)

    #M columns; each column represents a specific prefix end of each Xi in X for 0<=j=<N
    #N+1 rows; each row represnts a specific sequence xi in x for 0<=i<=M

    #initializing matrix with
    # constructing the first column on its own using position in X
    for xIndex in range(0, len(X)):
        A[xIndex][0] = xIndex

    #iterating through all the columns
    #building column j from j-1
    for j in range(1, N+1):

        #constructing all of the symbol, ordering in previous column tuples
        #each of them is sorted by the reverse prefix, which in this case, is just X[i]

        #building a ones list and a zeroes list
        currentZeroes = []
        currentOnes = []

        for i in range(0, M):
            #getting the previous column's value (at j-1) and iterating through it, in its order (STABLE SORT)
            #Reminder: this is which Xi...in the order found in the last column
            previousColumnValue = A[i][j-1]

            #getting the actual string that corresponds to Xi from X
            #Then, getting its symbol at j
            currentSymbol = X[previousColumnValue][j-1]

            #checking if the symbol is 0 or 1 and saving it to the appropriate list
            if currentSymbol == "0":
                currentZeroes.append(previousColumnValue)
            if currentSymbol == "1":
                currentOnes.append(previousColumnValue)
        #concatenating both lists as the proper order
        order = currentZeroes + currentOnes

        #saving the order to column j, for use in making the next one
        for i in range(0,M):
            A[i][j]=order[i]

    return A

"""Problem 2: 

Following on from the previous problem, let Y be the MxN matrix such that for 
all 0 <= i < M, 0 <= j < N, Y[i,j] = X[A[i,j]][j].

Complete the following to construct Y for X. 

Hint: You can either use your solution to constructReversePrefixSortMatrix() 
or adapt the code from that algorithm to create Y without using 
constructReversePrefixSortMatrix().

Question 2: In terms of M and N what is the asymptotic cost of your algorithm?

It is O(NM). 

"""
def constructYFromX(X):
    #Creates the MxN matrix
    Y = numpy.empty(shape=[len(X), 0 if len(X) == 0 else len(X[0]) ], dtype=str)
    M = len(X)
    N = len(X[0])

    #generating the reversePrefixSortMatrix using the previous function
    #can be queried by i,j
    A = constructReversePrefixSortMatrix(X)

    #mapping values of oldMatrix to the new matrix
    #It actually contains the symbol of X in the proper sort order, as opposed to just the Xi
    #Doesn't save the first row empty string 
    for j in range(0, N):
        #iterating over each column
        #iterating over all the xis
        for i in range(0, M):
            Xi = X[A[i][j]]
            jthCharacter = Xi[j]
            Y[i][j] = jthCharacter

    return Y

"""Problem 3.

Y is a transformation of X. Complete the following to construct X from Y, 
returning X as a list of strings as defined in problem 1.
Hint: This is the inverse of X to Y, but the code may look very similar.

Question 3a: In terms of M and N what is the asymptotic cost of your algorithm?
This one is O(NM^2) 

Question 3b: What could you use Y for? 
Hint: consider the BWT.

Y could be used to get the BWT for each sequence in X, since each row gives the BWT for the Xi at the corresponding position in the unsorted X. 

Question 3c: Can you come up with a more efficient data structure for storing Y?
Y could be stored as a single array that contains only the index, in the unsorted X, of the full string in order of reverse prefix. 

"""
def constructXFromY(X, A, Y):
    #Creates the MxN matrix
    X = numpy.empty(shape=[len(X), 0 if len(X) == 0 else len(X[0]) ], dtype=int)
    N = len(X[0])
    M = len(X)
    #Code to write - you're free to define extra functions
    #(inline or outside of this function) if you like.

    ## (1) Build the first column of A (i.e. [ i for i in range(M) ], call it A_0
    A0 = [i for i in range(0, len(X))]
    #print(A0)

    ## (2) For each column I, 0 through N (exclusive)
	## (3) Use A_i and Y_i to build X_i

    ## (4) Use A_i and Y_i to build A_i+1, the intuition here is that the entries in Y_i are all
    # that is needed to resort A_i to make A_i+1

    #I did it the other way around ^
    #collecting all of the characters in Xi order from Ai and Yi
    allOrderedCharacters = []
    for j in range(0, N):
        orderedCharacters = []
        symbolAiTuples = sorted( [ (A[i][j],Y[i][j]) for i in range(0,M) ], key = lambda x: x[0])
        for i in range(0, M):
            aTuple = symbolAiTuples[i]
            orderedCharacters.append(aTuple[1])
        allOrderedCharacters.append(orderedCharacters)

    #forming each Xi
    reformedX = []
    for i in range(0, M):
        Xi = ""
        for row in allOrderedCharacters:
            Xi += row[i]
        reformedX.append(Xi)

    return reformedX

"""Problem 4.

Define the common suffix of two strings to be the maximum length suffix shared 
by both strings, e.g. for "10110" and "10010" the common suffix is "10" because 
both end with "10" but not both "110" or both "010". 

Let D be a Mx(N+1) Numpy integer array such that for all 1<=i<M, 1<=j<=N, 
D[i,j] is the length of the common suffix between the substrings X[A[i,j]][:j] 
and X[A[i-1,j]][:j].  

Complete code for the following function that computes D for a given A.

Example:

>>> X = getRandomX()
>>> X
['110', '000', '001', '010', '100', '001', '100']
>>> A = constructReversePrefixSortMatrix(X)
>>> A
array([[0, 1, 1, 1],
       [1, 2, 2, 4],
       [2, 3, 5, 6],
       [3, 5, 4, 3],
       [4, 0, 6, 0],
       [5, 4, 3, 2],
       [6, 6, 0, 5]])
>>> D = constructCommonSuffixMatrix(A, X)
>>> D
array([[0, 0, 0, 0],
       [0, 1, 2, 2],
       [0, 1, 2, 3],
       [0, 1, 1, 1],
       [0, 0, 2, 2],
       [0, 1, 0, 0],
       [0, 1, 1, 3]])

Hints: 

As before, column j (0 < j <= N) of the matrix can be constructed from column j-1 
and the symbol in each sequence at index j-1.

For an efficient algorithm...
Consider: 
the length of the common suffix between X[A[i,j]][:j] and X[A[i-k,j]][:j], for all 0<k<=i is... 
min(D[i-k+1,j], D[i-k+2,j], ..., D[i,j]).

Question 4: In terms of M and N what is the asymptotic cost of your algorithm?
It is O(NM).  
"""

def constructCommonSuffixMatrix(A, X):
    """This solution has been adapted from the Durbin paper, and Alistar Miles' Github."""
    divergence = numpy.zeros(shape=A.shape, dtype=int) #Creates the Mx(N+1) D matrix
    D = numpy.zeros(shape=A.shape, dtype=int) #Creates the Mx(N+1) D matrix
    N = len(X[0])
    M = len(X)
    # initializing the divergence array
    columnDivergenceArray = [0] * M


    #iterating down the columns

    for columnNumber in range(0, N):
        #0s and 1s lists, as before
        currentZeroes = []
        currentOnes = []
        #these are initialized to the number of the column + 1, since the first cell of each column has nothing to compare to
        zeroMismatches = onesMismatches = columnNumber + 1  # q = p = k+1 in the Durbin paper


        #Iterating over the rows in reverse prefix order (which comes from A),
        #As well as the values of the last divergence array column (saved above)
        for previousMismatchesIndex in range(0, len(columnDivergenceArray)):
            #getting the symbol of the current Xi
            currentAValue = A[previousMismatchesIndex][columnNumber]

            #getting the Xi[j] symbol
            currentSymbol = X[currentAValue][columnNumber]

            #getting the mismatch count of the same Xi at the last column
            #in other words, the index where the match begins between it and the previous Xi
            previousMismatches = columnDivergenceArray[previousMismatchesIndex]

            #checking to see if the current number of mismatched 0s is greater than those corresponding to the of the previous column
            if previousMismatches > zeroMismatches:
                zeroMismatches = previousMismatches

            #doing the same for mismatched 1s
            if previousMismatches > onesMismatches:

                onesMismatches = previousMismatches

            #looking at the current symbol

            #if it is a 0, the current value of zeroMismatches is the one for the given cell
            #the formula columnNumber - # of mismatches gives us the common suffix length
            #saving that value to the current zeroes list
            #resetting zeroMismatches to 0
            if currentSymbol == "0":
                currentZeroes.append(zeroMismatches)
                zeroMismatches = 0

            #same for the ones case, but using q
            else:
                currentOnes.append(onesMismatches )
                onesMismatches = 0


        #saving this column to D
        columnDivergenceArray = currentZeroes + currentOnes

        #calculating the actual suffix thing
        for previousMismatchesIndex in range(0, len(columnDivergenceArray)):
            D[previousMismatchesIndex][columnNumber+1] = columnNumber - columnDivergenceArray[previousMismatchesIndex] + 1

    return D

"""Problem 5.
    
For a pair of strings X[x], X[y], a long match ending at j is a common substring
of X[x] and X[y] that ends at j (so that X[x][j] != X[y][j] or j == N) that is longer
than a threshold 'minLength'. E.g. for strings "0010100" and "1110111" and length
threshold 2 (or 3) there is a long match "101" ending at 5.
    
The following algorithm enumerates for all long matches between all substrings of
X, except for simplicity those long matches that are not terminated at
the end of the strings.

Note to Dennis: I was pretty lost here...if you'd be willing to leave comments pointing me in the direction of the right answers to these questions, I'd very much appreciate. 
    
Question 5a: What is the asymptotic cost of the algorithm in terms of M, N and the
number of long matches?

It is either O(NM) or variable term depending on the number of long matches between the pair of strings, whichever is larger.  
    
Question 5b: Can you see any major time efficiencies that could be gained by
refactoring?

The two loops that iterate over the long matches in lists b and c could be done in one zipped loop as was done in the Alistar Github. 
    
Question 5c: Can you see any major space efficiencies that could be gained by
refactoring?

Lists b and c could be combined into one list if one loop goes over all of the 0s and then iterates over the 1s subsequently, and adds them to the end of that list. 

Question 5d: Can you imagine alternative algorithms to compute such matches?,
if so, what would be the asymptotic cost and space usage?

The Alistar pages mentions Algorithmn 4, which could be used to compute them. It would have O(MN) time and O(M^2) space usage. 

"""
def getLongMatches(X, minLength):
    assert minLength > 0
    
    A = constructReversePrefixSortMatrix(X)
    D = constructCommonSuffixMatrix(A, X)
    
    #For each column, in ascending order of column index
    for j in range(1, 0 if len(X) == 0 else len(X[0])):
        #Working arrays used to store indices of strings containing long matches
        #b is an array of strings that have a '0' at position j
        #c is an array of strings that have a '1' at position j
        #When reporting long matches we'll report all pairs of indices in b X c,
        #as these are the long matches that end at j.
        b, c = [], []
        
        #Iterate over the aligned symbols in column j in reverse prefix order
        for i in range(len(X)):
            #For each string in the order check if there is a long match between
            #it and the previous string.
            #If there isn't a long match then this implies that there can
            #be no long matches ending at j between sequences indices in A[:i,j]
            #and sequence indices in A[i:,j], thus we report all long matches
            #found so far and empty the arrays storing long matches.
            if D[i,j] < minLength:
                for x in b:
                    for y in c:
                        #The yield keyword converts the function into a
                        #generator - alternatively we could just to append to
                        #a list and return the list
                        
                        #We return the match as tuple of two sequence
                        #indices (ordered by order in X) and coordinate at which
                        #the match ends
                        yield (x, y, j) if x < y else (y, x, j)
                b, c = [], []
            
            #Partition the sequences by if they have '0' or '1' at position j.
            if X[A[i,j]][j] == '0':
                b.append(A[i,j])
            else:
                c.append(A[i,j])
        
        #Report any leftover long matches for the column
        for x in b:
            for y in c:
                yield (x, y, j) if x < y else (y, x, j)


def main():
    theseBinaryStrings = ['110', '000', '001', '010', '100', '001', '100']
    thisRevPreSortMatrix = constructReversePrefixSortMatrix(theseBinaryStrings)
    thisY = constructYFromX(theseBinaryStrings)
    thisXFromY = constructXFromY(theseBinaryStrings, thisRevPreSortMatrix, thisY)
    thisCommmon = constructCommonSuffixMatrix(thisRevPreSortMatrix, theseBinaryStrings)

if __name__ == "__main__":
    main()
