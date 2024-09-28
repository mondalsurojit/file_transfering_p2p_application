# file_transfering_p2p_application
this program is a sample python program to trasfer any kind of files (.pdf, .mp4, .jpg etc) using p2p connection.
#standard libraries used 1)socket 2)OS
#exteral libraries used 1)tqdm
if you have a python seted in path >>go to terminal and command>> pip install tqdm(it may get version error, in that case you can upgrade your pip first)
two devices are needed one to be a sender and another to be reciever. they get connected via the senders IP address and port number. after stablishing connection the sender is promted to select path of the file to be sent. and the reciever is promted to select the path of the storage location. and then the file transfer begins. this file has no limit of transfering( say more than 100gb). Just the internet connection should be stable. and the reciever should have enough storage available.
currently this is a sample prototype. error handling, sequrity, data compressions, and Resuming connection lost status, GUI are some works that are yet to be done. but you can use it still if you have a stable  internet connection.
