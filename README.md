# Huffman_Coding 
Program that compresses and decompresses files using Huffman codes. 
The compressor will be a command-line utility that encodes any file into a compressed 
version with a .huf extension. The decompressor will be a web server that will let you 
decode as they are being sent to your web browser.
# Included files:
- util.py


# Running instructions:
Decompression:
- Move the util.py file to a directory containing the __pycache_ file, the wwwroot file, the bitio.py, the compress.py, webserver.py and huffman.py.
- Proceed to open the terminal and navigate to the wwwroot directory in the terminal and run:
	python3 ../webserver.py
- Once you perform this, you will see a message: Listening on port 8000
- Proceed to open the following web address on your web browser: http://localhost:8000
- To compress a file and create a new output file proceed to the terminal and run:
  python3 ../compress.py <File_Name>

