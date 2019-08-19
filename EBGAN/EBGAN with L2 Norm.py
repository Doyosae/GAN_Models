import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)): 
    ssl._create_default_https_context = ssl._create_unverified_context

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
 
from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("./mnist/data/", one_hot=True)
path = "./save"





# Generator Function
def Build_Generator (inputs):
    
    # 이하 Generator 관여하는 모든 변수는 variable_scope로 묶어요.
    with tf.variable_scope("Generator_Variables"):
        
        outputs = tf.layers.dense(inputs, 128*7*7)
        outputs = tf.reshape(outputs, [-1, 7, 7, 128])
        outputs = tf.layers.batch_normalization(outputs, training = Is_Training)
        outputs = tf.nn.relu (outputs)
        
        outputs = tf.layers.conv2d_transpose(outputs, 128, [5, 5], 
                                            strides = (2, 2), 
                                            padding = "SAME", 
                                            use_bias = False)
        outputs = tf.layers.batch_normalization(outputs, training = Is_Training)
        outputs = tf.nn.relu (outputs)
        
        outputs = tf.layers.conv2d_transpose(outputs, 64, [5, 5], 
                                            strides = (2, 2), 
                                            padding = "SAME", 
                                            use_bias = False)
        outputs = tf.layers.batch_normalization(outputs, training = Is_Training)
        outputs = tf.nn.relu (outputs)
        
        outputs = tf.layers.conv2d_transpose(outputs, 1, [5, 5], 
                                            strides = (1, 1), 
                                            padding = "SAME", 
                                            use_bias = False)
        
        # outputs image size is [None, 28, 28, 1]
        outputs = tf.nn.tanh (outputs)
        
    return outputs

    
# Discriminator Autoencdoer Function
def Build_DiscriminatorAutoencoder (inputs, reuse = None) : 
    
    # 이하 Dirscriminator에 관여하는 모든 변수는 variable_scope로 묶어요.
    with tf.variable_scope("Discriminator_Variables") as scope:
        
        if reuse:
            scope.reuse_variables()
            
        # inputs size is [None, 28, 28, 1]
        
        outputs = tf.layers.conv2d (inputs, 64, (5, 5), strides = (2, 2), padding ="SAME", use_bias = True)
        outputs = tf.nn.leaky_relu (outputs)
        # size is [None, 14, 14, 32]
        
        outputs = tf.layers.conv2d (outputs, 128, (5, 5), strides = (2, 2), padding ="SAME", use_bias = False)
        outputs = tf.layers.batch_normalization(outputs, training = Is_Training)
        outputs = tf.nn.leaky_relu (outputs)
        # size is [None, 7, 7, 64]
        
        outputs = tf.layers.conv2d_transpose(outputs, 64, [5, 5], strides = (2, 2), padding = "SAME", use_bias = False)
        outputs = tf.layers.batch_normalization(outputs, training = Is_Training)
        outputs = tf.nn.leaky_relu (outputs)
        # size is [None, 14, 14, 32]

        outputs = tf.layers.conv2d_transpose(outputs, 1, [5, 5], strides = (2, 2), padding = "SAME", use_bias = True)
        outputs = tf.nn.leaky_relu (outputs)
        # size is [None, 14, 14, 32]
        
    return outputs
 
    
# Noise Function
def Build_GetNoise (batch_size, noise_size):
    return np.random.uniform(-1.0, 1.0, size=[batch_size, noise_size])





# 데이터셋 전체를 학습에 사용할 횟수
# 데이터셋을 쪼갤 서브셋의 크기
# 노이즈의 크기
# Margin은 ECGAN에서 정의한 Loss Function에 필요한 인자에요. (URL : https://arxiv.org/abs/1609.03126)
TotalEpoch= 200
BatchSize = 128
NoiseLength = 100
Margin = max (1, BatchSize/64) 

