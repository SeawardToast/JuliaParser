#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 2 Parser - Python

import julia_lexer, sys, enum
from abc import ABC, abstractmethod

class ParserException(Exception):
    pass


class Memory:
    mem = [0]*52
    def store(self, ch, value):
        Memory.mem[self.indexof(ch)] = value
    def indexof(self, ch):
        if not ch.isalpha():
            raise ValueError('identifier argument invalid')
        if ch.islower():
            intch = ord(ch)      #ord returns unicode integer, A is 65, a is 97
            a = 'a'
            inta = ord(a)
            index = intch - inta
        else:
            intbc = ord(ch)
            ba = 'A'
            intba = ord(ba)
            index = 26 + intbc - intba
        return index

    def fetch(self, ch):
        return Memory.mem[self.indexof(ch)]


class It:

    global it
    it =[]

    def __init__(self, expr1, expr2):
        if expr1 is None or expr2 is None:
            raise ValueError('arithmetic expression argument null')
        self.expr1 = expr1
        self.expr2 = expr2
        it.append(self.expr1)
        it.append(self.expr2)

    def getBegin(self):
        return it[0]

    def getEnd(self):
        return it[1]


class Block:
    def __init__(self):
        self.statements = []

    def add(self, statement):
        if statement is None:
            print("ERROR: NoStatement Exception: Null statement value in block.")
            sys.exit(1);
        self.statements.append(statement)

    def exc(self):
        print('<Block>: ')
        for statement in self.statements:
            statement.exc()


class Statement(ABC):
    @abstractmethod
    def exc(self):
        pass


class ArithmeticExpression(ABC):
    @abstractmethod
    def evaluate(self):
        pass


class LiteralInteger(ArithmeticExpression):

    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value


class AssignmentStatement(Statement):

    def __init__(self, var, expr):
        if var == None:
            raise ValueError('ID argument null')
        if expr == None:
            raise ValueError('ArithmeticExpression argument null')

        self.var = var
        self.expr = expr

    def exc(self):
        print("<AssignmentStatement>")
        memory = Memory()
        memory.store( self.var.getChar(), self.expr.evaluate())




class ForStatement(Statement):

    def __init__(self, var, it, block):

        if it is None:
            raise ValueError('iterator argument is null')
        if block is None:
            raise ValueError('block argument is null')

        self.it = it
        self.var = var
        self.block = block

        def exc(self):
            print("<ForStatement>")
            begin = self.it.getBegin().evaluate()
            end = self.it.getEnd().evaluate()
            ch = self.var.getchar()
            memory = Memory()
            while begin <= end:
                memory.store(ch, begin)
                self.block.exc()
                begin +1

class IfStatement(Statement):

    def __init__(self, expr, blk1, blk2):
        if expr == None:
            raise ValueError('boolean expression null')

        if blk1 == None:
            raise ValueError('null block argument')

        if blk2 != None:
            self.expr = expr
            self.blk1 = blk1
            self.blk2 = blk2
        else:
            self.expr = expr
            self.blk1 = blk1

    def exc(self):
        print("<IfStatement>")
        if self.expr.evaluate():
            self.blk1.exc()
        else:
            self.blk2.exc()

class WhileStatement(Statement):

    def __init__(self, expr, blk):
        if expr == None:
            raise ValueError('boolean expression argument null')
        if blk == None:
            raise ValueError('block argument null')
        self.expr = expr
        self.blk = blk

    def exc(self):
        print("<WhileStatement>")
        while self.expr.evaluate():
            self.blk.exc()


class PrintStatement(Statement):
    def __init__(self, expression):
        if expression is None:
            raise ValueError('null arithmetic expression')
        self.expression = expression

    def exc(self):
        print("<PrintStatement>")
        print(self.expression.evaluate())


class boolOps(enum.Enum):
    OP_LE = 4
    OP_LT = 5
    OP_GE = 6
    OP_GT = 7
    OP_EQ = 8
    OP_NE = 9


class BooleanExpression:
    def __init__(self, operation, exp1, exp2):
        if operation is None:
            raise ValueError('null relational operator in a boolean expression')
        if exp1 is None or exp2 is None:
            raise ValueError('null arithmetic expression in a boolean expression')
        self.operation = operation
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self):
        print("<BooleanExpression>")
        if self.operation == boolOps.OP_LE:
            eval = self.exp1.evaluate() <= self.exp2.evaluate()
        elif self.operation == boolOps.OP_LT:
            eval = self.exp1.evaluate() < self.exp2.evaluate()
        elif self.operation == boolOps.OP_GE:
            eval = self.exp1.evaluate() >= self.exp2.evaluate()
        elif self.operation == boolOps.OP_GT:
            eval = self.exp1.evaluate() > self.exp2.evaluate()
        elif self.operation == boolOps.OP_EQ:
            eval = self.exp1.evaluate() == self.exp2.evaluate()
        elif self.operation == boolOps.OP_NE:
            eval = self.exp1.evaluate() == self.exp2.evaluate()
        return eval


