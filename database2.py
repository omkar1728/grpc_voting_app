import sqlite3

def create_tables():
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute('''CREATE TABLE IF NOT EXISTS Voter (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            voter_id TEXT UNIQUE
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Candidate (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            cName TEXT UNIQUE
                        )''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Voted (
                            voter_id TEXT,
                            candidate_name TEXT NOT NULL,
                            FOREIGN KEY (voter_id) REFERENCES Voter(voter_id),
                            FOREIGN KEY (candidate_name) REFERENCES Candidate(cName),
                            PRIMARY KEY (voter_id)
                        )''')

        conn.commit()
        conn.close()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)

def register_new_voter(voter_id):
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("INSERT INTO Voter (voter_id) VALUES (?)", (voter_id,))
        conn.commit()
        conn.close()
        message = "New voter " + str(voter_id) +" registered successfully."
        print(message)
        return message
    except sqlite3.IntegrityError:
        message = "Voter ID already exists."
        print(message)
        return message

    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

def register_new_candidate(cName):
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("INSERT INTO Candidate (cName) VALUES (?)", (cName,))
        conn.commit()
        conn.close()
        message = "New candidate " + cName +  " registered successfully."
        print(message)
        return message
    except sqlite3.IntegrityError:
        message = "Candidate name already exists."
        print(message)
        return message
    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

def get_all_candidates():
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("SELECT cName FROM Candidate")
        candidates = cursor.fetchall()
        conn.close()

        if candidates:
            return [candidate[0] for candidate in candidates]
        else:
            message = "No candidates found."
            print(message)
            return message
    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

def vote(voter_id, candidate_name):
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("INSERT INTO Voted (voter_id, candidate_name) VALUES (?, ?)", (voter_id, candidate_name))
        conn.commit()
        conn.close()
        message = "Vote recorded successfully."
        print(message)
        return message
    except sqlite3.IntegrityError as e:
        # print("Error", e)
        # print(type(e))
        err = str(e)
        if(err == "FOREIGN KEY constraint failed"):
            message = "Voter or Candidate not registered"
            print(message)
            return message

        else:
            message = "Voter already Voted"
            print(message)
            return message

    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

def get_candidate_with_max_votes():
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        # Find the maximum count
        cursor.execute("SELECT MAX(vote_count) FROM (SELECT COUNT(*) AS vote_count FROM Voted GROUP BY candidate_name)")

        # Fetch the maximum count
        max_count = cursor.fetchone()[0]

        # Fetch all records with the maximum count
        cursor.execute(
            "SELECT candidate_name, COUNT(*) AS vote_count FROM Voted GROUP BY candidate_name HAVING COUNT(*) = ?",
            (max_count,))
        candidate = cursor.fetchall()

        # cursor.execute("SELECT candidate_name, COUNT(*) AS vote_count FROM Voted GROUP BY candidate_name ORDER BY vote_count DESC LIMIT 1")
        # candidate = cursor.fetchall()
        conn.close()

        if candidate:
            return "Winner is " + candidate[0][0] + " with " + str(candidate[0][1] )+ " votes"
        else:
            message =  "No votes recorded yet."
            print(message)
            return message
            
    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

def get_candidate_votes():
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("SELECT candidate_name, COUNT(*) AS vote_count FROM Voted GROUP BY candidate_name")
        candidates = cursor.fetchall()
        conn.close()

        if candidates:
            return candidates
        else:
            message =  "No votes recorded yet."
            print(message)
            return message
    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message


def get_registered_voter_ids():
    try:
        conn = sqlite3.connect('voting_database.db')
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON;")

        cursor.execute("SELECT voter_id FROM Voter")
        registered_voter_ids = cursor.fetchall()

        # Close the connection
        conn.close()

        # Extract voter ids from the result
        registered_voter_ids = [voter_id[0] for voter_id in registered_voter_ids]
        if registered_voter_ids:
            print(registered_voter_ids)
            return registered_voter_ids
        else:
            message =  "No registered Voters"
            print(message)
            return message
    except sqlite3.Error as e:
        message = "Error occurred:" +  e
        print(message)
        return message

