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

class Statement(ABC):
    @abstractmethod
    def exc(self):
        pass


class ArithmeticExpression(ABC):
    @abstractmethod
    def exc(self):
        pass


def parse(self, tokens):
    #just testing the use of the list of tokens passed from julia_lexer
    for token in tokens:
        type = token.getTokenType()
        if type is 0:
            print("ERROR: invalid character found. Code will not compile")
            sys.exit(1)
        #assignment statement
        if type is 1:
            id_name = token.getIdName()

