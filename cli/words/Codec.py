import struct
import base64

class Codec:
    def decode(self, binary):
        if len(binary) == 32:
            compiler = struct.Struct("32s")
            word = compiler.unpack(binary)[0]
            word = str(base64.b64decode(word), encoding="utf-8")
            return word

    def encode(self, text):
        text = text.strip()
        text = base64.b64encode(bytes(text, encoding="utf-8")) 
        compiler = struct.Struct('32s')
        binary = compiler.pack(text)
        return binary
