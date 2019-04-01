from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://suzvassh:rfX15GwxG-0irniZUlrxhHoHAg5nipBA@hyena.rmq.cloudamqp.com/suzvassh'
QUEUE_NAME = 'test_queue'

# Initialize a client
client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)

# Send a message
#client.sendDataFetcherTask({'name' : 'test message'})


# Receive a message
client.getDataFetcherTask()
