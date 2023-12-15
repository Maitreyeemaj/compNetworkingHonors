# quiz project SERVER
# Authors: Maitreyee Majumdar, Sana Hasan, and Majd Omari
# created 11/13/2023
from socket import *
import threading  # Import the threading module
import random

serverPort = 12000  # initializing the server port
serverSocket = socket(AF_INET, SOCK_STREAM)  # create socket
serverSocket.bind((gethostname(), serverPort))  # binding to the server
# bind socket to port/address

# initialize server quiz information here, before listening for a connection
# variables
truemsg = "1"
falsemsg = "0"
menu = 0

# login info dictionary
users = {
    "Sana": "frog",
    "Majd": "password",
    "Maitreyee": "30",
    "ProfessorS": "5650",
    "Bob": "Alice"
}
loginuser = " "  # initializing the username

# client choice is between take quiz, get grade, and exit
# once in the quiz, the client receives a question, displays, receives and sends an answer to the server
# the client then requests the next question
# if the questions are over, the client receives "0", and then the client must give the user the choice of commands again

# takeQuiz: 'welcome to the quiz' index = 0 *call getques*


class quizCommands:  # putting all the functions under a class
    # questions list
    questions = ["You are a WSU student.", "Sana's favorite color is yellow.", "This quiz is easy.",
                 "arrays are the same as lists.", "you are excited about exams.", "Bob is very smart.",
                 "You are in computer networking."]
    # answers list
    answers = ["true", "false", "true", "true", "false", "true", "true"]

    # user answers
    useranswers = [" ", " ", " ", " "]  # initializing the useranswers

    def __init__(self, loginuser):  # initialization function
        self.studentname = loginuser  # setting up the username
        self.currentquestion = 0  # setting to the first question
        self.questionorder = random.sample(range(7), 4)  # gives 4 random numbers from 0 to 6 and does not repeat.
        # This is for randomizing the questions

    def takeQuiz(self):  # function for taking the quiz
        print("client has begun quiz")  # notifying the user that the takeQuiz function has been called
        self.questionorder = random.sample(range(7), 4)  # randomizes the question order
        self.currentquestion = 0  # starts from the first question in the random question order

        connectionSocket.send(truemsg.encode())  # checks to see if the takeQuiz function is being called correctly and sent to the client

    def getQues(self):  # getQues function initializing
        if self.currentquestion > 3:  # error checking to make sure only 4 questions are asked
            connectionSocket.send(falsemsg.encode())  # send an error to the client
            return  # break ifelse statement

        connectionSocket.send(
            self.questions[self.questionorder[self.currentquestion]].encode())  # sending the question in the correct prespecified random order from the list
        answer = connectionSocket.recv(2048).decode()  # gets the answer from the client
        self.useranswers[self.currentquestion] = answer  # adding the answer to the initialized array

        if self.currentquestion < 3:  # question is something between 0 and 3
            self.currentquestion += 1  # proceed to the next question
            connectionSocket.send(truemsg.encode())  # error checking and sent to the client
        elif self.currentquestion == 3:  # if it reaches the last question
            connectionSocket.send(falsemsg.encode())  # end the quiz and send it to the client

    # getGrade: compare useranswers and userquestions, if = then grade++
    def getGrade(self):  # function for the grade
        self.currentgrade = 0  # initializing the current grade
        for i in range(0, 4):  # for loop for the questions and answers
            if self.answers[self.questionorder[i]] == self.useranswers[i]:  # matching the answer with the corresponding question
                self.currentgrade += 1  # doing the same for subsequent question/answer pair

        percentgrade = self.currentgrade / 4 * 100  # changing the grade into a percent
        grademessage = "Your grade is %f " % percentgrade  # setting up the grade to print
        connectionSocket.send(grademessage.encode())  # sending the grade to the client

    def exit(self):  # function for exit
        print('socket closing\n')  # notifying the user the connection is closing
        connectionSocket.close()  # closing the connection between the client and server
        e = 0  # variable for menu while loop
        return e  # for menu


def handle_client(connection_socket):
    global connectionSocket
    loginuser = connection_socket.recv(2048).decode()  # decoding the username info
    if loginuser != " ":  # if a username is received
        print('user received:', loginuser, '\n')  # print the username
        connection_socket.send(truemsg.encode())  # send verification back to the client
    # end

    loginpass = connection_socket.recv(2048).decode()  # getting the password back from the client
    print('pass received:', loginpass, '\n')  # printing the password for verification

    if users[loginuser] == loginpass:  # checking if the username and password correlate
        connection_socket.send(truemsg.encode())  # password is received and true, the client can ask for the role
        role = connection_socket.recv(2048)  # the client then sends the role
        menu = 1  # correct username/password pair
        print('login successful \n')  # prints verification
        quiz = quizCommands(loginuser)  # instantiating the class containing our quiz data and functions
        if role.decode() == 'teacher':  # teacher stuff
            msg = "Hello Instructor, would you like to exit? \n   (type exit) \n"  # only gives the teacher the option to exit
        elif role.decode() == 'student':  # if the student takes the quiz
            msg = "Hello %s would you like to take the quiz? \n" % loginuser  # prints the message to the terminal
        # end
        connection_socket.send(msg.encode())  # send the teacher/student role to the client
    else:
        connection_socket.send(falsemsg.encode())  # login info is either not received or the password is false
        print("login failed for user. \n")  # prints failed verification to the terminal
        connection_socket.close()  # closes the connection
    # end

