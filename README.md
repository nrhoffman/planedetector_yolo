https://github.com/user-attachments/assets/c113919e-c566-4279-be5b-0ed439f3f866

DATA = https://universe.roboflow.com/gdit/aerial-airport/dataset/1

Warning: Picking an area too large for CPU can crash computer.

INSTRUCTIONS
1) An API Key must be created here: https://console.cloud.google.com/welcome

2) Make a .env file at the project root directory and paste this line:
   "API_KEY=<YOUR_API_KEY>"

3) Replace <YOUR_API_KEY> with your API Key from step 1 and save/close it

4) Run "docker compose up"
    - The first time installing the backend image will take a long time

5) Open browser and go to localhost

6) Select two points on a map and select the Send Coordinates button

After Loading, it'll give an image of detections and the number of planes
found.
