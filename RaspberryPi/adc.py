class adc(chan, vref):
	import RPi.GPIO as GPIO

	# SPI pins
	SPICLK = 18
	SPIMISO = 23
	SPIMOSI = 24
	SPICS = 25

	# setup the SPI interface pins
	GPIO.setup(SPIMOSI, GPIO.OUT)
	GPIO.setup(SPIMISO, GPIO.IN)
	GPIO.setup(SPICLK, GPIO.OUT)
	GPIO.setup(SPICS, GPIO.OUT)
	
	adcnum = chan
	vref = vref
	
	GPIO.setmode(GPIO.BCM)

	def voltage():
		return raw() * vref / 1023

	def raw():
		if ((adcnum > 7) or (adcnum < 0)):
    		return -1
    	GPIO.output(SPICS, True)

    	GPIO.output(SPICLK, False)  # start clock low
    	GPIO.output(SPICS, False)     # bring CS low

		commandout = adcnum
        commandout |= 0x18  # start bit + single-ended bit
        commandout <<= 3    # we only need to send 5 bits here
        for i in range(5):
    		if (commandout & 0x80):
        		GPIO.output(SPIMOSI, True)
            else:
                GPIO.output(SPIMOSI, False)
                commandout <<= 1
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)

        adcout = 0
		
        # read in one empty bit, one null bit and 10 ADC bits
        for i in range(12):
                GPIO.output(SPICLK, True)
                GPIO.output(SPICLK, False)
                adcout <<= 1
                if (GPIO.input(SPIMISO)):
                        adcout |= 0x1

        GPIO.output(SPICS, True)
        
        adcout >>= 1       # first bit is 'null' so drop it
		
        return adcout




