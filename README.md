## How to test the HTTP proxy ?



1. Run the server on a terminal. Keep it running and switch to your favorite web browser.
2. Go to your browser's proxy settings and change the proxy server to `localhost` and port to the one you defined
3. Now open any HTTP website (not HTTPs) and you should see the tracking on your terminal and access the content of the web page on the browser.



## How to test the TCP proxy ?

1. Run the server on a terminal. Keep it running and start a process.
2. Go to your OS' proxy settings and change the proxy server to localhost
3. You should be able to connect and see the exchanges on your terminal
