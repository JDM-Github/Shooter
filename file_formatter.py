import os


class Formatter:

    @staticmethod
    def save_encrypted_bin_file(file, text, cryptor=None):
        with open(file, "w") as f:
            if os.path.exists(text):
                with open(text, "r") as t:
                    output = (t.read().replace("\n", "")).replace("    ", "")
            else:
                output = (text.replace("\n", "")).replace("    ", "")
            if cryptor is not None:
                output = cryptor.encrypt_text(output)
            f.write("".join(format(ord(i), "08b")+"\n" for i in output))

    @staticmethod
    def save_decrypted_bin_file(file, text, cryptor=None):
        with open(file, "w") as f:
            with open(text, "r") as t:
                result = ""
                data = t.read()
                for i in range(0, len(data), 9):
                    temp_data = data[i:i+9]
                    result = result + chr(int(temp_data, 2))
                    print(temp_data)
                if cryptor is not None:
                    result = cryptor.decrypt_text(result)
                f.write(result)

    @staticmethod
    def convert_string_to_bin(text, cryptor=None):
        output = (text.replace("\n", "")).replace("    ", "")
        if cryptor is not None:
            output = cryptor.encrypt_text(output)
        return "".join(format(ord(i), "08b") for i in output)

    @staticmethod
    def convert_bin_to_string(file, cryptor=None):
        with open(file, "r") as text:
            output = ""
            data = text.read()
            for i in range(0, len(data), 9):
                temp_data = data[i:i+9]
                output = output + chr(int(temp_data, 2))
            if cryptor is not None:
                output = cryptor.decrypt_text(output)
            return output
