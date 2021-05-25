# Car_dealer
#A network implementation of blockchain to monitor/manage transactions that exchanged vehicles for cash in a secure manner

# How to Run <h1> 
1. Clone Repository 
2. Open two terminals (One for the client and one for the server)
3. For the client terminals run "python3 client.py"
4. For the server terminal run "python3 server.py"

# Functions 
  ## Buyers - 
  * PURCHASE
  ## Sellers - 
  * SELL
  ## Both - 
  * ADD
  * VIEW
  * HISTORY
  * AVAILABLE

# Logic <h1>

* Buyer sends a request to DMV with the seller’s id and the money required for the purchase.

* DMV finds the seller and request the car from that seller.

* Once DMV has both money and car, it then sends the items to the respected nodes

* DMV sends the money to the seller

* DMV sends the car to the buyer

* Then we check if the buyer received the car and then check if the seller received the money

* Once this is done, the DMV mines the new block with the owner and the car and adds it to the Blockchain


