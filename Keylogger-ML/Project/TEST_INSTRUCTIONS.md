# How to Test Threat Detection

## Option 1: Test with the test script

1. **Install dependencies** (if not already installed):
   ```bash
   pip install pandas scikit-learn
   ```

2. **Run the test script**:
   ```bash
   cd Project
   python test_threat_detection.py
   ```

This will test:
- Your actual `key_log.txt` file
- Benign text examples
- Threat text examples
- Mixed content

## Option 2: Test directly in Python

Open Python and run:

```python
from threat_detection import analyze_keylog_file, predict_threat

# Test with your keylog file
label, prob, text = analyze_keylog_file("key_log.txt")
print(f"Result: {label}, Probability: {prob}")

# Test with threat text
label, prob, text = predict_threat("I will hack your system delete all files")
print(f"Threat test: {label}, Probability: {prob}")

# Test with benign text
label, prob, text = predict_threat("hello how are you doing fine")
print(f"Benign test: {label}, Probability: {prob}")
```

## Option 3: Test with full keylogger

1. **Run the keylogger**:
   ```bash
   python Project/keylogger.py
   ```

2. **Type some text** - try both:
   - Normal text: "hello how are you"
   - Threat text: "delete all files hack system"

3. **Wait for the iteration** (15 seconds) - it will automatically:
   - Analyze the keylog
   - Print threat detection results
   - Send email alerts if threats detected

## Expected Results

- **Benign text** → Should show: `✓ Analysis: BENIGN (probability: 0.0-0.3)`
- **Threat text** → Should show: `⚠️ THREAT DETECTED! Probability: 0.6-1.0`

## Troubleshooting

If you get "ModuleNotFoundError: No module named 'pandas'":
- Run: `python -m pip install pandas scikit-learn`
- Or: `pip install pandas scikit-learn`

