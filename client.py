import grpc
import voting_pb2
import voting_pb2_grpc

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = voting_pb2_grpc.VotingStub(channel)

    # vote_request = voting_pb2.VoteRequest()
    # vote_request.candidate_id = "Candidate A"
    # vote_response = stub.CastVote(vote_request)
    # print("Vote Response:", vote_response.message)

    candidate_request = voting_pb2.CandidateRequest()
    candidate_list_response = stub.GetCandidates(candidate_request)
    print("Candidate List Response:", candidate_list_response.candidates)

if __name__ == '__main__':
    main()
