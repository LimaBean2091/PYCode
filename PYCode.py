import sys;
import time;

start = time.time();

debug = False;
default_charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890 `~!@#$%^&*()_+-=[]\{}|;\':",./<>?'

def printError(message):
    print("{0}: error: {1}".format(sys.argv[0],message));
    sys.exit();
def printWarning(message):
    print("{0}: warning: {1}".format(sys.argv[0],message));
def printDebug(message):
    if (debug):
        print("{0}: debug: {1}".format(sys.argv[0],message));
def getCharset():
    try:
        with open('charset.txt','r') as f:
            printDebug("file charset: {0}, LEN: {1}".format(f.read(),len(f.read())));
            return f.read();
    except Exception:
        printWarning("error reading charset file. Using default charset.");
        with open('charset.txt','w') as f:
            f.write(default_charset);
            printDebug("Wrote file charset: {0}, LEN: {1}".format(default_charset,len(default_charset)));
        return default_charset;
strs = getCharset();
printDebug("Strs: {0}, {1}".format(strs,getCharset()));
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
        if debug:
            perc = round(i/(len(strs)+1)*25);
            percbar = round(i/(len(strs)+1)*100);
            bar = 25-perc;
            print("{2}: debug: Generating tables... [{0}] [{1}%]".format("#"*perc+" "*bar,percbar,sys.argv[0]),end='\r');
        table.append(shifttext(i,strs));
    print();
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
        printDebug("ALPH: {0}, INDEX: {1}, LETTER: {2}, ALPHINDEX: {3}".format(alph,index,letter,alph[index]));
        if alph[index] == letter:
            return alph[0];
def getLetter(index,alphabet):
    return alphabet[index];
def encode(toEncode_,codeword_):
    i=0;
    word = '';
    printDebug("Encoding: {0}, {1}".format(toEncode_,codeword_));
    for c in toEncode_:
        v = codeword_[i];
        try:
            word += getLetter(getIndex(v),getAlphabet(getIndex(c)));
        except Exception:
            printError("charset does not contain character: '{0}' (Hint: Try using --usedefaultcharset or modify the charset.)".format(c));
            break;
        i+=1;
        printDebug("ALPH: {0}, INDEX_V: {1}, INDEX_C: {2}, LETTER_F: {3}, LETTER_ORG: {4}".format(getAlphabet(getIndex(c)),getIndex(v),getIndex(c),getLetter(getIndex(v),getAlphabet(getIndex(c))),c));
        if i >= len(codeword_):
            i = 0;
    return(word);
def decode(toDecode_,codeword_):
    i=0;
    word = '';
    printDebug("Decoding: {0}, {1}".format(toDecode_,codeword_));
    for c in toDecode_:
        v = codeword_[i];
        word+=getLetterD(getIndex(v),c);
        i+=1;
        if i >= len(codeword_):
            i = 0;
    return(word);
def printUsage(code,message):
    print("usage: python3 {0} [--d] [--usedefaultcharset] [--debug] code message".format(sys.argv[0]));
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
codeword = '';

if len(sys.argv) >= 2:
    codeword = sys.argv[1];
    for i in range(2,len(sys.argv)):
        arg = sys.argv[i];
        if arg[:2] == "--":
            arg = arg[-len(arg)+2:]
            if arg == 'd':
                decodeM = True;
            if arg == 'usedefaultcharset':
                strs = default_charset;
                table = gentable();
            if arg == 'debug':
                print("Debug Mode");
                debug = True;
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
end = time.time();
print("\nTime elapsed: {0}".format(end-start));