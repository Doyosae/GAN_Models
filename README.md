# Introdunction  
MNIST 데이터들로 여러가지 Generative Adversarial Networks을 구현해보고 있습니다.  
논문의 조건을 바꾸어가면서 더 공부하면서 GAN 알고리즘을 연습하는 공간입니다.  
  
  
***
# Reference  
- Generative Adversarial Networks (GAN)  
  URL : https://arxiv.org/abs/1406.2661  
- Unsupervised Representation Learning with Deep Convolutional Generative Adversarial Networks (DCGAN)  
  URL : https://arxiv.org/abs/1511.06434  
- Energy-based Generative Adversarial Network (EBGAN)  
  URL : https://arxiv.org/abs/1609.03126  
- InfoGAN: Interpretable Representation Learning by Information Maximizing Generative Adversarial Nets (InfoGAN)  
  URL : https://arxiv.org/abs/1606.03657  
- BEGAN: Boundary Equilibrium Generative Adversarial Networks (BEGAN)  
  URL : https://arxiv.org/abs/1703.10717  
- Escaping from Collapsing Modes in a Constrained Space (BEGAN-CS)  
  URL : https://arxiv.org/abs/1808.07258  
- Wasserstein GAN (WGAN)  
  URL : https://arxiv.org/abs/1701.07875  
  
  
***
# Summary  
  
  
## 1. DCGAN  
![DCGAN1](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN1.png)  
![DCGAN2](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN2.png)  
![DCGAN3](https://github.com/Doyosae/GAN_Guideline/blob/master/DCGAN/sample/DCGAN3.png)  
  
  
  
## 2. EBGAN  
-  Generator의 수렴 속도가 매우 빨랐음  
-  without sqrt에서는 81 Epoch부터 모델이 완전히 죽어버렸다. 왜 그럴까? sqrt가 빠져서 균형을 맞추지 못한 것 (?)    
-  논문에서의 내용대로 L2 Norm을 적용하면, 수렴 속도는 훨씬 느렸지만, 더 깔끔한 이미지를 얻을 수 있음  
  
### 2-1. EBGAN (without Square root)  
![EBGAN1](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN1.png)  
![EBGAN2](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN2.png)  
![EBGAN3](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/EBGAN3.png)  
  
### 2-2. EBGAN Model is dead (without Square root)   
![Collapse](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/81%20epoch.png)  
  
### 2-3. EBGAN with L2 Normalization  
![L21](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%201.png)  
![L22](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%202.png)  
![L23](https://github.com/Doyosae/GAN_Guideline/blob/master/EBGAN/sample/L2%20Norm%203.png)  
  
  
  
## 3. BEGAN
- Gamma 값은 Mode의 diversiy를 결정함. Gamma 파라미터를 1 이하로 하면 심각한 Mode Collapse가 발생  
- 값을 1 이상으로 높이면 Mode Collapse를 조금 완화함. 그러나 생성 이미지의 품질은 하락  
- Latent Space를 탐색하면 GAN의 학습 특성은 잘 반영한 것임을 알 수 있음 (기억 기반이 아님을 증명)  
- 보통 GAN의 벤치마크로 쓰이는 데이터셋은 CelebA와 같이 MNIST에 비해 Data Distribution이 Continuous한 특성이 강함  
- BEGAN의 논문에서도 강한 Multi mode에 대해서는 구체적인 대안을 제시하지 않았음  
- 예를 들어 백인 남성, 황인 남성, 흑인 남성의 데이터 관계와 숫자 1, 2, 3의 데이터 관계에서 어떠한 차이점이 있는지 알아야 함  
- Mode Collapse는 데이터 분포가 연속적인지 강하게 분리되어 있는지에 따라 민감하게 의존하는 것이 아닐까?  
- BEGAN의 Mode collapse Escaping에 대한 논문은 존재 (앞으로 실험 예정)  
  
### 3-1. BEGAN (== 50 epochs)  
![BEGAN1](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/BEGAN%20sample%201.png)  
![BEGAN2](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/BEGAN%20sample%202.png)  
![BEGAN3](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/BEGAN%20sample%203.png)  
  
### 3-2. BEGAN Latent Space  
![LATENT1](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/Latent%20Space%201.png)  
![LATENT2](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/Latent%20Space%202.png)  
  
### 3-3. BEGAN Mode Collapse (>= 75 epochs)  
![collapse](https://github.com/Doyosae/GAN_Guideline/blob/master/BEGAN/sample/Mode%20collapse%202%20(75epoch).png)  
  
  
  
## 4. WGAN  
- Loss Function은 reduce_mean으로 구현한 것이 차이점  
  
![WGAN1](https://github.com/Doyosae/GAN_Models/blob/master/WGAN/sample/WGAN1.png)  
![WGAN2](https://github.com/Doyosae/GAN_Models/blob/master/WGAN/sample/WGAN2.png)  
![WGAN3](https://github.com/Doyosae/GAN_Models/blob/master/WGAN/sample/WGAN3.png)  
