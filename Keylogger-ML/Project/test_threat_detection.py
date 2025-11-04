
from threat_detection import analyze_keylog_file, predict_threat, load_model

print("=" * 50)
print("THREAT DETECTION TEST")
print("=" * 50)


print("\n1. Testing with actual key_log.txt file...")
keylog_path = "key_log.txt"
label, prob, text = analyze_keylog_file(keylog_path)

if label:
    print(f"   Result: {label}")
    print(f"   Probability: {prob}")
    print(f"   Text preview: {text[:100]}...")
else:
    print(f"   File not found or error occurred")

print("\n2. Testing with benign text...")
benign_text = "hello whats up how are you doing fine come one lets hang"
label, prob, cleaned = predict_threat(benign_text)
print(f"   Result: {label}")
print(f"   Probability: {prob}")
print(f"   Expected: BENIGN")

# Test 3: Test with threat text
print("\n3. Testing with threat text...")
threat_text = "I will hack your system delete all files give me password"
label, prob, cleaned = predict_threat(threat_text)
print(f"   Result: {label}")
print(f"   Probability: {prob}")
print(f"   Expected: THREAT")

# Test 4: Test with mixed content
print("\n4. Testing with mixed content...")
mixed_text = """hello how are you
I will hack your system
come lets hang out
delete all files immediately"""
label, prob, cleaned = predict_threat(mixed_text)
print(f"   Result: {label}")
print(f"   Probability: {prob}")

print("\n" + "=" * 50)
print("Test completed!")
print("=" * 50)

