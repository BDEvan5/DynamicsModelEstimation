## DynamicsModelEstimation

- Aim: use a data set to estimate the model that best describes it
- Aim2: Use the model to train a DRL agent
    - Therefore, the model must be non-exploitable.

- If you redo the data to consider only the change in states between two frames, then you should be able to use the linear model as is for the no-slip case.
    -  The new position will be mainly y and and a little x every time.
    - This could be a good idea
    - Then you can just append it
    