class ArOps(enum.Enum):
    OP_ADD = 10
    OP_SUB = 11
    OP_MUL = 12
    OP_DIV = 13
    OP_MOD = 14
    OP_INV = 15
    OP_EXP = 16


class BinaryExpression(ArithmeticExpression):
    def __init__(self, operation, exp1, exp2):
        if operation is None:
            raise ValueError('null arithmetic operator in a arithmetic expression')
        if exp1 is None or exp2 is None:
            raise ValueError('null arithmetic expression in a arithmetic expression')
        self.operation = operation
        self.exp1 = exp1
        self.exp2 = exp2

    def evaluate(self):
        print("<BinaryExpression>")
        eval = 0
        if self.operation == ArOps.OP_ADD:
            eval = self.exp1.evaluate() + self.exp2.evaluate()
        elif self.operation == ArOps.OP_SUB:
            eval = self.exp1.evaluate() - self.exp2.evaluate()
        elif self.operation == ArOps.OP_MUL:
            eval = self.exp1.evaluate() * self.exp2.evaluate()
        elif self.operation == ArOps.OP_DIV:
            eval = self.exp1.evaluate() / self.exp2.evaluate()
        elif self.operation == ArOps.OP_MOD:
            eval = self.exp1.evaluate() % self.exp2.evaluate()
        elif self.operation == ArOps.OP_INV:
            eval = self.exp2.evaluate() / self.exp1.evaluate()
        elif self.operation == ArOps.OP_EXP:
            eval = self.exp1.evaluate() ^ self.exp2.evaluate()
        return eval

class Program:
    def __init__(self, block):
        if block == None:
            raise ValueError('null block argument')
        self.block = block

    def exc(self):
        print('<Program>: ')
        self.block.exc()
        print('\n')


class Id(ArithmeticExpression):

    def __init__(self, ch):
        if not ch.isalpha():
            raise ValueError('invalid identifier argument')
        self.ch = ch

    def getChar(self):
        return self.ch

    def evaluate(self):
        memory = Memory()
        return memory.fetch(self.ch)


