import logging

FORMAT = '%(name)s - %(levelname)s - %(message)s'
FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(filename='app.log', filemode='a', format=FORMAT)

for i in range(7):
    print(i)
    if i==5:
        logging.warning('This will get logged to a file')
    else:
        logging.error("todo bien")