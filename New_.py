
import time
start_time = time.time()
import re
import itertools
import collections 
import copy
import queue



data1=list()
count=0

# n2 = int(input("Enter number of queries: "))
# queries=list()
# print("Enter "+str(n2)+" queries")
# for i in range(n2):
#     line = input().rstrip()
#     if line.lower() == 'done':
#         break
#     queries.append(line)

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
        print(sentencetemp)
        queries.append(sentencetemp)
    else:
        queries.append(line.rstrip())  

print("queries"+str(queries))


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

variableArray = list("abcdefghijklmnopqrstuvwxyz")
variableArray2 = []
variableArray3 = []
variableArray5 = []
variableArray6 = []

for eachCombination in itertools.permutations(variableArray, 2):
    variableArray2.append(eachCombination[0] + eachCombination[1])
for eachCombination in itertools.permutations(variableArray, 3):
    variableArray3.append(eachCombination[0] + eachCombination[1] + eachCombination[2])
for eachCombination in itertools.permutations(variableArray, 4):
    variableArray5.append(eachCombination[0] + eachCombination[1] + eachCombination[2]+ eachCombination[3])
for eachCombination in itertools.permutations(variableArray, 5):
    variableArray6.append(eachCombination[0] + eachCombination[1] + eachCombination[2] + eachCombination[3] + eachCombination[4])
variableArray = variableArray + variableArray2 + variableArray3 + variableArray5 + variableArray6
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



pattern=re.compile("\||&|=>") #we can remove the '\|'' to speed up as 'OR' doesnt come in the KB
pattern1=re.compile("[(,]")
kb={}
def setupkb(kbbefore):
    print("inside setup",str(kbbefore))
    
    k = len(kbbefore)
    for i in range(0,k):   
        # print("KB before",kbbefore[i])
        temp=pattern.split(kbbefore[i])
        # print("temp",temp)
        lenoftemp=len(temp)
        for j in range(0,lenoftemp):
            clause=temp[j]
            clause=clause[:-1]
            print("clause",clause)
            predicate=pattern1.split(clause)
            argumentlist=predicate[1:]
            lengthofpredicate=len(predicate)-1

            if predicate[0] in kb:
                # print("predicate[0]",predicate[0])
                # print("KB pred",kb[predicate[0]])
                if lengthofpredicate in kb[predicate[0]]:
                    kb[predicate[0]][lengthofpredicate].append([kbbefore[i],temp,j,predicate[1:]])
                else:
                    kb[predicate[0]][lengthofpredicate]=[kbbefore[i],temp,j,predicate[1:]]
            else:
                kb[predicate[0]]={lengthofpredicate:[[kbbefore[i],temp,j,predicate[1:]]]}
            # print("kb pred[0]",kb[predicate[0]])
            
setupkb(kbbefore)

def substituevalue(paramArray, x, y):
    for index, eachVal in enumerate(paramArray):
        if eachVal == x:
            paramArray[index] = y
    return paramArray



def unificiation(arglist1,arglist2):
    print("Before Unification")
    print("arglist1",arglist1)
    print("arglist2",arglist2)
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
    print("theta",theta)
    print("New_arglist1",arglist1)
    print("New_arglist2",arglist2)             
    return [arglist1,arglist2,theta]



def resolution():
    global repeatedsentencecheck
    answer=list()
    qrno=0
    for qr in queries:
        qrno+=1
        repeatedsentencecheck.clear()
        q=queue.Queue()
        query_start=time.time()
        # kbquery=copy.deepcopy(kb)
        # print("KB",kbquery)
        ans=qr
        print(qr[0])
        # if qr[0]=='~':
        #     ans=qr[1:]
        # else:
        #     ans='~'+qr
        if qr[0]=='~':
            if('|' in qr):
                querysplit=pattern.split(qr)
                ans=querysplit[0][1:]
                if(querysplit[1][0]=='~'):
                    # print("split query1"+querysplit[1][1:])
                    kbbefore.append(querysplit[1][1:])
                    # print("kbbefore after appending"+str(kbbefore))
                    setupkb(kbbefore)
                    # print("kb after",kb)
                    # ans+="|"+querysplit[1][1:]
                else:
                    # print("split query2"+querysplit[1])
                    kbbefore.append("~"+querysplit[1])
                    # print("kbbefore after appending"+str(kbbefore))
                    setupkb(kbbefore)
                    # print("kb after",kb)
                    # ans+="|~"+querysplit[1]
            else:
                ans=qr[1:]
        else:
            if('|' in qr):
                querysplit=pattern.split(qr)
                ans='~'+querysplit[0]
                if(querysplit[1][0]=='~'):
                    # print("split query3"+querysplit[1][1:])
                    kbbefore.append(querysplit[1][1:])
                    # print("kbbefore after appending"+str(kbbefore))
                    setupkb(kbbefore)
                    # print("kb after",kb)
                    # ans+="|"+querysplit[1][1:]
                else:
                    # print("split query4"+querysplit[1])
                    kbbefore.append("~"+querysplit[1])
                    # print("kbbefore after appending"+str(kbbefore))
                    setupkb(kbbefore)
                    # print("kb after",kb)
                    # ans+="|~"+querysplit[1]
            else:
                ans='~'+qr
        # print("ans after negation"+ans)
        q.put(ans)
        kbquery=copy.deepcopy(kb)
        # print("KB",kbquery)
        currentanswer="FALSE" # TODO Change to not resovlable
        counter=0
        while True:
            counter+=1
            if q.empty():
                break
            ans=q.get()
          #  print("q",q.empty())
          #  print("ans->",ans)
            ansclauses=pattern.split(ans)
          #  print("ansclauses->",ansclauses)
            lenansclauses=len(ansclauses)

            for ac in range(0,lenansclauses):
                ansclausestruncated=ansclauses[ac][:-1]
