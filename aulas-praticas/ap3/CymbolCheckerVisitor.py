from antlr4 import *
from autogen.CymbolParser import CymbolParser 
from autogen.CymbolVisitor import CymbolVisitor

class Type:
	VOID = "void"
	INT = "int"
	BOOLEAN = "boolean"
	STRING = "string"
	FLOAT = "float"


class CymbolCheckerVisitor(CymbolVisitor):
	id_values = {}

	def visitIntExpr(self, ctx:CymbolParser.IntExprContext):
		return Type.INT

	def visitStringExpr(self, ctx:CymbolParser.StringExprContext):
		return Type.STRING

	def visitFloatExpr(self, ctx:CymbolParser.FloatExprContext):
		return Type.FLOAT

	def visitBooleanExpr(self, ctx:CymbolParser.BooleanExprContext):
		return Type.BOOLEAN

	def visitFormTypeInt(self, ctx:CymbolParser.FormTypeIntContext):
		return Type.INT

	def visitFormTypeVoid(self, ctx:CymbolParser.FormTypeVoidContext):
		return Type.VOID

	def visitFormTypeBoolean(self, ctx:CymbolParser.FormTypeBooleanContext):
		return Type.BOOLEAN

	def visitFormTypeString(self, ctx:CymbolParser.FormTypeStringContext):
		return Type.STRING

	def visitFormTypeFloat(self, ctx:CymbolParser.FormTypeFloatContext):
		return Type.FLOAT

	#To test
	def visitReturnStat(self, ctx:CymbolParser.ReturnStatContext):
		init = Type.VOID
		if ctx.expr() != None:
			init = self.visit(ctx.expr())
		return init

	#To test
	def visitIfElseStat(self, ctx:CymbolParser.IfElseStatContext):
		ifType = self.visit(ctx.ifStat())
		elseType = None
		result = ifType
		if ctx.elseStat() != None:
			elseType = self.visit(ctx.elseStat())
			if not (ifType == elseType):
				result = Type.VOID
				print("Mensagem de erro 1...")
				exit(1)
		return result

	# To test
	def visitIfElseExprStat(self, ctx:CymbolParser.IfElseExprStatContext):
		result = self.visitChildren(ctx)
		if result == None:
			result = Type.VOID
		return result

	# To test
	def visitEqExpr(self, ctx:CymbolParser.EqExprContext):
		left = self.visit(ctx.expr()[0])
		right= self.visit(ctx.expr()[1])
		if left == Type.BOOLEAN and right == Type.BOOLEAN:
			return Type.BOOLEAN
		elif left == Type.STRING and right == Type.STRING:
			return Type.BOOLEAN
		elif left == Type.FLOAT and right == Type.FLOAT:
			return Type.BOOLEAN
		elif left == Type.INT and right == Type.INT:
			return Type.BOOLEAN
		elif left == Type.INT and right == Type.FLOAT:
			return Type.BOOLEAN
		elif left == Type.FLOAT and right == Type.INT:
			return Type.BOOLEAN
		else:
			# TODO text of error
			result = Type.VOID
			print("Mensagem de erro 1...")
			exit(1)
		return result

	# To test
	def visitOrAndExpr(self, ctx:CymbolParser.OrAndExprContext):
		result = None
		left = self.visit(ctx.expr()[0])
		right= self.visit(ctx.expr()[1])
		if left == Type.BOOLEAN and right == Type.BOOLEAN:
			return Type.BOOLEAN
		else:
			result = Type.VOID
			print("Mensagem de erro 1...")
			exit(1)
		return result

	# To test
	def visitSignedExpr(self, ctx:CymbolParser.SignedExprContext):
		tyype = self.visit(ctx.expr())
		if tyype == Type.INT:
			return Type.INT
		elif tyype == Type.FLOAT:
			return Type.FLOAT
		else:
			result = Type.VOID
			# TODO error msg
			print("Mensagem de erro 1...")
			exit(1)
		return result

	# To test 
	def visitNotExpr(self, ctx:CymbolParser.NotExprContext):
		tyype = self.visit(ctx.expr())
		if tyype == Type.BOOLEAN:
			return Type.BOOLEAN
		else:
			result = Type.VOID
			# TODO error msg
			print("Mensagem de erro 1...")
			exit(1)
		return result

	# To test
	def visitMulDivExpr(self, ctx:CymbolParser.MulDivExprContext):
		left = self.visit(ctx.expr()[0])
		right= self.visit(ctx.expr()[1])
		if left == Type.FLOAT and right == Type.FLOAT:
			return Type.FLOAT
		elif left == Type.INT and right == Type.INT:
			return Type.INT
		elif left == Type.INT and right == Type.FLOAT:
			return Type.FLOAT
		elif left == Type.FLOAT and right == Type.INT:
			return Type.FLOAT
		else:
			# TODO text of error
			result = Type.VOID
			print("Mensagem de erro 1...")
			exit(1)
		return result

	# To test
	def visitComparisonExpr(self, ctx:CymbolParser.ComparisonExprContext):
		left = self.visit(ctx.expr()[0])
		right= self.visit(ctx.expr()[1])
		if (left == Type.INT or left == Type.FLOAT) and (right == Type.INT or right == Type.FLOAT):
			return Type.BOOLEAN
		else:
			# TODO text of error
			result = Type.VOID
			print("Mensagem de erro 1...")
			exit(1)
		return result

	#Done
	def visitVarDecl(self, ctx:CymbolParser.VarDeclContext):
		var_name = ctx.ID().getText()
		tyype = ctx.tyype().getText()
		# print("tyype = " + tyype)
		
		if (tyype == Type.VOID):
			result = Type.VOID
			print("Mensagem de erro 1...")
			exit(1)
		else:
			if ctx.expr() != None:
				init = ctx.expr().accept(self)
				# print("init = " + init)
				if init != tyype:
					print("Mensagem de erro 2...")
					exit(2)

			result = tyype
			self.id_values[var_name] = tyype

		print("saved variable " + var_name + " of type " + tyype)
		return result

	#To test
	def visitAddSubExpr(self, ctx:CymbolParser.AddSubExprContext):
		left = ctx.expr()[0].accept(self)
		right = ctx.expr()[1].accept(self)

		if left == Type.INT and right == Type.INT:
			result = Type.INT
		elif left == Type.FLOAT and right == Type.FLOAT:
			return Type.FLOAT
		elif left == Type.INT and right == Type.FLOAT:
			return Type.FLOAT
		elif left == Type.FLOAT and right == Type.INT:
			return Type.FLOAT
		elif ctx.op.getText() == "+" and left == Type.STRING and right == Type.INT or right == Type.FLOAT or right == Type.STRING or right == Type.BOOLEAN:
			return Type.STRING
		elif ctx.op.getText() == "+" and right == Type.STRING and left == Type.INT or left == Type.FLOAT or left == Type.STRING or left == Type.BOOLEAN:
			return Type.STRING
		else:
			result = Type.VOID
			print("Mensagem de erro 3...")
			exit()
		print("addition or subtraction of " + left + " " + right + " that results in a " + result)
		return result


	def aggregateResult(self, aggregate:Type, next_result:Type):
		return next_result if next_result != None else aggregate
