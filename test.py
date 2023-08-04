import uuid

def generate_random_uuids(num_uuids=5):
    random_uuids = [uuid.uuid4() for _ in range(num_uuids)]
    return random_uuids

# Generate five random UUIDs
random_uuids = generate_random_uuids(5)
print(random_uuids)