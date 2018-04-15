import tornado.ioloop
import tornado.web 
import tornado.httpserver
import tornado.options
import re
import json
import worker
from rq import Queue
from run_worker import conn
'''
	create redis object
'''

#accept options from command line
from tornado.options import define, options 
define("port",default=8000,help="run on the given port",type=int)


class MainHandler(tornado.web.RequestHandler):
	'''
		The index / main page for the web application 
	'''
	def get(self):
		self.write("Basic and Simple Calculator")

class AdditionHandler(tornado.web.RequestHandler):
	'''
		The method to process addition operation
	'''
	def post(self):
		self.write("Adding the array of integers")
		body = json.loads(self.request.body)
		total = sum(body["numbers"])
		self.write("\n The received list of numbers is: "+ str(body["numbers"])+'\nThe total is: '+str(total))

class MultiplicationHandler(tornado.web.RequestHandler):
	'''
		The method to process multiplication operation
	'''
	def post(self):
		self.write("Multiplying the array of integers")
		body = json.loads(self.request.body)
		product = reduce(lambda x,y : x*y,body["numbers"])
		self.write("\n The received list of numbers is: "+ str(body["numbers"]) +"\nThe product is: "+str(product))

class DivisionHandler(tornado.web.RequestHandler):
	'''
		The method to process division operation
	'''
	def post(self):
		self.write("Dividing the list of integers by the minimum number in the list / by the number entered")
		body = json.loads(self.request.body)
		input_arr =  body["numbers"]
		minimum = body.get('divisor',min(input_arr))
		minimum = (1,minimum) [bool(minimum)]
		division = [number / minimum for number in input_arr]
		self.write('\nThe list is divided by '+str(minimum)+'\n The output list is : '+str(division))

class SubtractionHandler(tornado.web.RequestHandler):
	'''
		The method to process subtraction operation 
	'''
	def post(self):
		self.write("Subtracting numbers from a list")
		body = json.loads(self.request.body)
		input_arr =  body["numbers"]
		minimum = body.get('subtract_by',min(input_arr))
		subtract = [number - minimum for number in input_arr]
		self.write('\nThe list is subtracted by '+str(minimum)+'\n The output list is : '+str(subtract))



class ModuloDivisionHandler(tornado.web.RequestHandler):
	def post(self):
		self.write("Modulo division of list of integers by the minimum number in the list / by the number entered")
		body = json.loads(self.request.body)
		input_arr =  body["numbers"]
		minimum = body.get('divisor',min(input_arr))
		minimum = (1,minimum) [bool(minimum)]
		modulo = [number % minimum for number in input_arr]
		self.write('\nThe list is divided by '+str(minimum)+'\n The output list is : '+str(modulo))

class FibonacciHandler(tornado.web.RequestHandler):
	def post(self):
		self.write("Print fibonacci series")
		body = json.loads(self.request.body)
		number = body["number"]
		q = Queue(connection=conn)
		job = q.enqueue(worker.fibonacci_series, number)
		self.write("\nJob created at job_id:"+str(job.id))
		print job.return_value


def make_app():
	'''
		List of discrete request handlers /  routes in the web application
	'''
	return tornado.web.Application([
			(r"/",MainHandler),
			(r"/add",AdditionHandler),
			(r"/multiply",MultiplicationHandler),
			(r"/divide", DivisionHandler),
			(r"/modulo", ModuloDivisionHandler),
			(r"/subtract", SubtractionHandler),
			(r"/fibonacci", FibonacciHandler)
		])

if __name__ == "__main__":
	tornado.options.parse_command_line() 
	app = make_app()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()