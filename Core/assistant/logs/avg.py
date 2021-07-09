import matplotlib.pyplot as plt

total = []
with open('total-response-time.txt') as f:
	for line in f:
		total.append(float(line))

	f.close()

replica = []
with open('replcia-time.txt') as f:
	for line in f:
		replica.append(float(line))
	f.close()

decode = []

with open('decode-time.txt') as f:
	for line in f:
		decode.append(float(line))
	f.close()


print('avg total: ' + str(sum(total)/len(total)))
print('avg decode: ' + str(sum(replica)/len(replica)))
print('avg voice: ' + str(sum(decode)/len(decode)))