class Parser:
    def __init__(self, tokenlist):
        global tokens
        tokens = tokenlist
        self.size = len(tokenlist)

    def parse(self):
        token = self.getNextToken()
        #function keyword
        self.checkToken(token.getTokenValue(), 17) #assert method token type
        #assert id value possibly
        token = self.getNextToken()
        functionName = token.getIdName()
        token = self.getNextToken()
        self.checkToken(token.getTokenValue(), 24) #assert open parentheses token type
        token = self.getNextToken()
        self.checkToken(token.getTokenValue(), 25) #assert closed parentheses token type

        block = self.getBlock()
        token = self.getNextToken()
        self.checkToken(token.getTokenValue(), 23) #assert token end type
        return Program(block)

    def getBlock(self):
        block = Block()
        token = self.seeNextToken()
        while self.isValidStartOfStatement(token):
            statement = self.getStatement()
            block.add(statement)
            token = self.seeNextToken()
        return block

    def isValidStartOfStatement(self, token):
        assert (token is not None)
        tokType = token.getTokenValue()
        return (tokType == 1 or
                tokType == 21 or
                tokType == 19 or
                tokType == 18 or
                tokType == 20)

    def getStatement(self):
        token = self.seeNextToken()
        tokType = token.getTokenValue()
        if tokType == 21:
            statement = self.getIfStatement()
        elif tokType == 19:
            statement = self.getWhileStatement
        elif tokType == 18:
            statement = self.getPrintStatement()
        elif tokType == 1:
            statement = self.getAssignmentStatement()
        elif tokType == 20:
            statement = self.getForStatement()
        else:
            raise ParserException('got ', token, 'invalid statement')
        return statement

    def getAssignmentStatement(self):
        var = self.getId()
        token = self.getNextToken()
        tokValue = token.getTokenValue()
        self.checkToken(tokValue, 3)
        expr = self.getArithmeticExpression()
        return AssignmentStatement(var, expr)

    def getPrintStatement(self):
        token = self.getNextToken()
        #Checks to see if the token is the print key.
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 18)
        #Checks to see if the token is an open parenthesis.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 24)
        #ArithmeticExpression because minimal form of julia contains only integers.
        expr = self.getArithmeticExpression()
        #Checks to see if the token is a close parenthesis.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 25)

        return PrintStatement(expr)

    def getForStatement(self):
        #Makes sure the token is the for key.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 20)

        id1 = self.getId()
        #checks token for assign operator.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 3)
        #statement within for loop.
        it = self.getIterStatement()
        #for loop block
        block = Block()
        block = self.getBlock()
        #checks token for end key.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 23)
        return ForStatement(id1, it, block)

    def getIfStatement(self):
        #checks token for if key.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 21)
        #if expression.
        expr = self.getBooleanExpression()
        #if loop block
        block1 = self.getBlock()
        #checks token for else key.
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        if tokVal == 22:
            #else loop block
            block2 = self.getBlock()
            token = self.getNextToken()
            tokVal = token.getTokenValue()
            self.checkToken(tokVal, 23)
        else:
            self.checkToken(tokVal, 23)
            block2 = None
        return IfStatement(expr, block1, block2)

    def getWhileStatement(self):
        #checks for while key.
        token = self.seeNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 19)
        #gets while expression.
        expr = self.getBooleanExpression()
        #gets while loop block.
        block = self.getBlock()
        #checks for end of while loop
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        self.checkToken(tokVal, 23)
        return WhileStatement(expr, block)

    def getArithmeticExpression(self):
        token = self.seeNextToken()
        tokVal = token.getTokenValue()
        if tokVal == 1:
            expr = self.getId()
        elif tokVal == 2:
            expr = self.getLiteralInteger()
        else:
            expr = self.getBinaryExpression()
        return expr

    def isArithmeticOperator(self, b):
        assert (b is not None)
        tokType = b.getTokenValue()
        return (tokType == 10 or
                tokType == 11 or
                tokType == 12 or
                tokType == 13 or
                tokType == 14 or
                tokType == 15 or
                tokType == 16)

    def getBinaryExpression(self):
        op = self.getArithmeticOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BinaryExpression(op, expr1, expr2)

    def getArithmeticOperator(self):
        token = self.getNextToken()
        tokType = token.getTokenValue()
        if tokType == 10:
            op = ArOps.OP_ADD
        elif tokType == 11:
            op = ArOps.OP_SUB
        elif tokType == 12:
            op = ArOps.OP_MUL
        elif tokType == 13:
            op = ArOps.OP_DIV
        elif tokType == 14:
            op = ArOps.OP_MOD
        elif tokType == 15:
            op = ArOps.OP_INV
        elif tokType == 16:
            op = ArOps.OP_EXP
        else:
            raise ParserException('expected arithmetic operator, did not get one')
        return op


    def getLiteralInteger(self):
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        if tokVal != 2:
            raise ('integer expected but not here', tokVal)
        value = token.getIntValue()
        return LiteralInteger(value)

    def getId(self):
        token = self.getNextToken()
        tokVal = token.getTokenValue()
        if tokVal != 1:
            raise ParserException('identifier expected but did not get')
        tokName = token.getIdName()
        return Id(tokName)

    def getIterStatement(self):
        expr1 = self.getArithmeticExpression()
        tok = self.getNextToken()
        self.checkToken(tok, 26) #assert colon token type
        expr2 = self.getArithmeticExpression()
        return It(expr1, expr2)

    def getBooleanExpression(self):
        op = self.getRelationalOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BooleanExpression(op, expr1, expr2)

    def getRelationalOperator(self):
        token = self.getNextToken()
        tokType = token.getTokenValue()
        if tokType == 4:
            op = boolOps.OP_LE
        elif tokType == 5:
            op = boolOps.OP_LT
        elif tokType == 6:
            op = boolOps.OP_GE
        elif tokType == 7:
            op = boolOps.OP_GT
        elif tokType == 8:
            op = boolOps.OP_EQ
        elif tokType == 9:
            op = boolOps.OP_NE
        else:
            raise ParserException('relational operator expected but did not get')
        return op

    def getNextToken(self):
        if not tokens:
            print("no more tokens.")
            sys.exit(1)
        return tokens.pop(0)

    def seeNextToken(self):
        if not tokens:
            print("No more tokens.")
            sys.exit(1)
        return tokens[0]
    def checkToken(self, tok, toktype):
        assert(tok is not None)
        assert(toktype is not None)
        if tok is not toktype:
            raise ParserException(toktype, 'expected ', tok, 'instead')