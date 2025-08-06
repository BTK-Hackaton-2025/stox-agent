import grpc
import seo_agent_pb2
import seo_agent_pb2_grpc


def test_health_check(stub):
    """Test the health check endpoint."""
    print("Testing Health Check...")
    request = seo_agent_pb2.HealthCheckRequest()
    response = stub.HealthCheck(request)
    print(f"Health Status: {response.status}, Service: {response.service}")
    print()


def test_analyze_seo(stub, image_url):
    """Test the SEO analysis endpoint."""
    print(f"Testing SEO Analysis with URL: {image_url}")
    request = seo_agent_pb2.AnalyzeSEORequest(image_url=image_url)
    
    try:
        response = stub.AnalyzeSEO(request)
        if response.success:
            print(f"Success: {response.success}")
            print(f"Image URL: {response.image_url}")
            print(f"Analysis: {response.analysis}")
            if response.intermediate_steps:
                print("Intermediate Steps:")
                for step in response.intermediate_steps:
                    print(f"  - {step}")
        else:
            print(f"Error: {response.error}")
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()}, {e.details()}")
    print()


def test_chat(stub, message):
    """Test the chat endpoint."""
    print(f"Testing Chat with message: {message}")
    request = seo_agent_pb2.ChatRequest(message=message)
    
    try:
        response = stub.Chat(request)
        if response.success:
            print(f"Success: {response.success}")
            print(f"Response: {response.response}")
            if response.intermediate_steps:
                print("Intermediate Steps:")
                for step in response.intermediate_steps:
                    print(f"  - {step}")
        else:
            print(f"Error: {response.error}")
    except grpc.RpcError as e:
        print(f"gRPC Error: {e.code()}, {e.details()}")
    print()


def main():
    """Main test function."""
    # Connect to the gRPC server
    channel = grpc.insecure_channel('localhost:50051')
    stub = seo_agent_pb2_grpc.SEOAgentServiceStub(channel)
    
    print("=== gRPC Client Test ===\n")
    
    # Test health check
    test_health_check(stub)
    
    # Test SEO analysis
    test_image_url = "https://dc9a2118r4lqa.cloudfront.net/users/b3a45f8c-5473-4a9a-9b48-35731c36125e/enhanced/enhanced_test-image_0d56bda0-ad35-45ab-a901-a206e54018ea_enhanced_a0fd79c3-6965-4dd4-9e8c-88f6273b193b.jpg"
    test_analyze_seo(stub, test_image_url)
    
    # Test chat
    test_chat(stub, "Hello! Can you tell me about SEO best practices for images?")
    
    # Test chat with image analysis request
    test_chat(stub, f"Please analyze this image for SEO: {test_image_url}")
    
    print("=== Test Complete ===")


if __name__ == '__main__':
    main()