import grpc
from concurrent import futures
from proto import grpc_service_pb2_grpc, grpc_service_pb2
from llm import TrendsToStory
from scraper import TrendScraper
import asyncio


class StoryService(grpc_service_pb2_grpc.StoryServiceServicer):
    def __init__(self):
        self.llm = TrendsToStory()
        self.scraper = TrendScraper()

    def GenerateStory(self, request, context):
        try:
            # Create an event loop for this request
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            print(f"Generating story for source: {request.source} and theme: {request.theme}")

            # Run the async functions in the event loop
            trends = loop.run_until_complete(self.scraper.get_trends(request.source))
            story = loop.run_until_complete(self.llm.generate_story(trends, request.theme))
            
            # Clean up the event loop
            loop.close()
            
            return grpc_service_pb2.StoryResponse(story=story, error="")
        except Exception as e:
            return grpc_service_pb2.StoryResponse(story="", error=str(e))


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_service_pb2_grpc.add_StoryServiceServicer_to_server(StoryService(), server)
    server.add_insecure_port("[::]:50051")
    print("🚀 gRPC server running on port http://localhost:50051...")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
