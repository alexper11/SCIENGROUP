#This file is the file executed by gunicorn, and deply the service that keep 
#online the service

from index import server as application
if __name__ =='__main__':
    application.run()