
import time
start_time = time.time()
import re
import collections 
import copy
import queue


data1=list()
count=0

def CNF(sentence):
    temp=re.split("=>",sentence)
    temp1=temp[0].split('&')
    for i in range(0,len(temp1)):
        if temp1[i][0]=='~':
            temp1[i]=temp1[i][1:]
        else:
            temp1[i]='~'+temp1[i]
    temp2='|'.join(temp1)
    temp2=temp2+'|'+temp[1]
    return temp2

n2 = int(input("Enter number of queries: "))
queries=list()
kbbefore=list()
print("Enter "+str(n2)+" queries")
for i in range(n2):
    line = input()
    line=line.replace(" ","") 
    if "=>" in line:
        line=line.replace(" ","") 
        sentencetemp=CNF(line.rstrip())
        queries.append(sentencetemp)
    else:
        queries.append(line.rstrip())  


k = int(input("Enter number of rules: "))
print("Enter "+str(k)+" rules")
for i in range(k):
    line = input()
    line=line.replace(" ","") 
    if "=>" in line:
        line=line.replace(" ","") 
        sentencetemp=CNF(line.rstrip())
        kbbefore.append(sentencetemp)
    else:
        kbbefore.append(line.rstrip())  

capitalVariables = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
number=0


def replace(sentence,theta):
    newsentence=sentence
    i=0
    while i <=len(newsentence)-1 :
        if(newsentence[i]==',' or newsentence[i]=='('):
            if newsentence[i+1] not in capitalVariables:
               j=i+1
               while(newsentence[j]!=',' and newsentence[j]!=')' ):
                     j+=1
               nstemp=newsentence[i+1:j]      
               substitution=theta.get(nstemp)
               if substitution :
                    newsentence=newsentence[:i+1]+substitution+newsentence[j:]
                    i=i+len(substitution)
        i+=1   
    return newsentence    

repeatedsentencecheck=collections.OrderedDict()


def insidekbcheck(sentence):
    newsentence=pattern.split(sentence)
    newsentence.sort()
    newsentence="|".join(newsentence)
    global repeatedsentencecheck 
    i=0
    while i <=len(newsentence)-1 :
        if(newsentence[i]==',' or newsentence[i]=='('):
            if newsentence[i+1] not in capitalVariables:
               j=i+1
               while(newsentence[j]!=',' and newsentence[j]!=')' ):
                     j+=1
               newsentence=newsentence[:i+1]+'x'+newsentence[j:]
        i+=1
    repeatflag=repeatedsentencecheck.get(newsentence)
    if repeatflag :
        return True
    repeatedsentencecheck[newsentence]=1    
    return False                           

for i in range(0,k):
    kbbefore[i]=kbbefore[i].replace(" ","") 



pattern=re.compile("\||&|=>")
pattern1=re.compile("[(,]")
kb={}
def setupkb(kbbefore):
    k = len(kbbefore)
    # k is no of Rules
    for i in range(0,k):
        temp=pattern.split(kbbefore[i])
        lenoftemp=len(temp)
        # lenoftemp is no of clauses in a rule
        for j in range(0,lenoftemp):
            clause=temp[j]
            clause=clause[:-1]
            predicate=pattern1.split(clause)
            lengthofpredicate=len(predicate)-1
            #Check if predicate is already in KB
            if predicate[0] in kb:
                # Check for no of arguments inside predicate
                if lengthofpredicate in kb[predicate[0]]:
                    kb[predicate[0]][lengthofpredicate].append([kbbefore[i],temp,j,predicate[1:]])
                else:
                    kb[predicate[0]][lengthofpredicate]=[kbbefore[i],temp,j,predicate[1:]]
            else:
                kb[predicate[0]]={lengthofpredicate:[[kbbefore[i],temp,j,predicate[1:]]]}
            
# KB before is CNF Clauses
setupkb(kbbefore)

def substituevalue(paramArray, x, y):
    for index, eachVal in enumerate(paramArray):
        if eachVal == x:
            paramArray[index] = y
    return paramArray



def unificiation(arglist1,arglist2):
    theta = collections.OrderedDict()
    for i in range(len(arglist1)):
        if arglist1[i] != arglist2[i] and (arglist1[i][0] in capitalVariables) and (arglist2[i][0] in capitalVariables):
            return []     
        elif arglist1[i] == arglist2[i] and (arglist1[i][0] in capitalVariables) and (arglist2[i][0] in capitalVariables):
            if arglist1[i] not in theta.keys():  
                theta[arglist1[i]] = arglist2[i]
        elif (arglist1[i][0] in capitalVariables) and not (arglist2[i][0] in capitalVariables):
            if arglist2[i] not in theta.keys():
                theta[arglist2[i]] = arglist1[i]
                arglist2 = substituevalue(arglist2, arglist2[i], arglist1[i])
        elif not (arglist1[i][0] in capitalVariables) and (arglist2[i][0] in capitalVariables):
            if arglist1[i] not in theta.keys():
                theta[arglist1[i]] = arglist2[i]
                arglist1 = substituevalue(arglist1, arglist1[i], arglist2[i])   
        elif not (arglist1[i][0] in capitalVariables) and not (arglist2[i][0] in capitalVariables):
            if arglist1[i] not in theta.keys():
                theta[arglist1[i]] = arglist2[i]
                arglist1 = substituevalue(arglist1, arglist1[i], arglist2[i])
            else:
                argval=theta[arglist1[i]]
                theta[arglist2[i]]=argval
                arglist2 = substituevalue(arglist2, arglist2[i], argval)          
    return [arglist1,arglist2,theta]



