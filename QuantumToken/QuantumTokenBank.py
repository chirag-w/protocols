from random import randint, random, sample
from time import sleep
from cqc.pythonLib import CQCConnection, qubit


cheating = 0
wait = 2
N = 2
M = 8
random_pair_number = []
Bank_bits2 = [ [] for i in range(M) ]
Bank_bits = [ [] for i in range(M) ]
Bank_basis = [[] for j in range(M)]
token = [[] for i in range(M)]
outcomes_from_merchant = []
s = []
def distributing_money():
    global cheating
    print("The first part is starting and The bank prepare the money")
    with CQCConnection("Alice") as Alice:
        for serial in range(M):
            for j in range(N):
                random_bits = randint(0,1)
                random_bits2 = randint(0,1)
                random_basis = randint(0,1)
                Bank_bits2[serial].append(random_bits2)
                Bank_bits[serial].append(random_bits)
                Bank_basis[serial].append(random_basis)
                q1 = qubit(Alice)
                q2 = qubit(Alice)
                if random_bits == 1:
                    q1.X()
                if random_bits2 == 1:
                    q2.X()
                if random_basis == 1:
                    q1.H()
                else:
                    q2.H()
                token[j].append((q1,q2))
                Alice.sendQubit(q1, "Eve")
                Alice.sendQubit(q2, "Eve")
        Alice.flush()
        print("Bank sent qubits pairs/token to Client")
        sleep(wait)
        for serial in range(M):
            for j in range(N):
                outcomes_from_merchant = list(Alice.recvClassical())
                print ("The bank accepts the bits and base from merchant: ", outcomes_from_merchant)

                if outcomes_from_merchant[2] == 0:
                    which_qubit_to_check = Bank_basis[serial][j]
                    if which_qubit_to_check == 0:
                        if Bank_bits[serial][j] != outcomes_from_merchant[0]:
                            print("1. Cheating")
                            cheating += 1
                    else:
                        if Bank_bits2[serial][j] != outcomes_from_merchant[1]:
                            print("2. Cheating")
                            cheating += 1
                else:
                    which_qubit_to_check = 1 - Bank_basis[serial][j]
                    if which_qubit_to_check == 0:
                        if Bank_bits[serial][j] != outcomes_from_merchant[0]:
                            print("3. Cheating")
                            cheating += 1
                    else:
                        if Bank_bits2[serial][j] != outcomes_from_merchant[1]:
                            print(Bank_bits2[serial][j])
                            print(outcomes_from_merchant[1])
                            print("4. Cheating")
                            cheating += 1
        if (cheating > 0):
            print ("There is cheating here :( Money rejected", cheating)     
        else:
            print ("There is no cheating, super! :) Money accepted")      
        print ("End of protocol !")

if __name__ == "__main__":
    distributing_money()
