from __future__ import division
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import sys
import pprint
import gzip

rpc_user="test"
rpc_password="test"

# rpc_user and rpc_password are set in the bitcoin.conf file
rpc_connection = AuthServiceProxy("http://%s:%s@127.0.0.1:8332"%(rpc_user, rpc_password))
#best_block_hash = rpc_connection.getbestblockhash()
#print(rpc_connection.getblock(best_block_hash))

## # batch support : print timestamps of blocks 0 to 99 in 2 RPC round-trips:
## commands = [ [ "getblockhash", height] for height in range(410009,410010) ]
## block_hashes = rpc_connection.batch_(commands)
## blocks = rpc_connection.batch_([ [ "getblock", h, 2 ] for h in block_hashes ])
## block_times = [ block["time"] for block in blocks ]
## print(block_times)
## for block in blocks:
##   tx=block["tx"]
##   pprint.pprint(tx)

def printAllTxOut(start,end):
  fout=gzip.open("block_info1.txt.gz","w")
  txCount=0
  cinCount=0
  coutCount=0
  for height in range(start,end):
    if height%1000==0: print(height)
    hash=rpc_connection.getblockhash(height)
    block=rpc_connection.getblock(hash)
    #print sys.getsizeof(block, 1)
    #print block
    tx_list=block["tx"]
    #print len(tx_list)
    for txid in tx_list:
      tx = rpc_connection.getrawtransaction(txid, 1)
      txCount+=1
      #print tx
      for vout in tx["vout"]:
	s="%s\n"%(vout["scriptPubKey"]["asm"])
        print(s)
	coutCount+=1
	#fout.write(s.encode('utf-8'))
      for vin in tx["vin"]:
        if vin.has_key('coinbase'):
            continue
        s="%s %s %s %d\n"%(tx["hash"], vin["scriptSig"]["asm"], vin["txid"],
          len(vin["scriptSig"]["hex"]))
        cinCount+=1
        print(s)
        fout.write(s.encode('utf-8'))
  print "Tx count = %d" %(txCount)
  print "Cout count = %d" %(coutCount)
  print "Cin count = %d" %(cinCount)
  print "Cin/Tx = %f" %(cinCount/txCount)
  s = "%d %d %d %f\n"%(txCount, coutCount, cinCount, (cinCount/txCount))
  fout.write(s.encode('utf-8'))
  fout.close()

printAllTxOut(521000,521001)

