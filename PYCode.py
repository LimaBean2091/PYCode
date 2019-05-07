import sys;

default_charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 `~!@#$%^&*()_+-=[]\{}|;\':",./<>?'
def getCharset():
    try:
        with open('charset.txt','r') as f:
            return f.read();
    except Exception:
        print ("Error reading charset file. Using default charset.");
        with open('charset.txt','w') as f:
            f.write(default_charset);
        return default_charset;
strs = getCharset();
def shifttext(shift,inp):
    data = []
    for i in inp:
        if i.strip() and i in strs:
            data.append(strs[(strs.index(i) + shift) % len(strs)])    
        else:
            data.append(i)
    output = ''.join(data)
    return output
def gentable():
    table = [];
    for i in range(0,len(strs)+1):
        table.append(shifttext(i,strs));
    return table;
def getIndex(letter):
    x = 0;
    for i in strs:
        if letter == i:
            return x;
        x += 1;
    return 39;
table = gentable();
def getAlphabet(index):
    return table[index];
def getLetterD(index,letter):
    for alph in table:
        if alph[index] == letter:
            return alph[0];
def getLetter(index,alphabet):
    return alphabet[index];
def encode(toEncode_,codeword_):
    i=0;
    word = '';
    for c in toEncode_:
        v = codeword_[i];
        word += getLetter(getIndex(v),getAlphabet(getIndex(c)));
        i+=1;
        if i >= len(codeword_):
            i = 0;
    return(word);
def decode(toDecode_,codeword_):
    i=0;
    word = '';
    for c in toDecode_:
        v = codeword_[i];
        word+=getLetterD(getIndex(v),c);
        i+=1;
        if i >= len(codeword_):
            i = 0;
    return(word);
def printUsage(code,message):
    print("usage: python3 {0} [--d] [--usedefaultcharset] code message".format(sys.argv[0]));
    m = '';
    if (code == ''):
        m += 'code';
    if (message == ''):
        m += 'message'
    if (m == 'code'):
        print('{0}: error: the following arguments are required: code'.format(sys.argv[0]));
    elif (m == 'message'):
        print('{0}: error: the following arguments are required: message'.format(sys.argv[0]));
    elif (m == 'codemessage'):
        print('{0}: error: the following arguments are required: code, message'.format(sys.argv[0]));
codeword = ''
esd = ''
decodeM = False
if len(sys.argv) >= 2:
    codeword = sys.argv[1];
    esd = ''
    decodeM = False;
    for i in range(2,len(sys.argv)):
        arg = sys.argv[i];
        if arg[:2] == "--":
            arg = arg[-len(arg)+2:]
            if arg == 'd':
                decodeM = True;
            if arg == 'usedefaultcharset':
                strs = default_charset;
                table = gentable();
        else:
            esd += sys.argv[i] + " ";               
        
    if (esd == ''):
        printUsage(codeword,esd);
        sys.exit();
else:
    printUsage(codeword,esd);
    sys.exit();
esd = esd[:-1]
if (decodeM): 
    print('"'+decode(esd,codeword)+'"');
else:
    print('"'+encode(esd,codeword)+'"');
