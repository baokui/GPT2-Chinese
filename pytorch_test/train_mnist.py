import torch
import torch.nn as nn
import torch.utils.data as Data
import torchvision
import matplotlib.pyplot as plt

torch.manual_seed(1)

EPOCH = 1
BATCH_SIZE = 50
LR = 0.001
DOWNLOAD_MNIST = True

train_data = torchvision.datasets.MNIST(
    root='./mnist',
    train=True,
    transform=torchvision.transforms.ToTensor(),
    download=DOWNLOAD_MNIST,
)

test_data = torchvision.datasets.MNIST(root='./mnist', train=False)

# 批处理
train_loader = Data.DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)
# 测试
test_x = torch.unsqueeze(test_data.test_data, dim=1).type(torch.FloatTensor)[:2000] / 255
test_y = test_data.test_labels[:2000]

test_x = test_x.cuda()
test_y = test_y.cuda()

# 卷积(Conv2d) -> 激励函数(ReLU) -> 池化, 向下采样 (MaxPooling) ->
# 再来一遍 -> 展平多维的卷积成的特征图 -> 接入全连接层 (Linear) -> 输出

class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential( # 1x28x28
            nn.Conv2d(
                in_channels=1,
                out_channels=16,
                kernel_size=5,
                stride=1,
                padding=2,
            ),# 16x28x28
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2)
        )
        self.conv2 = nn.Sequential( # 16x14x14
            nn.Conv2d(16, 32, 5, 1, 2),# 32x14x14
            nn.ReLU(),
            nn.MaxPool2d(2),# 32x7x7
        )
        self.out = nn.Linear(32*7*7, 10)

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)  # 展平多维的卷积图成 (batch_size, 32 * 7 * 7)\
        output = self.out(x)
        return output

cnn = CNN()
cnn = cnn.cuda()
print(cnn)

optimizer = torch.optim.Adam(cnn.parameters(), lr=LR)
loss_func = nn.CrossEntropyLoss()

for epoch in range(EPOCH):
    for step, (b_x, b_y) in enumerate(train_loader):
        output = cnn(b_x.cuda())
        loss = loss_func(output, b_y.cuda())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

test_output = cnn(test_x[:10])
pred_y = torch.max(test_output, 1)[1].data.cpu().numpy().squeeze()
print(pred_y, 'prediction number')
print(test_y[:10].cpu().numpy(), 'real number')
