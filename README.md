# Introdunction  
MNIST 데이터들로 여러가지 적대적 생성 신경망을 구현해보고 있어요.  
연습하는 공간입니다.  
  
***
# Reference  
- Generative Adversarial Networks (GAN)  
  URL : https://arxiv.org/abs/1406.2661  
- Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks (DCGAN)  
  URL : https://arxiv.org/abs/1511.06434  
- Energy-based Generative Adversarial Network  (EBGAN)  
  URL : https://arxiv.org/abs/1609.03126  
- InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets (InfoGAN)  
  URL : https://arxiv.org/abs/1606.03657  
  
***
# MNIST Summary  
### DCGAN  
![DCGAN1](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN1.png)  
![DCGAN2](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN2.png)  
![DCGAN3](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN3.png)  
  
### EBGAN without sqrt  
-  Generator의 수렴 속도가 놀랍도록 빨랐습니다. (5 Epoch부터 이미 예시의 샘플을 얻음)  
-  81 Epoch부터 Model Collapse가 반드시 생겼습니다. 왜 그런건가요? sqrt 연산이 빠져서 학습 억제가 안되기 때문인가요?  
-  논문에서의 내용대로 L2 Norm을 적용하면, 수렴 속도는 훨씬 느렸지만, 더 깔끔한 이미지를 얻을 수 있었습니다.  
  
![EBGAN1](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN1.png)  
![EBGAN2](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN2.png)  
![EBGAN3](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN3.png)  
![Collapse](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/81%20epoch.png)  
  
### EBGAN with L2 Normalization  
![L21](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%201.png)  
![L22](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%202.png)  
![L23](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%203.png)  