# Close connection
def close_connection():
    try:
        conn = sqlite3.connect('voting_database.db')
        conn.close()
        print("Connection closed successfully.")
    except sqlite3.Error as e:
        print("Error occurred:", e)

# Create tables
create_tables()

# Example usage:
# register_new_voter("Voter1")
# register_new_candidate("Candidate1")
# print(get_all_candidates())
# vote("Voter1", "Candidate1")
# print(get_candidate_with_max_votes())
# print(get_candidate_votes())
# close_connection()


# #Main loop for user interaction
# while True:
#     print("\nMenu:")
#     print("1. Get candidate list")
#     print("2. Register new candidate")
#     print("3. Register new voter")
#     print("4. Vote")
#     print("5. Get candidate with max votes")
#     print("6. Get candidate votes")
#     print("7. Get Registered voters")
#     print("8. Exit")

#     choice = input("Enter your choice: ")
#     if choice == "1":
#         candidate_list = get_all_candidates()
#         if candidate_list:
#             print("Candidate List:")
#             for candidate in candidate_list:
#                 print(candidate)
#         else:
#             print("No candidates found.")
#     elif choice == "2":
#         candidate_name = input("Enter candidate name: ")
#         register_new_candidate(candidate_name)
#     elif choice == "3":
#         voter_id = input("Enter voter ID: ")
#         register_new_voter(voter_id)
#     elif choice == "4":
#         voter_id = input("Enter voter ID: ")
#         candidate_name = input("Enter candidate name: ")
#         vote(voter_id, candidate_name)
#     elif choice == "5":
#         candidate_name = get_candidate_with_max_votes()
#         if candidate_name:
#             print("Candidate with Max Votes:")
#             for cand in candidate_name:
#                 print(cand[0])
#         else:
#             print("No votes recorded yet.")
#     elif choice == "6":
#         candidate_votes = get_candidate_votes()
#         if candidate_votes:
#             print("Candidate Votes:")
#             for candidate, vote_count in candidate_votes:
#                 print(f"{candidate}: {vote_count}")
#         else:
#             print("No votes recorded yet.")
#     elif choice == "7":
#         registered_voter_ids = get_registered_voter_ids()

#         if registered_voter_ids:
#             print("Registered Voters")
#             for voter in registered_voter_ids:
#                 print(voter)
#     elif choice == "8":
#         print("Exiting...")
#         break
#     else:
#         print("Invalid choice. Please enter a valid option.")

# #Close the connection
# close_connection()



# #Main loop for user interaction
# while True:
#     print("\nMenu:")
#     print("1. Get candidate list")
#     print("2. Register new candidate")
#     print("3. Register new voter")
#     print("4. Vote")
#     print("5. Get candidate with max votes")
#     print("6. Get candidate votes")
#     print("7. Exit")

#     choice = input("Enter your choice: ")
#     if choice == "1":
#         candidate_list = get_all_candidates()
#         if candidate_list:
#             print("Candidate List:")
#             for candidate in candidate_list:
#                 print(candidate)
#         else:
#             print("No candidates found.")
#     elif choice == "2":
#         candidate_name = input("Enter candidate name: ")
#         register_new_candidate(candidate_name)
#     elif choice == "3":
#         voter_id = input("Enter voter ID: ")
#         register_new_voter(voter_id)
#     elif choice == "4":
#         voter_id = input("Enter voter ID: ")
#         candidate_name = input("Enter candidate name: ")
#         vote(voter_id, candidate_name)
#     elif choice == "5":
#         candidate_name = get_candidate_with_max_votes()
#         if candidate_name:
#             print("Candidate with Max Votes:", candidate_name)
#         else:
#             print("No votes recorded yet.")
#     elif choice == "6":
#         candidate_votes = get_candidate_votes()
#         if candidate_votes:
#             print("Candidate Votes:")
#             for candidate, vote_count in candidate_votes:
#                 print(f"{candidate}: {vote_count}")
#         else:
#             print("No votes recorded yet.")
#     elif choice == "7":
#         print("Exiting...")
#         break
#     else:
#         print("Invalid choice. Please enter a valid option.")

# #Close the connection
# close_connection()
