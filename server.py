import grpc
import voting_pb2
import voting_pb2_grpc
from concurrent import futures


class VotingServicer(voting_pb2_grpc.VotingServicer):
    def CastVote(self, request, context):
        # Process the VoteRequest and return a VoteResponse
        response = voting_pb2.VoteResponse()
        response.message = f"Vote casted for candidate ID: {request.candidate_id}"
        return response

    def GetCandidates(self, request, context):
        # Return a list of candidates as CandidateListResponse
        response = voting_pb2.CandidateListResponse()
        response.candidates.extend(["Kaka", "anish", "Candidate C"])
        return response

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    voting_pb2_grpc.add_VotingServicer_to_server(VotingServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
