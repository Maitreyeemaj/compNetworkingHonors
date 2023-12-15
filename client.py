from socket import *

serverName = gethostname()  # retrieves the host name from the server to make it universal
serverPort = 12000  # set up to connect to the server port 12000

def client_thread():
    clientSocket = socket(AF_INET, SOCK_STREAM)  # part of the socket module; initializing server connection
    clientSocket.connect((serverName, serverPort))  # connecting to the server

    # Sample login credentials
    user = input("Enter your user id: ")  # asking the user for username
    password = input("Enter your password: ")  # asking the user for a password

    # Send login information to the server
    clientSocket.send(user.encode())  # encoding the information to send to the server
    userrcv = clientSocket.recv(2048).decode()  # getting the authentication result back from the server
    if userrcv == "1":
        # ask for and send password if the username was received
        clientSocket.send(password.encode())  # sending the password back to the server
        # Receive authentication result from the server
        auth_result = clientSocket.recv(2048).decode()  # checking the authentication from the server

        if auth_result == "1":  # rest of the code works iff the username and password are correct
            print("Login successful.")
            # Send user role to the server
            role = input("Enter your role (teacher/student): ")  # user inputs their role
            clientSocket.send(role.encode())  # role title is sent to the server
            print(clientSocket.recv(2048).decode())  # Message from the server for the role selection

            while role == "student":  # quiz only runs if the user is a student
                # Student operations
                command = input("Enter a command (takeQuiz/exit): \n ")  # user inputs if they want to take the quiz or exit
                clientSocket.send(command.encode())  # command is sent to the server

                # Take quiz will be available once the student role is accepted
                if command == "takeQuiz":  # quiz commands are carried through if the server verifies that the user wants to take the quiz
                    while True:
                        proceed = clientSocket.recv(2048).decode()  # the TakeQuiz verification getting sent back from the server
                        if proceed == "1":  # iff 1, then the server verified that the user wants to take the quiz
                            command = "getQues"  # the command getQues is sent to the server if the user proceeds with the quiz
                            clientSocket.send(command.encode())  # getQues command sent to the server
                            question = clientSocket.recv(2048).decode()  # question getting sent back from the server
                            print("Question:", question)  # printing the question to the terminal
                            answer = input("Your answer (true/false): ")  # user inputs their answer
                            clientSocket.send(answer.encode())  # answer getting sent to the server
                        elif proceed == "0":  # other option if the user finishes the quiz
                            command = "getGrade"  # setting up the getGrade command
                            clientSocket.send(command.encode())  # sending getGrade to the server
                            grade = clientSocket.recv(2048).decode()  # decoding the server response (grade value)
                            print("Grade: ", grade, '%')  # printing the grade results from the server
                            break  # No more questions
                elif command == "exit":  # command if the user chooses to exit the quiz
                    clientSocket.close()  # closing the connection with the server
                    print("Your session has ended \n")  # notifying the user that they have exited the quiz
                    break  # exit the if-else statement

            while role == "teacher":  # code for if the teacher attempts to take the quiz
                command = input("\n")  # interpreting the teacher input
                clientSocket.send(command.encode())  # sending the teacher input to the server
                if command == "exit":  # interprets the teacher input as automatically exiting the quiz system
                    clientSocket.close()  # closing the socket connection
                    print("Your session has ended \n");  # notifying the user that the connection has closed
                    break  # breaking the if-else statement

        else:  # if the username and password do not work
            print("Login failed.")  # notifying the user that their credentials are incorrect

    clientSocket.close()  # close the client socket after completing the operations

# Create two threads for the clients
thread1 = threading.Thread(target=client_thread)
thread2 = threading.Thread(target=client_thread)

# Start both threads
thread1.start()
thread2.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
