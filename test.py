from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import pprint
import gzip

rpc_user="wk"
rpc_password="wk"

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
  fout=gzip.open("block_info3.txt.gz","w")
  for height in range(start,end):
    if height%1000==0: print(height)
    hash=rpc_connection.getblockhash(height)
    block=rpc_connection.getblock(hash, 2)
    tx_list=block["tx"]
    for tx in tx_list:
      for vout in tx["vout"]:
        #print(vout["value"])
        s="%s %s %f %d\n"%(tx["hash"], vout["n"], vout["value"],
          len(vout["scriptPubKey"]["hex"])/2)
        fout.write(s.encode('utf-8'))
  fout.close()

#printAllTxOut(410009,410010)
printAllTxOut(367000,472408)