# Variable GeneratorVal/dense/kernel already exists, disallowed. 해결 방법
# tf.reset_default_graph()를 그래프 맨 앞에 적어두기
tf.reset_default_graph()
 
Is_Training = tf.placeholder(tf.bool)
DiscInput = tf.placeholder(tf.float32, [None, 28, 28, 1])
GeneInput = tf.placeholder(tf.float32, [None, NoiseLength])

DiscGlobalStep = tf.Variable(0, trainable = False, name = "DiscGlobal")
GeneGlobalStep = tf.Variable(0, trainable = False, name = "GeneGlobal")


# 노이즈를 Generator에 입력하면 [-1, 28, 28, 1] 결과가 나오나,
# Discriminator에 보낼때는 다시 [-1. 784] 형태로 tf.reshape을 하도록 설계했어요.
FakeImage = Build_Generator(GeneInput)

# DiscInput은 MNIST train 이미지가 담기는 placeholder이고, 이것을 Discriminator에 보낼꺼에요.
# Generator를 지나온 ReFakeImage는 reuse = True 상태로 보내요. 
# 진짜 이미지를 이미 거친 Discriminator의 인자들을 재활용해요.
DiscReal = Build_DiscriminatorAutoencoder(DiscInput)
DiscGene = Build_DiscriminatorAutoencoder(FakeImage, True)

# 여태까지 모양을 한 번 검사해봅시다.
print (np.shape(DiscReal))
print (np.shape(DiscInput))
print (np.shape(DiscGene))
print (np.shape(FakeImage))


# 중요한 부분.
# Discriminator에 대해여 진짜 이미지 입력벡터와 출력벡터의 차이를 squared summation 한 후, mean을 계산해요.
# 마찬가지로 가짜 이미지 입력벡터와 출력벡터의 차이를 squared summation 한 후, mean을 계산해요.
# Autoencoder의 출력이 입력과 근사하도록 만드는 과정과 일치합니다.

# 의문점???
# 처음에 구현하였을 때는 tf.pow로 입출력 차이값들을 모두 제곱하고, reduce_mean으로 다 더해서 평균을 냈어요.
# 그런데 논문을 다시 보니 손실도를 L2 Norm으로 생각한 것 같아서 sqrt를 사이에 끼웠더니 수렴 속도는 느리지만
# 매우 깔끔한 결과물을 얻었어요. 수렴 속도가 빠르다고 좋은건 아니긴 하네요.

# DiscReal : 출력벡터, DiscInput : 입력벡터
# DiscGene : 출력벡터, ReFakeImage : 입력벡터
RealImageLoss = tf.sqrt (2 * tf.nn.l2_loss(DiscReal - DiscInput)) / BatchSize
FakeImageLoss = tf.sqrt (2 * tf.nn.l2_loss(DiscGene - FakeImage)) / BatchSize
print (np.shape (RealImageLoss), np.shape (FakeImageLoss))

# Discriminator에서 가짜이미지의 손실은 그대로 Generator의 손실로 정의하고요. (해당 논문 그대로 옮김)
# Discriminator의 손실을 새롭게 정의하는데 논문의 수식을 거의 그대로 갖고왔어요.
# 다만 Margin의 계산을 Relu의 개념을 빌리면서 보통 1 내지 그 이상이면 충분하다고 알려진 것 같아요.
DiscLoss = RealImageLoss + tf.maximum (Margin - FakeImageLoss, 0)
GeneLoss = FakeImageLoss

# tf.get_collection과 tf.GraphKeys.TRAINABLE_VARIABLES with "scope 이름" 을 이용하여 독립으로 학습시킨 변수들의 묶음을 정의해요.
# Discriminator의 변수와 Generator의 변수는 따로 학습시켜요. (GAN의 기본 뼈대)
# tf.control_dependecies는 묶음 연산과 실행 순서를 정의하는 메서드에요.
# UpdataOps를 먼저 실행하고 TrainDisc, TrainGene을 실행해요. (DCGAN의 경우 with tf.control~~이 없어도 결과가 잘 나왔으나...)
GeneVars = tf.get_collection (tf.GraphKeys.TRAINABLE_VARIABLES, scope = "Generator_Variables")
DiscVars = tf.get_collection (tf.GraphKeys.TRAINABLE_VARIABLES, scope = "Discriminator_Variables")
UpdateOps = tf.get_collection (tf.GraphKeys.UPDATE_OPS)


