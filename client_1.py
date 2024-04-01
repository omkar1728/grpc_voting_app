import grpc
import voting_pb2
import voting_pb2_grpc

def main():
    # Create a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')
    # Create a stub (client)
    stub = voting_pb2_grpc.VotingStub(channel)
    voter_id = "1"
    while(True):
        print("1. Get candidate list")
        print("2. Register candidate")
        print("3. Register voter")
        print("4. Vote candidate")
        print("5. Get winner")
        print("6. Exit")

        choice = input("Enter your choice: ")
        print()
        if choice == "1":
            # Call the GetCandidates RPC
            get_candidates_request = voting_pb2.GetCandidateRequest(message="Get candidates")
            candidate_list_response = stub.GetCandidates(get_candidates_request)
            candidates = candidate_list_response.candidates
            print("List of candidates is:")
            for i in candidates:
                print(i)

        elif choice == "2":
            # Call the RegisterCandidate RPC
            name = input("Enter candidate name: ")
            register_candidate_request = voting_pb2.RegisterCandidateRequest(candidate_name= name)
            register_candidate_response = stub.RegisterCandidate(register_candidate_request)
            print( register_candidate_response.message)

        elif choice == "3":
            # Call the RegisterVoter RPC
            #voter_id = input("Enter your voter id: ")
            register_voter_request = voting_pb2.RegisterVoterRequest(voter_id=voter_id)
            register_voter_response = stub.RegisterVoter(register_voter_request)
            print( register_voter_response.message)
        
        elif choice == "4":
            #voter_id = input("Enter your voter id: ")
            name = input("Enter candidate name: ")
            vote_candidate_request = voting_pb2.VoteRequest(candidate_name= name, voter_id= voter_id)
            vote_candidate_response = stub.VoteCandidate( vote_candidate_request )
            print(vote_candidate_response.message)

        elif choice == "5":
            winner_candidate_request = voting_pb2.WinnerRequest(message="123")
            winner_candidate_response = stub.GetWinner( winner_candidate_request )
            print(winner_candidate_response.message)

        elif choice == "6":
            break
        else:
            print("Choose a valid choice")

        print()
        print()
        print()



    # # Call the VoteCandidate RPC
    # vote_request = voting_pb2.VoteRequest(candidate_name="Candidate A", voter_id="Voter2")
    # vote_response = stub.VoteCandidate(vote_request)
    # print("Vote Candidate Response:", vote_response.message)

if __name__ == '__main__':
    main()
