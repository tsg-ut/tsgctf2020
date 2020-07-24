import torch
import torch.nn as nn
import torch.nn.functional as F

imgH = 42
imgW = 20
charnum = 93

import pickle
fontdata = pickle.load(open('fontdata','rb'))

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        self.conv = nn.Conv2d(3, 6, 5) # bsize * 6 * 38 * 16
        self.pool = nn.MaxPool2d(2, 2) # bsize * 6 * 19 * 8
        self.fc1 = nn.Linear(6 * 19 * 8, 120)
        self.fc2 = nn.Linear(120, charnum)

    def forward(self, x):
        x = self.pool(F.relu(self.conv(x)))
        x = x.view(-1, 6 * 19 * 8)
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x

net = Net()
#dummy_input = torch.randn(10, 3, 32, 32)

import params

ds = list(fontdata.items())
cs = list(params.S)

import random
import numpy as np

dataset = []
for i in range(10):
    random.shuffle(ds)
    dataset.append((
    	torch.transpose(torch.FloatTensor(list(map(lambda x: x[1],ds))),1,3),
    	torch.LongTensor(list(map(lambda x: cs.index(x[0]),ds)))
    ))

#print(dataset)

import torch.optim as optim

criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

for epoch in range(100):  # loop over the dataset multiple times
    running_loss = 0.0
    for data in dataset:
        # get the inputs; data is a list of [inputs, labels]
        inputs, labels = data

        # zero the parameter gradients
        optimizer.zero_grad()

        # forward + backward + optimize
        # print(inputs.shape,labels.shape)
        # print(labels)
        outputs = net(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        # print statistics
        running_loss += loss.item()
    print('[%d] loss: %.3f' % (epoch,running_loss))

print('Finished Training')


ind = torch.FloatTensor([list(fontdata.values())[0]])
# torch.Size([1, 42, 20, 3])
ind = torch.transpose(ind,1,3)
print(ind.shape)
td = net(ind)
print(td.shape)
"""
"""

dummy_input = ind
input_names = [ "img" ] + [ "param%d" % i for i in range(6) ]
output_names = [ "class" ]

torch.onnx.export(net, dummy_input, "model.onnx", verbose=True, input_names=input_names, output_names=output_names)


