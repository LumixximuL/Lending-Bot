#Documentation module
#Taylor Webber

import time
import configure

def document_trans(type, period, currency, rate, amount, id):
        #Document trade in text file
        output_file = open(configure.file, "a")
        output_file.write(time.strftime("%a, %d %b %Y %H:%M:%S    ", time.localtime()))
        output_file.write("{0:10}".format(type))
        output_file.write("{0:9}".format(str(period)))
        output_file.write("{0:8}".format(currency))
        output_file.write("{0:8}".format(str(rate)))
        output_file.write("{0:16}".format(str(amount)))
        output_file.write(str(str(id)))
        output_file.write("\n")
        output_file.close()