def resolution():
    global repeatedsentencecheck
    # creating a list that contains all the answers in case of multiple queries
    answer=list()
    qrno=0
    #iterate through the queries one by one 
    for qr in queries:
        qrno+=1
        repeatedsentencecheck.clear()
        #create a queue that stores each clause of the queries
        q=queue.Queue()
        #time to check if there is a loop
        query_start=time.time()
        ans=qr
        #To negate the query
        if qr[0]=='~':
            if('|' in qr):
                querysplit=pattern.split(qr)
                ans=querysplit[0][1:]
                if(querysplit[1][0]=='~'):
                    kbbefore.append(querysplit[1][1:])
                    setupkb(kbbefore)
                else:
                    kbbefore.append("~"+querysplit[1])
                    setupkb(kbbefore)
            else:
                ans=qr[1:]
        else:
            if('|' in qr):
                querysplit=pattern.split(qr)
                ans='~'+querysplit[0]
                if(querysplit[1][0]=='~'):
                    kbbefore.append(querysplit[1][1:])
                    setupkb(kbbefore)
                else:
                    kbbefore.append("~"+querysplit[1])
                    setupkb(kbbefore)
            else:
                ans='~'+qr
        #print()
        print("***** Resolution Start *****")
        #print()
        print("Query after negation=> "+ans)
        #print()
        #Adding the negated query to the queue
        q.put(ans)
        kbquery=copy.deepcopy(kb)
        print("KB=> ",kbquery)
        #starting with the answer to the resolution set to false
        currentanswer="FALSE" 
        counter=0
        while True:
            counter+=1
            if q.empty():
                break
            ans=q.get()
            ansclauses=pattern.split(ans)
            lenansclauses=len(ansclauses)

            for ac in range(0,lenansclauses):
                ansclausestruncated=ansclauses[ac][:-1]
                #extract the predicate of the query
                ansclausespredicate=pattern1.split(ansclausestruncated)
                lenansclausespredicate=len(ansclausespredicate)-1
                #negating the query again to find the matching rule
                if ansclausespredicate[0][0]=='~':
                    anspredicatenegated=ansclausespredicate[0][1:]
                else:
                    anspredicatenegated="~"+ansclausespredicate[0]   
                x=kbquery.get(anspredicatenegated,{}).get(lenansclausespredicate) # x is matching rules in KB 
                #print()
                #print("Rules that can be resolved with query: ",x) 

                if not x:
                    continue      
                else:
                    lenofx=len(x) 
                    mergepart1=""
                    for numofpred in range(0,lenofx):
                        if len(mergepart1) >0:
                            x=kbquery.get(mergepart1,{}).get(lenansclausespredicate) # x is matching rules in KB            
                            if x is None:
                                break
                        sentenceselected=x[numofpred]
                        #print()
                        #print("Clause selected ->",sentenceselected)  
                        thetalist=unificiation(copy.deepcopy(sentenceselected[3]),copy.deepcopy(ansclausespredicate[1:]))

                        if(len(thetalist)!=0):
                            for key in thetalist[2]:
                                tl=key
                                tl2=thetalist[2].get(key)
                                if tl2:
                                    thetalist[2][key]=tl2
                            notincludedindex=sentenceselected[2]
                            senclause=copy.deepcopy(sentenceselected[1])
                            mergepart1=""
                            del senclause[notincludedindex]
                            ansclauseleft=copy.deepcopy(ansclauses)
                            del ansclauseleft[ac]

                            for am in range(0,len(senclause)):
                                senclause[am]=replace(senclause[am],thetalist[2])
                                mergepart1=mergepart1+senclause[am]+'|'      

                            for remain in range(0,len(ansclauseleft)):
                                listansclauseleft=ansclauseleft[remain]
                                ansclauseleft[remain]=replace(listansclauseleft,thetalist[2])
                                if ansclauseleft[remain] not in senclause:
                                    mergepart1=mergepart1+ansclauseleft[remain]+'|'
                            mergepart1=mergepart1[:-1]
                            #print()
                            #print("Clause Left->",mergepart1)
                            if mergepart1=="":
                               values = list(thetalist[2].values())
                               are_equal = False
                               if len(values)>1:
                                   are_equal = all(value == values[0] for value in values)
                               if are_equal:
                                   continue
                               currentanswer="TRUE"
                               break                             
                            ckbflag=insidekbcheck(mergepart1)

                            if not ckbflag:
                                    ans=mergepart1
                                    temp=pattern.split(ans)
                                    lenoftemp=len(temp)

                                    for j in range(0,lenoftemp):
                                        clause=temp[j]
                                        clause=clause[:-1]
                                        predicate=pattern1.split(clause)
                                        argumentlist=predicate[1:]
                                        lengthofpredicate=len(predicate)-1

                                        if predicate[0] in kbquery:
                                            if lengthofpredicate in kbquery[predicate[0]]:
                                                kbquery[predicate[0]][lengthofpredicate].append([mergepart1,temp,j,argumentlist])
                                            else:
                                                kbquery[predicate[0]][lengthofpredicate]=[[mergepart1,temp,j,argumentlist]]
                                        else:
                                            kbquery[predicate[0]]={lengthofpredicate:[[mergepart1,temp,j,argumentlist]]}
                                    q.put(ans)                      
                    if(currentanswer=="TRUE"):
                        break                        
            if(currentanswer=="TRUE"):
               break
            if(counter==2000 or (time.time()-query_start)>20):
                break
        answer.append(currentanswer)
    return answer  

if __name__ == '__main__': 

    finalanswer=resolution()
    print("Is the query resolvable: "+str(finalanswer[0]))
