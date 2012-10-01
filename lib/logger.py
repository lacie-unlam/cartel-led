import logging

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', 
					datefmt='%d/%m/%Y %H:%M:%S', 
					filename='./log/cartel-led.log', filemode='w', 
					level=logging.INFO)