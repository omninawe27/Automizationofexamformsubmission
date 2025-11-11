import requests
import threading
import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuration
BASE_URL = 'http://127.0.0.1:8000'  # Adjust if running on different port
CONCURRENT_USERS = [10, 50, 100, 200]  # Test with different user loads
TEST_DURATION = 60  # seconds per test
REQUESTS_PER_USER = 10  # requests per user during test

# Endpoints to test
ENDPOINTS = [
    '/',
    '/login/',
    '/register/',
    '/admin/dashboard/',
    '/student/dashboard/',
]

# Store results
results = {}

def make_request(session, endpoint):
    """Make a single request and return response time and success status"""
    start_time = time.time()
    try:
        response = session.get(f"{BASE_URL}{endpoint}", timeout=10)
        response_time = time.time() - start_time
        return response_time, response.status_code == 200
    except Exception as e:
        response_time = time.time() - start_time
        return response_time, False

def simulate_user(user_id, concurrent_users, test_duration):
    """Simulate a single user making requests"""
    session = requests.Session()
    user_results = []

    # Login if needed (for authenticated endpoints)
    try:
        # Attempt login with test credentials
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        session.post(f"{BASE_URL}/login/", data=login_data, timeout=10)
    except:
        pass  # Continue without login if fails

    start_time = time.time()
    request_count = 0

    while time.time() - start_time < test_duration and request_count < REQUESTS_PER_USER:
        for endpoint in ENDPOINTS:
            if time.time() - start_time >= test_duration:
                break

            response_time, success = make_request(session, endpoint)
            user_results.append({
                'endpoint': endpoint,
                'response_time': response_time,
                'success': success,
                'user_id': user_id
            })
            request_count += 1

            # Small delay between requests
            time.sleep(0.1)

    return user_results

def run_load_test(concurrent_users, test_duration):
    """Run load test with specified number of concurrent users"""
    print(f"\n{'='*50}")
    print(f"Testing with {concurrent_users} concurrent users")
    print(f"Duration: {test_duration} seconds")
    print(f"{'='*50}")

    start_time = time.time()

    with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
        futures = [
            executor.submit(simulate_user, user_id, concurrent_users, test_duration)
            for user_id in range(concurrent_users)
        ]

        all_results = []
        for future in as_completed(futures):
            try:
                user_results = future.result()
                all_results.extend(user_results)
            except Exception as e:
                print(f"Error in user simulation: {e}")

    total_time = time.time() - start_time

    # Analyze results
    successful_requests = [r for r in all_results if r['success']]
    failed_requests = [r for r in all_results if not r['success']]

    response_times = [r['response_time'] for r in all_results]

    print(f"\nResults for {concurrent_users} users:")
    print(f"Total requests: {len(all_results)}")
    print(f"Successful requests: {len(successful_requests)}")
    print(f"Failed requests: {len(failed_requests)}")
    print(".2f")
    print(".2f")
    print(".2f")
    print(".2f")
    print(".2f")

    # Check for crashes (high failure rate or very slow responses)
    failure_rate = len(failed_requests) / len(all_results) if all_results else 0
    avg_response_time = statistics.mean(response_times) if response_times else 0

    if failure_rate > 0.5:
        print("⚠️  HIGH FAILURE RATE - Possible server crash or overload")
    elif avg_response_time > 5.0:
        print("⚠️  VERY SLOW RESPONSES - Server struggling")
    elif avg_response_time > 2.0:
        print("⚠️  SLOW RESPONSES - Server under load")
    else:
        print("✅ Server handling load well")

    return {
        'concurrent_users': concurrent_users,
        'total_requests': len(all_results),
        'successful_requests': len(successful_requests),
        'failed_requests': len(failed_requests),
        'failure_rate': failure_rate,
        'avg_response_time': avg_response_time,
        'median_response_time': statistics.median(response_times) if response_times else 0,
        'min_response_time': min(response_times) if response_times else 0,
        'max_response_time': max(response_times) if response_times else 0,
        'test_duration': total_time
    }

def main():
    print("Django Application Load Testing")
    print("Make sure the Django server is running on http://127.0.0.1:8000")
    print("This test will simulate multiple users accessing the application simultaneously.")

    input("Press Enter to start the load test...")

    all_test_results = []

    for num_users in CONCURRENT_USERS:
        try:
            result = run_load_test(num_users, TEST_DURATION)
            all_test_results.append(result)

            # Stop testing if failure rate is too high (server likely crashed)
            if result['failure_rate'] > 0.8:
                print(f"\nStopping tests - Server appears to have crashed at {num_users} users")
                break

        except KeyboardInterrupt:
            print("\nTest interrupted by user")
            break
        except Exception as e:
            print(f"Error during test with {num_users} users: {e}")
            break

    # Summary
    print(f"\n{'='*60}")
    print("LOAD TEST SUMMARY")
    print(f"{'='*60}")

    print("<10")
    print("<10")
    print("<10")
    print("<10")
    print("<10")

    print("\nDetailed Results:")
    for result in all_test_results:
        print(f"\n{result['concurrent_users']} users:")
        print(f"  Success Rate: {(1-result['failure_rate'])*100:.1f}%")
        print(f"  Avg Response Time: {result['avg_response_time']:.2f}s")
        print(f"  Max Response Time: {result['max_response_time']:.2f}s")

    # Recommendations
    if all_test_results:
        max_successful_users = max(
            (r for r in all_test_results if r['failure_rate'] < 0.1),
            key=lambda x: x['concurrent_users'],
            default=all_test_results[0]
        )['concurrent_users']

        print(f"\n{'='*60}")
        print("RECOMMENDATIONS")
        print(f"{'='*60}")
        print(f"Maximum concurrent users with <10% failure rate: {max_successful_users}")
        print("Consider implementing:")
        print("- Database connection pooling")
        print("- Caching (Redis/Memcached)")
        print("- Load balancing")
        print("- CDN for static files")
        print("- Database optimization")
        print("- Asynchronous task processing")

if __name__ == "__main__":
    main()
