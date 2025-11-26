def tea(p,finalstate=True):
	de = 0
	for i in p:
		if i == "(": de+= 1
		if i == ")": de-= 1
		if de < 0:
			print("ERR: MISMATCHED PARENTHESIS")
			return
	if de != 0:
		print("ERR: MISMATCHED PARENTHESIS")
		return

	halt = False

	stack1 = []
	stack2 = []

	def interpret(p, d=0):
		nonlocal halt, stack1, stack2

		def lencheck(n,cmd,t=False):
			nonlocal halt, stack1, stack2
			if t:
				if len(stack2) < n:
					halt = True
					print(f"ERR: COMMAND `{cmd}` REQUIRES AT LEAST {n} ITEM(S) ON SECONDARY STACK")
				return len(stack2) < n
			else:
				if len(stack1) < n:
					halt = True
					print(f"ERR: COMMAND `{cmd}` REQUIRES AT LEAST {n} ITEM(S) ON PRIMARY STACK")
				return len(stack1) < n

		built = ""
		built2 = ""
		
		cp = 0

		while cp < len(p):
			if halt: return

			if not (p[cp].isdigit() or p[cp] in ":%+-!*{}@"):
				print(f"ERR: INVALID COMMAND `{"\\n" if p[cp] == "\n" else p[cp]}`")
				halt = True
				return

			if p[cp].isdigit():
				built+= p[cp]
			elif built != "" and built.isdigit():
				stack1.append(int(built))
				built = ""
			
			if p[cp] == ":":
				if lencheck(1,":"): return
				stack1.append(stack1[-1])

			if p[cp] == "%":
				if lencheck(2,"%"): return
				b, a = stack1.pop(), stack1.pop()
				stack1.append(b)
				stack1.append(a)

			if p[cp] == "+":
				if lencheck(1,"+"): return
				stack1[-1]+= 1

			if p[cp] == "-":
				if lencheck(1,"-"): return
				if stack1[-1] == 0:
					print("ERR: CANNOT DECREMENT 0")
					return
					halt = True
				stack1[-1]-= 1

			if p[cp] == "!":
				if lencheck(1,"!"): return
				stack1.pop()

			if p[cp] == "*":
				cp+= 1
				if p[cp] != "(":
					print("ERR: EXPECTED `(` AFTER `*` COMMAND")
					halt = True
					return
				cp+= 1
				if p[cp] == ")":
					print("ERR: CODE BLOCK CANNOT BE EMPTY")
					halt = True
					return
				built2 = ""
				depth = 1
				while depth > 0:
					if p[cp] == "(": depth+= 1
					if p[cp] == ")": depth-= 1
					if depth > 0:
						built2 += p[cp]
					cp+= 1
					if depth == 0: break
				if lencheck(1,"*"): return
				times = stack1.pop()
				interpret(built2*times,d+1)
				continue

			if p[cp] == "@":
				cp+= 1
				if p[cp] != "(":
					print("ERR: EXPECTED `(` AFTER `@` COMMAND")
					halt = True
					return
				cp+= 1
				if p[cp] == ")":
					print("ERR: CODE BLOCK CANNOT BE EMPTY")
					halt = True
					return
				built2 = ""
				depth = 1
				while depth > 0:
					if p[cp] == "(": depth+= 1
					if p[cp] == ")": depth-= 1
					if depth > 0:
						built2 += p[cp]
					cp+= 1
					if depth == 0: break
				if lencheck(1,"@",t=True): return
				while stack2[-1] > 0:
					interpret(built2,d+1)
					if lencheck(1,"@",t=True): return
				continue

			if p[cp] == "{":
				if lencheck(1,"{"): return
				stack2.append(stack1.pop())

			if p[cp] == "}":
				if lencheck(1,"}",True): return
				stack1.append(stack2.pop())

			cp+= 1

		if built != "" and built.isdigit():
			stack1.append(int(built))

		if d==0 and not halt and finalstate: print(f"FINAL STATE:\n{stack1} {stack2}")

	interpret(p)
