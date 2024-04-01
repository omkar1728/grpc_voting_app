import grpc
from concurrent import futures
import voting_pb2
import voting_pb2_grpc
import database2 as db

class VotingServicer(voting_pb2_grpc.VotingServicer):
    def GetCandidates(self, request, context):

        candidate_list = db.get_all_candidates()
        return voting_pb2.CandidateListResponse(candidates= candidate_list)

    def RegisterCandidate(self, request, context):
        message = db.register_new_candidate(request.candidate_name)
        return voting_pb2.Ack(message= message)

    def RegisterVoter(self, request, context):
        message = db.register_new_voter(request.voter_id)
        return voting_pb2.Ack(message= message)

    def VoteCandidate(self, request, context):
        
        message = db.vote(request.voter_id, request.candidate_name)
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
