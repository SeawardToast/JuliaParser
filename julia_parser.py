#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 2 Parser - Python

import julia_lexer, sys, enum
from abc import ABC, abstractmethod

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
        for statement in self.statements:
            statement.exc()


class Statement(ABC):
    @abstractmethod
    def exc(self):
        pass


class ArithmeticExpression(ABC):
    @abstractmethod
    def exc(self):
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
        memory = Memory()
        memory.store( self.var.getchar(), self.expr.evaluate())




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

        if blk1 == None or blk2 == None:
            raise ValueError('null block argument')

        self.expr = expr
        self.blk1 = blk1
        self.blk2 - blk2


    def exc(self):
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
        while self.expr.evaluate():
            self.blk.exc()


class PrintStatement(Statement):
    def __init__(self, expression):
        if expression is None:
            raise ValueError('null arithmetic expression')
        self.expression = expression

    def exc(self):
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
        eval = 0
        if self.operations == ArOps.OP_ADD:
            eval = self.exp1.evaluate() + self.exp2.evaluate()
        elif self.operations == ArOps.OP_SUB:
            eval = self.exp1.evaluate() - self.exp2.evaluate()
        elif self.operations == ArOps.OP_MUL:
            eval = self.exp1.evaluate() * self.exp2.evaluate()
        elif self.operations == ArOps.OP_DIV:
            eval = self.exp1.evaluate() / self.exp2.evaluate()
        elif self.operations == ArOps.OP_MOD:
            eval = self.exp1.evaluate() % self.exp2.evaluate()
        elif self.operations == ArOps.OP_INV:
            eval = self.exp2.evaluate() / self.exp1.evaluate()
        elif self.operations == ArOps.OP_EXP:
            eval = self.exp1.evaluate() ^ self.exp2.evaluate()
        return eval

class Program:
    def __init__(self, block):
        if block == None:
            raise ValueError('null block argument')
        self.block = block

    def exc(self):
        self.block.exc()


class Parser:
    def __init__(self, tokenlist):
        global tokens
        tokens = tokenlist
        self.size = tokenlist.len()

    def parse(self):
        token = self.getNextToken()
        #function keyword
        checkToken(token.getTokenType(), 17) #assert method token type
        #assert id value possibly
        functionName = token.getIdName()
        token = self.getNextToken()
        checkToken(token.getTokenType(), 24) #assert open parentheses token type
        token = self.getNextToken()
        checkToken(token.getTokenType(), 25) #assert closed parentheses token type

        block = self.getBlock()
        token = self.getNextToken()
        checkToken(token.getTokenType(), 23) #assert token end type
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
       tokType = token.getTokenType()
       return (tokType == 1 or
               tokType == 21 or
               tokType == 19 or
               tokType == 18 or
               tokType == 20)

    def getStatement(self):
        token = self.seeNextToken()
        tokType = token.getTokenType()
        if tokType == julia_lexer.TokenType.KEY_IF:
            statement = self.getIfStatement()
        elif tokType == julia_lexer.TokenType.KEY_WHILE:
            statement = self.getWhileStatement
        elif tokType == julia_lexer.TokenType.KEY_PRINT:
            statement = self.getPrintStatement()
        elif tokType == julia_lexer.TokenType.ID:
            statement = self.getAssignmentStatement()
        elif tokType == julia_lexer.TokenType.KEY_FOR:
            statement = self.getForStatement()
        else:
            raise ParserException('got ', token.getTokenType, 'invalid statement')
        return statement

    def getAssignmentStatement(self):
        var = self.getId()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.OP_ASSIGN)
        expr = self.getArithmeticExpression()
        return AssignmentStatement(var, expr)

    def getPrintStatement(self):
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_PRINT)
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.PAREN_OPEN)
        expr = self.getArithmeticExpression()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.PAREN_CLOSE)
        return PrintStatement(expr)

    def getForStatement(self):
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_FOR)
        id1 = self.getId()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.OP_ASSIGN)
        it = self.getIterStatement()
        block = Block()
        block = self.getBlock()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_END)
        return ForStatement(id1, it, block)

    def getIfStatement(self):
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_IF)
        expr = self.getBooleanExpression()
        block1 = self.getBlock()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_ELSE)
        block2 = self.getBlock()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_END)
        return IfStatement(expr, block1, block2)

    def getWhileStatement(self):
        token = self.seeNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_WHILE)
        expr = self.getBooleanExpression()
        block = Block()
        block = self.getBlock()
        token = self.getNextToken()
        self.checkToken(token, julia_lexer.TokenType.KEY_END)
        return WhileStatement(expr, block)

    def getArithmeticExpression(self):
        token = self.seeNextToken()
        if token.getTokenType() == julia_lexer.TokenType.ID:
            expr = self.getId()
        elif token.getTokenType() == julia_lexer.TokenType.INT:
            expr = self.getLiteralInteger()
        else:
            expr = self.getBinaryExpression()
        return expr

    def getBinaryExpression(self):
        op = self.getArithmeticOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BinaryExpression(op, expr1, expr2)

    def getArithmeticOperator(self):
        token = self.getNextToken()
        tokType = token.getTokenType()
        if tokType == julia_lexer.TokenType.OP_ADD:
            op = ArOps.OP_ADD
        if tokType == julia_lexer.TokenType.OP_SUB:
            op = ArOps.OP_SUB
        if tokType == julia_lexer.TokenType.OP_MUL:
            op = ArOps.OP_MUL
        if tokType == julia_lexer.TokenType.OP_DIV:
            op = ArOps.OP_DIV
        else:
            raise ParserException('expectex arithmetic operator, did not get one')
        return op


    def getLiteralInteger(self):
        token = self.getNextToken()
        if token.getTokenType() != julia_lexer.TokenType.INT:
            raise ('integer expected but not here')
        value = int(token.getLexeme())
        return LiteralInteger(value)

    def getId(self):
        token = self.getNextToken()
        if token.getTokenType() != julia_lexer.TokenType.ID:
            raise ParserException('identifier expected but did not get')
        return Id(julia_parser.Token.getLexeme()[0])

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
        tokType = token.getTokenType()
        if tokType == julia_lexer.TokenType.OP_EQ:
            op = boolOps.OP_EQ
        elif tokType == julia_lexer.TokenType.OP_NE:
            op = boolOps.OP_NE
        elif tokType == julia_lexer.TokenType.OP_GT:
            op = boolOps.OP_GT
        elif tokType == julia_lexer.TokenType.OP_GE:
            op = boolOps.OP_GE
        elif tokType == julia_lexer.TokenType.OP_LT:
            op = boolOps.OP_LT
        elif tokType == julia_lexer.TokenType.OP_LE:
            op = boolOps.OP_LE
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
        token = tokens.pop()
        tokens.insert(0, token)
        return token


    def checkToken(self, tok, toktype):
        assert(tok is not None)
        assert(toktype is not None)
        if tok.getTokenType is not toktype:
            raise ParserException(toktype, 'expected, got' tok, 'instead')


