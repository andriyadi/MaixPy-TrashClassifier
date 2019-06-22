# MaixPy-TrashClassifier
A simple trash/waste classifier developed using [MaixPy](https://github.com/sipeed/MaixPy) (a MicroPython framework) to run on K210 MCU on Sipeed's Maix dev board.

I use this repo for doing live demo and talk at Pycon Thailand 2019, which I discussed about [AIoT: Intelligence on Low Power Microcontroller, with MicroPython](https://th.pycon.org/en/schedule/) 

## What does it do?
The MicroPython script ([`trash_classifier.py`](https://github.com/andriyadi/MaixPy-TrashClassifier/blob/master/trash_classifier.py)) will grab image from camera. Using prepared ML model (`trash.kmodel`), it can classify captured image as Plastic, Glass, or Other trash. Then display the captured image, inference result, and inference's frame/second on LCD.

Demo on [Youtube](https://youtu.be/x3vW4LiNaRM?t=1054)

## Prerequisites

* One of Sipeed Maix development board. I use Maix Go. May work for other boards.
* MaixPy. Please refer to MaixPy [docs](https://maixpy.sipeed.com/en/) for setting up development environment.
* Copy `trash.kmodel` model file to Maix board, either via microSD card or burn it to board's memory using [k-flash GUI tool](https://github.com/sipeed/kflash_gui). Make sure to adjust the code for loading the model.

## Credits

* Model is trained using dataset taken from [trashnet](https://github.com/garythung/trashnet) repo, and transfer learning from MobileNet arcitecture
