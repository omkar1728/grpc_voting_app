import grpc
from concurrent import futures
import voting_pb2
import voting_pb2_grpc
import database as db

class VotingServicer(voting_pb2_grpc.VotingServicer):
    # def CastVote(self, request, context):
    #     # Implement CastVote logic here
    #     # For demonstration purposes, we just return a simple acknowledgment
    #     db.vote({request.voter_id}, {request.candidate_name})
    #     message = f"Vote casted for candidate: {request.candidate_name} by voter: {request.voter_id}"
    #     print(message)
    #     return voting_pb2.Ack(message= message)

    def GetCandidates(self, request, context):
        # Implement GetCandidates logic here
        # For demonstration purposes, we return a list of sample candidates
        candidate_list = db.get_all_candidates()
        return voting_pb2.CandidateListResponse(candidates= candidate_list)

    def RegisterCandidate(self, request, context):
        # Implement RegisterCandidate logic here
        # For demonstration purposes, we just return a simple acknowledgment
        db.register_new_candidate(request.candidate_name)
        return voting_pb2.Ack(message=f"Candidate {request.candidate_name} registered successfully")

    def RegisterVoter(self, request, context):
        # Implement RegisterVoter logic here
        # For demonstration purposes, we just return a simple acknowledgment
        db.register_new_voter(request.voter_id)
        return voting_pb2.Ack(message=f"Voter {request.voter_id} registered successfully")

    def VoteCandidate(self, request, context):
        # Implement VoteCandidate logic here
        # For demonstration purposes, we just return a simple acknowledgment
        
        print(request.voter_id, request.candidate_name)
        db.vote(request.voter_id, request.candidate_name)
        message = f"Vote casted for candidate: {request.candidate_name} by voter: {request.voter_id}"
        print(message)
        return voting_pb2.Ack(message= message)
    
    def GetWinner(self, request, context):
        # Implement VoteCandidate logic here
        # For demonstration purposes, we just return a simple acknowledgment
        winner = db.get_candidate_with_max_votes()
        return voting_pb2.Ack(message= winner)
    

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_VotingServicer_to_server(VotingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
