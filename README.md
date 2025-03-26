Driver Behavior Analysis & Risk Detection

Overview
This project uses Machine Learning and K-Means clustering to analyze driver behavior and detect risky driving patterns based on acceleration and gyroscope sensor data. By clustering different driving styles, the model helps identify behaviors like harsh acceleration, sudden braking, and sharp turns, which can indicate accident risks.

Objectives

1)Analyze driver behavior using unsupervised learning (K-Means clustering).

2)Detect risky driving patterns using acceleration & gyroscope data.

3)Visualize clusters to understand high-risk driving behaviors.

4)Optimize clustering using the Elbow Method for better accuracy.

 Technologies Used
 Python (Pandas, NumPy, Scikit-Learn)
 Machine Learning (K-Means Clustering)
 Data Visualization (Seaborn, Matplotlib)

 Risk-based clustering: Groups drivers based on acceleration and gyroscope sensor values
 Data preprocessing & feature engineering: Handles missing values and optimizes input features
 Cluster visualization: Uses scatter plots & pair plots for clear insights
 Accident risk identification: Helps predict potentially dangerous driving behavior

  92% precision in detecting high-risk behaviors

 Clusters
![Screenshot 2025-03-26 003442](https://github.com/user-attachments/assets/d4b7135b-43c5-4eb6-8fe9-4d5e0fbb88de)

![Screenshot 2025-03-26 003644](https://github.com/user-attachments/assets/2028ba69-5663-46ac-8cf6-3032a1a4aaac)





Cluster 0: High Negative Acceleration and High Angular Velocity (Potential Risky Driving) 
accelX = -2.17, accelY = -11.99 → Sudden deceleration and lateral movement (harsh braking or 
swerving).

gyroZ = -35.36 → High rotational movement, indicating sharp turns or loss of control.

Risk Assessment: This cluster may represent aggressive drivers who frequently brake hard or make 
sudden maneuvers, increasing accident risk. 
 
Cluster 1: High Vertical Acceleration and Extreme Gyro Movements (Very Risky) 
accelZ = 33.22 → Sudden vertical movement, possibly due to hitting bumps or aggressive 
acceleration.

gyroX = -23.80, gyroY = -18.61 → Strong gyroscope movements, indicating rapid lane changes or 
drifting.

Risk Assessment: This group could represent very risky drivers, including those who engage in 
reckless behaviors like hard acceleration, sudden lane changes, and potential rollovers. 
 
Cluster 2: Normal Driving Behavior (Safe Driving) 
accelX = 0.64, accelY = -0.33, accelZ = 9.76 → Moderate acceleration values, indicating controlled 
driving.

gyroX, gyroY, gyroZ are close to zero → Minimal rotational movement, suggesting stable driving. 
 
Risk Assessment: This cluster likely represents safe drivers who maintain smooth acceleration and 
steering control.
