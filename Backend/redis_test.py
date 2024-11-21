import redis

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    db=0,
    decode_responses=True
)

try:
    redis_client.ping()
    print("✅ Redis connection successful!")
    
    # Test data set karo
    redis_client.set('test_key', 'test_value', ex=300)  # 5 minutes expiry
    
    # Test data get karo
    value = redis_client.get('test_key')
    print(f"Test value from Redis: {value}")
    
except redis.ConnectionError:
    print("❌ Redis connection failed! Make sure Redis is running.")