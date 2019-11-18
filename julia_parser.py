#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 2 Parser - Python

import julia_lexer, enum, sys
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
            ina = ord(a)
            index = intch - inta
        else:
            intbc = ord(ch)
            ba = 'A'
            intba = ord(ba)
            index = 26 + intbc - intba
        return index

    def fetch(self, ch):
        return Memory.mem[self.indexof(ch)]


class Iterator:

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


class AssignmentStatement(Statement):

    def __init__(self, var, expr):
        if var == None:
            raise ValueError('ID argument null')
        if expr == None:
            raise ValueError('ArithmeticExpression argument null')

        self.var = var
        self.expr = expr

    def execute(self):
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

        def execute(self):
            begin = self.it.getBegin().evaluate()
            end = self.it.getEnd().evaluate()
            ch = self.var.getchar()
            memory = Memory()
            while begin <= end:
                memory.store(ch, begin)
                self.block.execute()
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


    def execute(self):
        if self.expr.evaluate():
            self.blk1.execute()
        else:
            self.blk2.execute()

class WhileStatement(Statement):

    def __init__(self, expr, blk):
        if expr == None:
            raise ValueError('boolean expression argument null')
        if blk == None:
            raise ValueError('block argument null')
        self.expr = expr
        self.blk = blk

    def execute(self):
        while self.expr.evaluate():
            self.blk.execute()

class Parser:
    def __init__(self, tokenlist):
        global tokens
        tokens = tokenlist
        self.size = tokenlist.len()

    def parse(self):
        token = self.getNextToken()
        #function keyword
        if(token.getTokenType()!= 17):
            print("ERROR: syntax error on line" + (self.size - tokens.len()))
        token = self.getNextToken()
        #id value
        if (token.getTokenType() != 1):
            print("ERROR: syntax error on line" + (self.size - tokens.len()))
        functionName = token.getIdName()
        token = self.getNextToken()
        #open par
        if (token.getTokenType() != 24):
            print("ERROR: syntax error on line" + (self.size - tokens.len()))
        token = self.getNextToken()
        #close par
        if (token.getTokenType() != 25):
            print("ERROR: syntax error on line" + (self.size - tokens.len()))
        block = self.getBlock()
        token = self.getNextToken()
        if (token.getTokenType() != 23):
            print("ERROR: syntax error on line" + (self.size - tokens.len()))
        return Program(block)

    def getBlock(self):
        block = Block()
        token = self.seeNextToken()

    def getStatement(self):
        token = self.seeNextToken()
        if token.getTokenType() == julia_lexer.TokenType.KEY_IF:
            statement = self.getIfStatement()

    def getNextToken(self):
        if not tokens:
            print("no more tokens.")
            sys.exit(1)
        return tokens.pop(0)

    def seeNextToken(self):
        if not tokens:
            print("No more tokens.")
            sys.exit(1)
        token = tokens.pop(0)
        tokens.insert(0, token)
        return token