with tf.control_dependencies(UpdateOps):
    
    # 조금 어려운 부분이에요. AdamOptimizer를 사용하고, 적절한 learning_rate를 찾아야해요. 통상 적대적 신경망은 lr이 매우 낮긴 해요.
    TrainDisc = tf.train.AdamOptimizer(learning_rate = 0.0002, beta1 = 0.5).minimize(DiscLoss, var_list=DiscVars, global_step = DiscGlobalStep)
    TrainGene = tf.train.AdamOptimizer(learning_rate = 0.0002, beta1 = 0.5).minimize(GeneLoss, var_list=GeneVars, global_step = GeneGlobalStep)

    
    
    
    
# 늘 해왔던 것처럼 Session을 열고 그래프를 실행해요.
with tf.Session() as sess:
    saver = tf.train.Saver()
    sess.run(tf.global_variables_initializer())
    TotalBatch = int(mnist.train.num_examples / BatchSize)
    
    for epoch in range(TotalEpoch):
        
        DiscLossValue = 0
        GeneLossValue = 0
        
        for i in range(TotalBatch):
            
            batch_xs, batch_ys = mnist.train.next_batch(BatchSize)
            batch_xs = np.reshape (batch_xs, (-1, 28, 28, 1))
            NOISE = Build_GetNoise(BatchSize, NoiseLength)

            # Discriminator는 원본 이미지와 노이즈가 생성한 이미지를 모두 받은 후에 학습하여서 feed_dict가 DiscInput, GeneInput 둘 다 필요
            sess.run(TrainDisc, feed_dict = {DiscInput : batch_xs, GeneInput : NOISE, Is_Training : True})
            DiscLossValue = sess.run(DiscLoss, feed_dict = {DiscInput : batch_xs, GeneInput : NOISE, Is_Training : True})
            
            # feed_dict에는 batch_xs도 넣지만, GeneLoss 계산 시에 Discriminator를 freeze 하였죠.
            # 따라서 원본 이미지가 입력되어도 관여하지 않아요. 오직 노이즈만 받으면 됩니다.
            # feed_dict에 DiscInput을 명시하고 싶지 않으나, 오류가 발생하는데 왜 그러는지는 잘 모르겠네요.
            sess.run(TrainGene, feed_dict = {DiscInput : batch_xs, GeneInput : NOISE, Is_Training : True})
            GeneLossValue = sess.run(GeneLoss, feed_dict = {DiscInput : batch_xs, GeneInput : NOISE, Is_Training : True})

        print('Epoch:', '%02d  ' %(epoch+1), 'Discriminator loss: {:.4}  '.format(DiscLossValue), 'Generator loss: {:.4}  '.format(GeneLossValue))


        # 모든 결과를 보기 위해서 매 epoch마다 결과물을 출력합니다.
        if epoch % 1 == 0:
            
            NOISE = Build_GetNoise(10, NoiseLength)
            Samples = sess.run(FakeImage, feed_dict = {GeneInput : NOISE, Is_Training : False})

            fig, ax = plt.subplots(1, 10, figsize=(20, 10))

            for i in range(10):
                ax[i].set_axis_off()
                ax[i].imshow(np.reshape(Samples[i], (28, 28)))

            plt.show ()
            plt.close(fig)
            
        if (epoch+1) % 25 == 0:
            
            print ("%d epoch에서 한 번 저장할게요." %(epoch+1))
            saver.save(sess, path + "/EBGAN_with_L2Norm" + str(epoch+1) + ".ckpt")
