class View:
    def red(self,text):
        print(f"\033[1;31m{text}\033[0m")
        return self 

    def green_input(self,text):
        prompt = f"\033[1;32m[{text}] \033[0m"
        keyword = input(prompt).lower()
        return keyword        

    def white(self,text):
        print(text)
        return self

    def display_words(self,words):
        print()
        print("User Defined Keywords List")
        print("=" * 80)
        for word in words:
            print(word,end="    ")
        print()
        print()
        return self