import grpc
import asyncio
from proto import grpc_service_pb2, grpc_service_pb2_grpc

async def run():
    try:
        with grpc.insecure_channel("host.docker.internal:50051") as channel:
            stub = grpc_service_pb2_grpc.StoryServiceStub(channel)
            
            # Construct a valid request
            request = grpc_service_pb2.StoryRequest(source="news", theme="romance")

            # Call the service
            response = stub.GenerateStory(request)
            print(response)
    except grpc.RpcError as e:
        print(f"RPC failed: {e.code()}: {e.details()}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run())
