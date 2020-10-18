# Introduction to columnar transposition
Columnar transposition Edit
In a columnar transposition, the message is written out in rows of a fixed length, and then read out again column by column, and the columns are chosen in some scrambled order. Both the width of the rows and the permutation of the columns are usually defined by a keyword. For example, the word ZEBRAS is of length 6 (so the rows are of length 6), and the permutation is defined by the alphabetical order of the letters in the keyword. In this case, the order would be "6 3 2 4 1 5".

In a regular columnar transposition cipher, any spare spaces are filled with nulls; in an irregular columnar transposition cipher, the spaces are left blank. Finally, the message is read off in columns, in the order specified by the keyword. For example, suppose we use the keyword ZEBRAS and the message WE ARE DISCOVERED. FLEE AT ONCE. In a regular columnar transposition, we write this into the grid as:
```
6 3 2 4 1 5
W E A R E D 
I S C O V E 
R E D F L E 
E A T O N C 
E Q K J E U 
```
Providing five nulls (QKJEU) at the end. The ciphertext is then read off as:

EVLNE ACDTK ESEAQ ROFOJ DEECU WIREE
In the irregular case, the columns are not completed by nulls:
```
6 3 2 4 1 5
W E A R E D 
I S C O V E 
R E D F L E 
E A T O N C 
E 
```
This results in the following ciphertext:
```
EVLNA CDTES EAROF ODEEC WIREE
```
To decipher it, the recipient has to work out the column lengths by dividing the message length by the key length. Then he can write the message out in columns again, then re-order the columns by reforming the key word.

# Implementation
+ Based on Genetic Algorithm.
+ Use weighted Suitability Assessment as fitness function.
+ Revive if too much convergence 
+ Optimized bigram/trigram.
+ B plus tree optimization.

# Specificattion 
Alphabet Set: \[A-Z_\], space is replaced by _ </br>
Default Key Length(Column): 10 </br>
Plaintext padded to 10*N with 'X'</br>

# Usage
```
ct_crack.py [-d] [file]
```
Option
+ -d : decrypt mode

# Result 
Key Length: 10
Attempts: 1000
Average Time to Find One Answer: 4.7 seconds
First found correctness: ~90%  
