# Perceptive Automation

## Scenario:
In self-driving vehicles, the camera and sensors are constantly scanning the environment to detect obstacles that the vehicle may encounter. Obstacles are generally static in the environment and may be easier to process, while others may be stochastic in nature and not follow a strict pattern. One such observation is when humans intend to cross the road (not the chicken!). Often, you may encounter a pedestrian openly waiting for the vehicle to stop so that they may cross the road. In another case, a person may be behind another obstacle and suddenly come into camera view, can the vehicle detect this person and stop within time?

## Task:
Given a video captured from a vehicle (e.g. dashcam):

1. Generate frames for analysis
2. Determine whether pedestrian is on sidewalk and showing intent to cross
3. If on sidewalk, then is pedestrian showing intent to cross
4. Perform analysis of data
