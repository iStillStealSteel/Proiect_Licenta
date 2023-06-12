import docx2txt
my_text_as_string = docx2txt.process("test.docx")
#print(my_text_as_string)

my_text_as_array=my_text_as_string.split(".")
i=1
for elem in my_text_as_array:
    print(elem+" "+str(i))
    i+=1
    
