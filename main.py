class Filereader:
    def __init__(self,filename):
        self.filename = filename
        self.lines = [] 
    def read(self):
        file = open(self.filename)
        self.lines = file.readlines()
        file.close()


digits = ['0','1','2','3','4','5','6','7','8','9']



fr = Filereader('examples/matrix.c')
fr.read()


class DFA:
    def __init__(self,name,inputs,table,accepted):
        self.name = name
        self.inputs = inputs
        self.table = table
        self.accepted = accepted
    def next(self,current,input_ch):
        if not input_ch in self.inputs:
            input_ch = "AW"
        return self.table[current][input_ch]



    
    


# integer numbers detection
table_num_dec = {
    'A' : {'0' : 'C', '1' : 'B','2' : 'B','3' : 'B','4' : 'B','5' : 'B','6' : 'B','7' : 'B','8' : 'B','9' : 'B','AW':'TRAP'},
    'B' : {'0' : 'B', '1' : 'B','2' : 'B','3' : 'B','4' : 'B','5' : 'B','6' : 'B','7' : 'B','8' : 'B','9' : 'B','AW':'TRAP'},
    'C' : {'0' : 'C', '1' : 'TRAP','2' : 'TRAP','3' : 'TRAP','4' : 'TRAP','5' : 'TRAP','6' : 'TRAP','7' : 'TRAP','8' : 'TRAP','9' : 'TRAP','AW':'TRAP'},
    'TRAP' : {'0' : 'TRAP', '1' : 'TRAP','2' : 'TRAP','3' : 'TRAP','4' : 'TRAP','5' : 'TRAP','6' : 'TRAP','7' : 'TRAP','8' : 'TRAP','9' : 'TRAP','AW':'TRAP'},
}

rule_num_dec = DFA('numbers',digits,table_num_dec,['B','C'])

nums = ['']

counter = 0
current_state = 'A'
for line in fr.lines:
    print("==============================")
    print("Line length : "+ str(len(line)))
    print("==============================")
    for ch_counter in range(0,len(line)):
        print(line[ch_counter])
        print("counter :"+ str(counter) + ", ch_counter"+ str(ch_counter))
        nums[counter] += line[ch_counter]
        next_state = rule_num_dec.next(current_state,line[ch_counter])

        print('WE ARE AT '+ current_state + ' and are going to ' + next_state)
        current_state = next_state
        if(current_state == 'TRAP'):
            current_state = 'A'
            nums[counter] = ''
            print("WE TRAPPED")
        if(ch_counter == len(line)-1):
            if(current_state in rule_num_dec.accepted):
                print("FOUNDED = "+ str(nums[counter]))
                counter = counter + 1
                nums.append('')

                print("END OF LINE")
        else:
            if(current_state in rule_num_dec.accepted):
                
                next_state = rule_num_dec.next(current_state,line[ch_counter+1])
                if not next_state in rule_num_dec.accepted :
                    print("FOUNDED = "+ str(nums[counter]))
                    counter = counter + 1
                    nums.append('')
                    print("NEXT STEP IS NOT ACCEPTED")
                else:
                    print("NEXT STEP IS ALSO ACCEPTED")


nums = filter(lambda x: x != '', nums)

print(nums)
                


    

