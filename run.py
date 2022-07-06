import peer
import time

print("\nSkatoCoin")
print("---------")

peer = peer.Peer()

while True:
    
    choice = input("")
    
    if choice == "connect":
        ip = input("IP address: ")
        if ip == "self":
            ip = peer.ip
        peer.connect(ip)
        peer.client.close()
        
    elif choice == "append":
        block = input("")
        peer.add_block(block)
        
    elif choice == "peers":
        
        for p in peer.peers:
           print("0x" + p + " at " + peer.peers[p])
           
    elif choice == "chain":
        
        print(peer.chain)
        