import sys, os
import random
import time
sys.path.append("/home/pi/mobile-privacy-client-message/thrift/gen-py")
from QueryAnswer import ttypes

rng = random.SystemRandom()

#generate random byte or int string as the key
def genkeyS(length):
    return os.urandom(length)

def genkeyI(num):
    return rng.randint(10 ** (num - 1), (10 ** (num)) - 1)
    
#xor encryption
def xorEncryptS(message,key):
    return "".join(chr(ord(a)^ord(b)) for a,b in zip(message,key))

#encrypt and decrypt QueryAnswers
def encrypt(query):
    anIdK = genkeyS(len(query.analystId))
    quIdK = genkeyI(len(str(query.queryId))) 
    spId = query.splitId
    ansBitsK = genkeyS(len(query.answerBits))
    queryE = ttypes.QueryAnswer(xorEncryptS(query.analystId, anIdK), query.queryId^quIdK, query.splitId, xorEncryptS(query.answerBits, ansBitsK))
    queryK = ttypes.QueryAnswer(anIdK, quIdK, spId, ansBitsK)
    return (queryE, queryK)

def decrypt((queryE, queryK)):
    queryD = ttypes.QueryAnswer(xorEncryptS(queryE.analystId, queryK.analystId), queryE.queryId^queryK.queryId, queryK.splitId, xorEncryptS(queryE.answerBits, queryK.answerBits))
    return queryD

#testing functions
def genBits(length):
    genned = 0
    bitsStr = ''

    while genned < length:
	bitsStr = bitsStr + str(random.randint(0, 1))
	genned = genned + 1
    return bitsStr

def sampleQueries():
    i = 0
    while i < 5:
	aId = genkeyS(5)
	qId = genkeyI(5)
	sId = genkeyI(5)
	aBits = genBits(5)

	query = ttypes.QueryAnswer(aId, qId, sId, aBits)
	print 'QueryAns: ', query.analystId, ' ', query.queryId, ' ', query.splitId, ' ', query.answerBits

	encQueries = encrypt(query)
	print 'Encrypted: ', encQueries

	query = decrypt(encQueries)
	print 'Decrypted: ', query.analystId, ' ', query.queryId, ' ', query.splitId, ' ', query.answerBits
	print ''
	i = i + 1	

start = time.ctime()
sampleQueries()
print 'Start: ', start
print 'End: %s' % time.ctime()
