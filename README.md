# arduino_cam_follower

Little experiment I did with an arduino, camera and servos. To program this I used python with openCV library (pardon my hairy leg and a mess on the desk).

![Magic!](img\ezgif.com-gif-maker.gif)

### How it works

Image recognition script connects to the camera server in local network, grabs the frames and performs some processing. User can define which color values should be considered useful - in the example I set it to focus on the red color. 

From all the areas within the color range, only the ones above a certain threshold are selected and shown on the preview with blue bounds around them. After that I calculate the center of the biggest area and its offset to the center of the frame - shown with a green dot and a line.

The offset between the center of our area and the center of the screen (only X-axis at the moment) is sent through a socket connection to a second script, which is connected through a serial port with an Arduino controlling the servo where the camera is mounted.

The script upon receiving the data determines if it should tell the servo to move left/right which result in a camera trying to center itself on the followed object.