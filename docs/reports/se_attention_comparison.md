\# SE Attention Comparison



\## Purpose



This experiment was conducted as the risk-management alternative defined in the accepted TÜBİTAK 2209-A project proposal.



The proposal states that if the selected attention mechanism does not improve model performance, a simpler channel-focused Squeeze-and-Excitation (SE) mechanism should be evaluated.



The previous VGG16 + CBAM experiment produced a slightly lower validation MAE than the VGG16 baseline, but its test MAE was worse. Therefore, the SE-Net alternative was implemented and evaluated under the same experimental conditions.



\---



\## Experimental Setup



The SE experiment used the same synthetic FRIDA/FRIDA2 dataset and the same scene-based data split as the previous experiments.



\- Total images: 672

\- Training images: 464

\- Validation images: 96

\- Test images: 112

\- Image size: 224 × 224

\- Batch size: 16

\- Epochs: 20

\- Optimizer: Adam

\- Learning rate: 1e-4

\- Weight decay: 1e-5

\- Loss function: L1Loss / MAE

\- Random seed: 42

\- Backbone: ImageNet-pretrained VGG16

\- Backbone status: Frozen

\- Regression head: Same as the baseline VGG16 experiment

\- SE reduction ratio: 16



The SE block was inserted after the final convolutional block of VGG16 and before the final MaxPool operation.



This placement matches the location previously used for CBAM, allowing the attention mechanisms to be compared under closely aligned architectural conditions.



\---



\## SE Architecture



The SE block performs channel-wise feature recalibration using:



1\. Global average pooling

2\. Channel reduction

3\. ReLU activation

4\. Channel expansion

5\. Sigmoid gating

6\. Channel-wise feature scaling



Parameter counts:



\- Total parameters: 27,658,817

\- Trainable parameters: 12,944,129

\- Frozen parameters: 14,714,688

\- SE trainable parameters: 32,768

\- Regression head trainable parameters: 12,911,361



The VGG16 backbone remained frozen while the SE block and regression head were trainable.



\---



\## Training Results



The model was trained for 20 epochs.



Best checkpoint:



\- Best epoch: 19

\- Best validation MAE: 70.6083 m



Final epoch:



\- Training MAE: 50.1878 m

\- Validation MAE: 70.7658 m



Validation performance improved steadily until epoch 19 and slightly degraded at epoch 20. Therefore, the checkpoint from epoch 19 was correctly retained as the best model.



\---



\## Independent Test Results



The best SE checkpoint was evaluated on the same untouched 112-image scene-based test set used for the previous models.



Results:



\- Test samples: 112

\- Test MAE: 72.4412 m

\- Mean signed error: -12.9774 m

\- Minimum absolute error: 0.1255 m

\- Maximum absolute error: 423.1353 m



The negative mean signed error indicates that the model still exhibits an average underestimation tendency.



\---



\## Comparison with Previous Models



| Model | Best Validation MAE | Test MAE | Mean Signed Error | Maximum Absolute Error |

|---|---:|---:|---:|---:|

| VGG16 baseline | 69.9705 m | \*\*66.7227 m\*\* | -17.3877 m | \*\*392.8829 m\*\* |

| VGG16 + CBAM | \*\*69.3274 m\*\* | 67.6214 m | \*\*-10.8501 m\*\* | 439.5097 m |

| VGG16 + SE | 70.6083 m | 72.4412 m | -12.9774 m | 423.1353 m |



Compared with the VGG16 baseline, the SE-enhanced model increased test MAE by:



\- 5.7185 m

\- approximately 8.57%



Compared with VGG16 + CBAM, the SE-enhanced model increased test MAE by:



\- 4.8198 m



\---



\## Interpretation



The SE mechanism did not improve the overall regression performance of the VGG16 model under the current synthetic FRIDA/FRIDA2 experimental setup.



Although the SE model produced a lower minimum absolute error and a smaller mean underestimation bias than the baseline model, these secondary improvements did not translate into a lower overall test MAE.



The baseline VGG16 model remains the best-performing synthetic model according to the primary selection criterion defined in the project: test MAE.



Current synthetic ranking:



1\. VGG16 baseline — 66.7227 m

2\. VGG16 + CBAM — 67.6214 m

3\. VGG16 + SE — 72.4412 m

4\. ResNet50 baseline — 124.6181 m



\---



\## Scientific Conclusion



Under the current single-seed synthetic experimental setup, neither CBAM nor SE improved the test MAE of the VGG16 baseline.



Therefore:



\- The attention hypothesis is not supported by the current synthetic test results.

\- The SE-Net risk-management alternative defined in the accepted proposal has been executed.

\- The selected synthetic architecture remains the baseline VGG16 model.

\- No statistical significance claim is made because the current comparison is based on a single deterministic split and a single random seed.



The next major research stage is real-world validation and fine-tuning using FVEI/FHVI or an appropriate accessible alternative dataset, as defined in the accepted TÜBİTAK proposal.

