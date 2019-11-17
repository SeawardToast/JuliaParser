#!/usr/bin/env python3

# Class:      CS 4308 Section 1
# Term:       Fall 2019
# Name:       Daniel Skinner, Samuel Wood, Aidan Murphy
# Instructor: Deepa Muralidhar
# Project:    Deliverable 2 Parser - Python

import julia_lexer, enum, sys
from abc import ABC, abstractmethod


class Block:
    def __init__(self):
        self.statements = []

    def add(self, statement):
        if statement is None:
            print("ERROR: Null value exception in Block class.")
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


class Parser:
    def __init__(self, tokenlist):
        global tokens
        tokens = tokenlist

    def parse(self):
        statement = self.getStatement()

    def getStatement(self):
        token = self.seeNextToken()
        if token.getTokenType() == julia_lexer.TokenType.KEY_IF:
            statement = self.getIfStatement()
        

    def getNextToken(self):
        if not tokens:
            print("ERROR: IndexOutOfBounds. no more tokens.")
            sys.exit(1)
        return tokens.pop(0)
    def seeNextToken(self):
        if not tokens:
            print("ERROR: IndexOutOFBounds(Parser.SeeNextToken): No more tokens.")
            sys.exit(1)
        token = tokens.pop(0)
        tokens.insert(0, token)
        return token


