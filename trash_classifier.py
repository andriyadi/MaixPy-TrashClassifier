import sensor, image, lcd, time
import KPU as kpu
from fpioa_manager import fm
from board import board_info
from Maix import GPIO

# Define GPIO to light up the LEDs
fm.register(board_info.LED_B, fm.fpioa.GPIO0)
led_plastic=GPIO(GPIO.GPIO0,GPIO.OUT)
fm.register(board_info.LED_G, fm.fpioa.GPIO1)
led_glasss=GPIO(GPIO.GPIO1,GPIO.OUT)
fm.register(board_info.LED_R, fm.fpioa.GPIO2)
led_other=GPIO(GPIO.GPIO2,GPIO.OUT)

# Change this if you're confident enough
THRESHOLD = 0.3

# Init camera sensor
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_windowing((224, 224))
sensor.set_vflip(0)
sensor.set_hmirror(False)
sensor.run(1)

# Init LCD
lcd.init(freq=15000000)
lcd.clear()
lcd.draw_string(100,96,"Waste Classifier")
lcd.draw_string(100,112,"Loading Models...")

# Classification labels
labels=['glass', 'other', 'plastic']

# Load Model, either from memory or SD Card
# task = kpu.load('/sd/models/trash.kmodel')
task = kpu.load(0x00500000)

clock = time.clock()

allImg = image.Image()

def lightUpLed(classIdx):
    # Should be cleverer than this, but it does its job for now
    led_plastic.value(0)
    led_glasss.value(0)
    led_other.value(0)

    if (classIdx == 0):
        led_plastic.value(1)
    if (classIdx == 1):
        led_glasss.value(1)
    if (classIdx == 2):
        led_other.value(1)


while(True):

    # Get image from camera
    img = sensor.snapshot()
    clock.tick()

    # Inference
    fmap = kpu.forward(task, img)
    fps = clock.fps()

    # Get inference result and biggest probabiltity
    plist = fmap[:]
    pmax = max(plist)

    label_text = ""
    if pmax > THRESHOLD:
        max_index=plist.index(pmax)	
        label_text = "{:.1f}%: {}".format(pmax*100, labels[max_index].strip())
    else:
        label_text = "Unknown"

    lightUpLed(max_index)
    
    # Display image from camera
    allImg.draw_image(img, 0, 0)
    allImg.draw_rectangle(0, 224, 320, (240-224), (0,0,0), 1, True)
    lcd.display(allImg, oft=(0, 0))

    # Display classification result
    lcd.draw_string(2, 224, label_text)

    # Display FPS
    lcd.draw_string((224 + 10), 10, "FPS:")
    lcd.draw_string(224+10, 30, "{0:.2f}".format(fps))
    
a = kpu.deinit(task)