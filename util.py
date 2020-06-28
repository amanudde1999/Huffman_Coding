import bitio
import huffman
import pickle


def read_tree(tree_stream):
    '''Read a description of a Huffman tree from the given compressed
    tree stream, and use the pickle module to construct the tree object.
    Then, return the root node of the tree itself.

    Args:
      tree_stream: The compressed stream to read the tree from.

    Returns:
      A Huffman tree root constructed according to the given description.
    '''
    # The tree is unpickled from the tree stream
    unpickled = pickle.load(tree_stream) 
    return unpickled       
   

def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.
    """
    node = tree
    # The while loop will keep as long as we are in a branch   
    while not isinstance(node, huffman.TreeLeaf):
            # Depending on the value of the bit that is read, we will move left or right
            bit = bitreader.readbit()
            if bit == 0:
              node = node.getLeft()
            
            elif bit == 1:
              node = node.getRight()
    # This try/except block will deal with out end of file error
    try:        
      # Once we reach a leaf we will obtain its value
      return node.getValue()
    # Once we have the end of file error it will be excepted and we will return None for later use
    except EOFError:
      return None
    

def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.
    '''
    flag = 1
    # We get the bits from the compressed stream and use it to obtain our tree
    unpickled = read_tree(compressed)
    # Bit Reader object is created
    in_stream = bitio.BitReader(compressed)
    # Bit Writer object is created
    out_stream = bitio.BitWriter(uncompressed)
    while flag == 1:
      # Coded bits will be decoded until we reach the end and None will be returned
      decoded = decode_byte(unpickled,in_stream)
      if decoded == None:
        flag = 0 
      # Keep writing the bits until we reach the end of the file
      elif decoded != None:
        out_stream.writebits(decoded,8)
    out_stream.flush()

      

def write_tree(tree, tree_stream):
    '''
    Write the specified Huffman tree to the given tree_stream
    using pickle.

    Args:
      tree: A Huffman tree.
      tree_stream: The binary file to write the tree to.
    '''
    # The tree is pickled and we write it to the tree stream    
    pickle.dump(tree,tree_stream)
    

def compress(tree, uncompressed, compressed):
    '''
    First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
  '''
    # The given tree is written to the compressed     
    write_tree(tree,compressed)
    # The bit writer object is created
    compressed_ = bitio.BitWriter(compressed)
    # The bit reader object is created
    uncompressed_ = bitio.BitReader(uncompressed) 
    # Encoding table is made here
    encoding_table = huffman.make_encoding_table(tree)
    flag1 = 1
    while flag1 == 1:
      # To catch the End of File error
      try:
        # Reading 8 bits (byte)
        current_bits = uncompressed_.readbits(8)
        # These are stored in an encoding table
        compressed1 = encoding_table[current_bits]
        for bits in compressed1:
          compressed_.writebit(bits)
          
      
      except EOFError:
        for bits in encoding_table[None]:
          compressed_.writebit(bits)
          # Where the while loop will end
          flag1 = 0
    compressed_.flush()

  


  
