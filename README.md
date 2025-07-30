# AES-256 Web Application

An interactive web application demonstrating AES-256 encryption/decryption with visual step-by-step representation.

## ✨ Features

- **AES-256 Encryption/Decryption**: Full implementation using `pycryptodome` library.
- **Multiple Encryption Modes**: Supports ECB, CBC, CFB, OFB, and CTR modes.
- **Bilingual Interface**: Full support for both English and Arabic languages.
- **Detailed Step Visualization**: Complete visual representation of AES transformation rounds as a flow diagram.
- **Block-Level Analysis**: Detailed processing of each 16-byte block across all 14 AES rounds.
- **Educational Round Explanation**: Clear illustration of `SubBytes`, `ShiftRows`, `MixColumns`, and `AddRoundKey` operations in each round.
- **Tutorial Interface**: Clear explanations and visual feedback for easy understanding.
- **XMind Export**: Ability to download detailed process steps as a mind map file (XMind).
- **Input Validation**: Comprehensive error handling and user guidance to ensure correct data entry.

## 🚀 Installation

1. **Clone or download the project**
2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
🛠️ Usage
Run the application:

bash
python app.py
Open your browser and navigate to http://127.0.0.1:5000

For Encryption:

Enter the plaintext you wish to encrypt.

Enter a 32-character encryption key (256-bit).

Select an encryption mode (ECB, CBC, CFB, OFB, CTR).

For modes requiring it (e.g., CBC), enter a 16-character initialization vector (IV).

Click "🔒 Encrypt".

For Decryption:

Enter the Base64-encoded ciphertext.

Use the same 32-character key used for encryption.

Select the same encryption mode used initially.

For modes requiring it, use the same initialization vector (IV).

Click "🔓 Decrypt".

View Results:

Observe the visual representation of AES steps.

Download the XMind file for detailed process analysis.

📁 File Structure
text

### Key Translation Notes:
1. "Backgroud" (cell) was interpreted as "Web Application" in context  
2. Maintained technical terms like ECB/CBC/IV without translation  
3. Used Arabic numerals (١٢٣) in Arabic section, Western numerals in English  
4. Kept emojis and code blocks format consistent  
5. Structured both versions with identical Markdown formatting  

Would you like me to add any specific technical details or modify the translation approach?


```
aes_webapp/
├── app.py              # Flask web application
├── aes_engine.py       # AES-256 implementation with step tracking
├── xmind_exporter.py   # XMind file generation
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html      # Web interface template
├── static/
│   ├── style.css       # Styling
│   └── aes.js          # Frontend JavaScript
└── README.md           # This file
```

## Technical Details

### AES Implementation
- Uses `pycryptodome` library for cryptographic operations
- Implements proper PKCS7 padding
- Supports both ECB and CBC modes
- Comprehensive error handling and validation

### Step Tracking
The application logs and displays:
1. Input preparation and validation
2. Key setup and validation
3. Padding application (PKCS7)
4. Mode-specific initialization (IV for CBC)
5. Block-by-block processing
6. Final output formatting

### Security Notes
- **ECB Mode**: Less secure, used for educational purposes only
- **CBC Mode**: More secure, requires proper IV management
- **Key Management**: Keys should be securely generated and stored in production
- **This is an educational tool**: Not recommended for production encryption needs

## Example Usage

### Encryption Example
- **Plaintext**: "Hello, World!"
- **Key**: "MySecretKey123456789012345678901" (32 chars)
- **Mode**: CBC
- **IV**: "1234567890123456" (16 chars)
- **Result**: Base64 encoded ciphertext

### Decryption Example
- **Ciphertext**: [Base64 from encryption]
- **Key**: "MySecretKey123456789012345678901" (same key)
- **Mode**: CBC (same mode)
- **IV**: "1234567890123456" (same IV)
- **Result**: "Hello, World!" (original plaintext)

## Troubleshooting

### Common Errors
1. **"Key must be 32 characters"**: Ensure your key is exactly 32 characters long
2. **"Data must be aligned to block boundary"**: Invalid ciphertext or wrong key/mode
3. **"Invalid Base64 input"**: Ciphertext must be valid Base64 encoding
4. **"Invalid padding"**: Wrong key or corrupted data

### Tips
- Use the character counters to ensure correct key/IV lengths
- Copy the exact ciphertext output for decryption
- Use the same key and mode for encryption and decryption
- For CBC mode, ensure IV consistency

## Dependencies

- **Flask**: Web framework
- **pycryptodome**: Cryptographic library
- **xmind**: Mind map file generation

## License

This project is for educational purposes. Please ensure compliance with local cryptography regulations.
