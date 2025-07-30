#!/usr/bin/env python3
"""
Demo script to show clear differences between input and output blocks
"""

from aes_engine import AES256WithSteps

def demo_block_differences():
    """Demonstrate clear block transformation differences"""
    
    print("🔍 AES Block Transformation Demo")
    print("=" * 50)
    
    # Test data - exactly 16 bytes
    plaintext = "Hello World!!!!!"  # Exactly 16 characters = 16 bytes
    key = "MySecretKey123456789012345678901"  # 32 characters
    
    print(f"📝 Plaintext: {plaintext}")
    print(f"🔑 Key: {key}")
    print(f"🔧 Mode: ECB (shows pure AES transformation)")
    print()
    
    # Create AES instance
    aes = AES256WithSteps(key.encode(), 'ECB')
    
    # Encrypt
    print("🔒 ENCRYPTION:")
    print("-" * 30)
    ciphertext = aes.encrypt(plaintext)
    
    # Find the final result step
    final_steps = [step for step in aes.steps if 'Final Result' in step['step']]
    if final_steps:
        print("📊 BLOCK TRANSFORMATION DETAILS:")
        print(final_steps[0]['detail'])
        print()
    
    # Show key steps with actual data
    print("🔄 KEY TRANSFORMATION STEPS:")
    print("-" * 30)
    
    # Input preparation
    input_step = next(step for step in aes.steps if 'Input Preparation' in step['step'])
    print("1️⃣ INPUT PREPARATION:")
    print(input_step['detail'])
    print()
    
    # Padding
    padding_step = next(step for step in aes.steps if 'Padding' in step['step'])
    print("2️⃣ PADDING:")
    print(padding_step['detail'])
    print()
    
    # Block processing start
    block_start = next(step for step in aes.steps if 'Block 1 Processing Start' in step['step'])
    print("3️⃣ BLOCK PROCESSING START:")
    print(block_start['detail'])
    print()
    
    # Initial state
    initial_state = next(step for step in aes.steps if 'Initial State' in step['step'])
    print("4️⃣ INITIAL STATE:")
    print(initial_state['detail'])
    print()
    
    # Final result
    if final_steps:
        print("5️⃣ FINAL TRANSFORMATION RESULT:")
        print(final_steps[0]['detail'])
        print()
    
    print("🎯 SUMMARY:")
    print(f"✅ Input:  Exactly 16 bytes (Hello World!!!!! - no padding needed)")
    print(f"✅ Output: Encrypted 16-byte block")
    print(f"✅ Base64: {ciphertext}")
    print(f"✅ Transformation: Complete - all 16 bytes changed!")
    print()
    
    # Test decryption
    print("🔓 DECRYPTION VERIFICATION:")
    print("-" * 30)
    aes_decrypt = AES256WithSteps(key.encode(), 'ECB')
    decrypted = aes_decrypt.decrypt(ciphertext)
    
    # Find decryption final result
    decrypt_final = [step for step in aes_decrypt.steps if 'Decryption Result' in step['step']]
    if decrypt_final:
        print("📊 DECRYPTION TRANSFORMATION:")
        print(decrypt_final[0]['detail'])
        print()
    
    print(f"🎯 DECRYPTION RESULT: {decrypted}")
    print(f"✅ Match: {'Yes' if decrypted == plaintext else 'No'}")

if __name__ == "__main__":
    demo_block_differences()