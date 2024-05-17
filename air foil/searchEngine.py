import json
class Search:
    # initialize dict and word searched   
    def __init__(self, dictionry, code_search = "none"):
        self.dict = dictionry
        self.code_ser = code_search
        self.suggestions_lst = []

    # Search healper give code suggestions for the uesr 
    def search_helper(self):
        if self.code_ser not in self.dict:
            self.code_index = len(self.code_ser)
            while self.code_index:
                self.prefix = self.code_ser[:self.code_index]
                self.code_index -= 1
                # Search about match this input
                for self.code in self.dict:
                    if self.code.startswith(self.prefix):
                        self.suggestions_lst.append(self.code)
                        # Out when finding codes with first prefix
                        self.code_index = 0  
            return self.suggestions_lst

        else:
            return self.dict[self.code_ser]
            

# with open('data.json', 'r') as json_file:
#     data = json.load(json_file)
#     json_file.close()

# v= "a63a108c"
# ss= Search(data, v)
# print(ss.search_helper())



