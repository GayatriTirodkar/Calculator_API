
def fibonacci_series(number):
	print number
	print "="*20
	fibonacci_list = []
	a = 0
	b = 1
	fibonacci_list.extend((a,b))
	while number > 0:
		c = a+b
		fibonacci_list.append(c)
		a = b
		b = c 
		number -= 1
	return fibonacci_list