#                print("ansclausestruncated",ansclausestruncated)
                ansclausespredicate=pattern1.split(ansclausestruncated)
#                print("ansclausespredicate->",ansclausespredicate)
                lenansclausespredicate=len(ansclausespredicate)-1
                if ansclausespredicate[0][0]=='~':
                    anspredicatenegated=ansclausespredicate[0][1:]
                else:
                    anspredicatenegated="~"+ansclausespredicate[0]   
                x=kbquery.get(anspredicatenegated,{}).get(lenansclausespredicate) # x is matching rules in KB 
#                print("x->",x)

                if not x:
                    continue      
                else:
                    lenofx=len(x) 
#                    print("lenofx->",lenofx)
                    mergepart1=""
                    for numofpred in range(0,lenofx):
#                        print("Mergepart1_INSIDE->",mergepart1)

                        if len(mergepart1) >0:
                            x=kbquery.get(mergepart1,{}).get(lenansclausespredicate) # x is matching rules in KB            
                            if x is None:
                                break
#                        print("x_INSIDE->",x)
                        sentenceselected=x[numofpred]
#                        print("sentenceselected->",sentenceselected)
                        thetalist=unificiation(copy.deepcopy(sentenceselected[3]),copy.deepcopy(ansclausespredicate[1:]))
#                        print("thetalist->",thetalist)
#                        print("sentenceselected[3]->",sentenceselected[3])
#                        print("ansclausespredicate->",ansclausespredicate[1:])

                        if(len(thetalist)!=0):
                            for key in thetalist[2]:
                                # print("key->",key)
                                # tl=thetalist[2][key]
                                tl=key
                                tl2=thetalist[2].get(key)
                                # print("tl->",tl)
                                # print("tl2->",tl2)
                                if tl2:
                                    thetalist[2][key]=tl2
                            # print("thetalist->",thetalist)
                            flagmatchedwithkb=1
                            notincludedindex=sentenceselected[2]
                            senclause=copy.deepcopy(sentenceselected[1])
                            # print("senclause->",senclause)
                            mergepart1=""
                            del senclause[notincludedindex]
#                            print("senclause->",senclause)
                            ansclauseleft=copy.deepcopy(ansclauses)
#                            print("ansclauseleft->",ansclauseleft)
                            del ansclauseleft[ac]
#                            print("ansclauseleft->",ansclauseleft)

                            for am in range(0,len(senclause)):
                                senclause[am]=replace(senclause[am],thetalist[2])
                                mergepart1=mergepart1+senclause[am]+'|'      

                            for remain in range(0,len(ansclauseleft)):
                                listansclauseleft=ansclauseleft[remain]
                                ansclauseleft[remain]=replace(listansclauseleft,thetalist[2])
                                if ansclauseleft[remain] not in senclause:
                                    mergepart1=mergepart1+ansclauseleft[remain]+'|'
                            mergepart1=mergepart1[:-1]
#                            print("mergepart1->",mergepart1)
                            if mergepart1=="":
                               values = list(thetalist[2].values())
                               are_equal = False
                               if len(values)>1:
                                   are_equal = all(value == values[0] for value in values)
#                               print("are_equal->",are_equal)
                               if are_equal:
                                   continue
                               currentanswer="TRUE"
                               break                             
                            ckbflag=insidekbcheck(mergepart1)

                            if not ckbflag:
                                    # mergepart1=insidestandardizationnew(mergepart1)
#                                    print("After Stand mergepart1->",mergepart1)
#                                    print(numofpred)
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
#                    print("After Loop x->",x)
#                    print("currentanswer->",currentanswer)                         

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
    print("Final answer is: ".join(finalanswer))
