# aes_engine.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import binascii
import struct

class AES256WithSteps:
    def __init__(self, key, mode='ECB', iv=None):
        """
        Initialize AES-256 cipher with step tracking
        
        Args:
            key (bytes): 32-byte key for AES-256
            mode (str): 'ECB', 'CBC', 'CFB', 'OFB', or 'CTR'
            iv (bytes): Initialization vector/nonce (16 bytes)
        """
        self.key = key
        self.mode = mode.upper()
        self.iv = iv if iv else get_random_bytes(16)
        self.steps = []
        
        # Validate key length
        if len(self.key) != 32:
            raise ValueError("Key must be 32 bytes for AES-256")
        
        # Validate mode
        if self.mode not in ['ECB', 'CBC', 'CFB', 'OFB', 'CTR']:
            raise ValueError("Mode must be one of: ECB, CBC, CFB, OFB, CTR")
        
        # Validate IV/nonce for modes that require it
        if self.mode in ['CBC', 'CFB', 'OFB', 'CTR'] and len(self.iv) != 16:
            raise ValueError(f"IV/Nonce must be 16 bytes for {self.mode} mode")
    
    def _log_step(self, step_name, detail):
        """Log a step in the AES process"""
        self.steps.append({
            "step": step_name,
            "detail": detail
        })
    
    def _bytes_to_hex(self, data):
        """Convert bytes to hex string for display"""
        return binascii.hexlify(data).decode('utf-8').upper()
    
    def _format_state(self, state):
        """Format state matrix for display"""
        if isinstance(state, bytes):
            hex_str = self._bytes_to_hex(state)
            # Format as 4x4 matrix
            formatted = ""
            for i in range(0, len(hex_str), 8):
                row = hex_str[i:i+8]
                formatted += " ".join([row[j:j+2] for j in range(0, len(row), 2)]) + "\n"
            return formatted.strip()
        return str(state)
    
    def _compare_blocks(self, input_block, output_block, operation="transformation"):
        """Compare input and output blocks and show differences"""
        if input_block == output_block:
            return f"⚠️ WARNING: No change detected in {operation}!"
        
        # Count different bytes
        different_bytes = sum(1 for a, b in zip(input_block, output_block) if a != b)
        total_bytes = len(input_block)
        
        return (f"✅ {operation.capitalize()} successful!\n"
                f"📊 Changed bytes: {different_bytes}/{total_bytes} ({different_bytes/total_bytes*100:.1f}%)\n"
                f"🔄 Data transformation: Complete")
    
    def _simulate_aes_rounds(self, block_data, block_num, is_encryption=True):
        """
        Simulate detailed AES round transformations for educational purposes
        This provides step-by-step breakdown of what happens inside AES
        """
        operation = "Encryption" if is_encryption else "Decryption"
        
        # Convert block to state matrix representation
        state_hex = self._bytes_to_hex(block_data)
        
        self._log_step(f"6.{block_num}.1. Initial State (Block {block_num})",
                      f"Input block: {state_hex}\n"
                      f"State matrix (column-major order):\n{self._format_state(block_data)}\n"
                      f"Ready for {operation.lower()}")
        
        # Simulate key expansion (simplified)
        self._log_step(f"6.{block_num}.2. Key Schedule",
                      f"AES-256 uses 14 rounds (plus initial round)\n"
                      f"Key expansion generates 15 round keys (240 bytes total)\n"
                      f"Initial Round: Only AddRoundKey\n"
                      f"Rounds 1-13: Full rounds (SubBytes → ShiftRows → MixColumns → AddRoundKey)\n"
                      f"Round 14: Final round (SubBytes → ShiftRows → AddRoundKey, no MixColumns)")
        
        if is_encryption:
            # Initial round (Round 0) - Only AddRoundKey
            self._log_step(f"6.{block_num}.3. Initial Round",
                          f"Operation: AddRoundKey only\n"
                          f"State ⊕ RoundKey[0] (original key)\n"
                          f"Each byte of state XORed with corresponding key byte\n"
                          f"This provides initial key mixing before main rounds")
            
            # Main rounds (1-13) - Full rounds with all 4 operations
            for round_num in range(1, 14):
                self._log_step(f"6.{block_num}.{3+round_num}. Round {round_num}",
                              f"Step 1: SubBytes - Apply S-box substitution\n"
                              f"  • Each byte replaced using AES S-box lookup table\n"
                              f"  • Provides non-linearity and confusion\n"
                              f"Step 2: ShiftRows - Cyclically shift rows\n"
                              f"  • Row 0: No shift, Row 1: Left shift 1\n"
                              f"  • Row 2: Left shift 2, Row 3: Left shift 3\n"
                              f"  • Provides diffusion across columns\n"
                              f"Step 3: MixColumns - Matrix multiplication\n"
                              f"  • Each column multiplied by fixed matrix in GF(2^8)\n"
                              f"  • Further diffusion within columns\n"
                              f"Step 4: AddRoundKey - XOR with round key\n"
                              f"  • State ⊕ RoundKey[{round_num}]\n"
                              f"  • Incorporates round-specific key material")
            
            # Final round (14) - No MixColumns
            self._log_step(f"6.{block_num}.17. Final Round (Round 14)",
                          f"Step 1: SubBytes - Apply S-box substitution\n"
                          f"Step 2: ShiftRows - Cyclically shift rows\n"
                          f"Step 3: AddRoundKey - XOR with final round key\n"
                          f"⚠️ Note: MixColumns is SKIPPED in the final round\n"
                          f"Final ciphertext block produced")
        else:
            # Decryption - reverse the encryption process
            # Start by removing the final round key (Round 14)
            self._log_step(f"6.{block_num}.3. Initial Decryption Step",
                          f"Operation: AddRoundKey (Round 14 key)\n"
                          f"State ⊕ RoundKey[14]\n"
                          f"Remove final encryption round key to start decryption")
            
            # Reverse final round (was Round 14 in encryption)
            self._log_step(f"6.{block_num}.4. Reverse Final Round",
                          f"Step 1: InvShiftRows - Reverse cyclical shift\n"
                          f"  • Row 0: No shift, Row 1: Right shift 1\n"
                          f"  • Row 2: Right shift 2, Row 3: Right shift 3\n"
                          f"Step 2: InvSubBytes - Apply inverse S-box\n"
                          f"  • Each byte replaced using inverse S-box\n"
                          f"  • Reverses the SubBytes from final encryption round\n"
                          f"⚠️ Note: No InvMixColumns (final round had no MixColumns)")
            
            # Reverse main rounds (13 down to 1)
            for round_num in range(13, 0, -1):
                self._log_step(f"6.{block_num}.{18-round_num}. Reverse Round {round_num}",
                              f"Step 1: AddRoundKey - XOR with round key\n"
                              f"  • State ⊕ RoundKey[{round_num}]\n"
                              f"Step 2: InvMixColumns - Inverse matrix multiplication\n"
                              f"  • Each column multiplied by inverse matrix in GF(2^8)\n"
                              f"  • Reverses the MixColumns transformation\n"
                              f"Step 3: InvShiftRows - Reverse cyclical shift\n"
                              f"  • Row 0: No shift, Row 1: Right shift 1\n"
                              f"  • Row 2: Right shift 2, Row 3: Right shift 3\n"
                              f"Step 4: InvSubBytes - Apply inverse S-box\n"
                              f"  • Each byte replaced using inverse S-box\n"
                              f"  • Reverses the SubBytes transformation")
            
            # Final decryption step - remove initial round key
            self._log_step(f"6.{block_num}.17. Final Decryption Step",
                          f"Operation: AddRoundKey (Round 0 key)\n"
                          f"State ⊕ RoundKey[0] (original key)\n"
                          f"Remove initial encryption round key\n"
                          f"Original plaintext block recovered")
    
    def _detailed_block_processing(self, padded_data, cipher, is_encryption=True):
        """
        Process blocks with detailed step-by-step logging
        """
        if self.mode in ['ECB', 'CBC']:
            num_blocks = len(padded_data) // AES.block_size
            result_blocks = []
            
            for i in range(num_blocks):
                block_start = i * AES.block_size
                block_end = block_start + AES.block_size
                input_block = padded_data[block_start:block_end]
                
                # Log block start
                self._log_step(f"6.{i+1}. Block {i+1} Processing Start",
                              f"Block {i+1} of {num_blocks}\n"
                              f"Input: {self._bytes_to_hex(input_block)}\n"
                              f"Size: {len(input_block)} bytes (128 bits)\n"
                              f"Mode: {self.mode}")
                
                # Add mode-specific preprocessing
                if self.mode == 'CBC' and is_encryption:
                    if i == 0:
                        # First block XOR with IV
                        self._log_step(f"6.{i+1}.0. CBC Preprocessing",
                                      f"First block XOR with IV\n"
                                      f"Block: {self._bytes_to_hex(input_block)}\n"
                                      f"IV: {self._bytes_to_hex(self.iv)}\n"
                                      f"Block ⊕ IV for encryption input")
                    else:
                        self._log_step(f"6.{i+1}.0. CBC Preprocessing",
                                      f"Block {i+1} XOR with previous ciphertext\n"
                                      f"Current block: {self._bytes_to_hex(input_block)}\n"
                                      f"Previous ciphertext block used for chaining")
                
                # Simulate detailed AES rounds
                self._simulate_aes_rounds(input_block, i+1, is_encryption)
                
                # Process the actual block (for ECB mode we can do individual blocks)
                if self.mode == 'ECB':
                    # ECB allows individual block processing
                    output_block = cipher.encrypt(input_block) if is_encryption else cipher.decrypt(input_block)
                else:
                    # For CBC, we'll simulate the output (actual processing happens later)
                    # This is for educational visualization only
                    output_block = input_block  # Will be replaced with actual result later
                
                # Log block completion with correct output
                self._log_step(f"6.{i+1}.18. Block {i+1} Processing Complete",
                              f"Input block: {self._bytes_to_hex(input_block)}\n"
                              f"After AES transformation: [Processed through 14 rounds]\n"
                              f"Output block: {self._bytes_to_hex(output_block)}\n"
                              f"Block {i+1} processing finished\n"
                              f"{'✅ Real transformation applied' if self.mode == 'ECB' else '📝 Educational simulation (actual processing in next step)'}")
                
                result_blocks.append(output_block)
            
            return b''.join(result_blocks)
        else:
            # Stream modes - different processing
            self._log_step("6. Stream Mode Processing",
                          f"Mode: {self.mode} (Stream cipher)\n"
                          f"Input length: {len(padded_data)} bytes\n"
                          f"Processing as continuous stream\n"
                          f"Keystream generation and XOR operation")
            
            return padded_data  # Placeholder
    
    def encrypt(self, plaintext):
        """
        Encrypt plaintext using AES-256
        
        Args:
            plaintext (str): Text to encrypt
            
        Returns:
            str: Base64 encoded ciphertext
        """
        self.steps = []  # Reset steps
        
        # Step 1: Convert plaintext to bytes
        plaintext_bytes = plaintext.encode('utf-8')
        self._log_step("1. Input Preparation", 
                      f"Plaintext: {plaintext}\n"
                      f"Plaintext bytes: {self._bytes_to_hex(plaintext_bytes)}\n"
                      f"Length: {len(plaintext_bytes)} bytes")
        
        # Step 2: Key preparation
        self._log_step("2. Key Preparation",
                      f"Key: {self.key.decode('utf-8', errors='ignore')}\n"
                      f"Key bytes: {self._bytes_to_hex(self.key)}\n"
                      f"Key length: {len(self.key)} bytes (256-bit)")
        
        # Step 3: Input validation and processing (minimum 16 bytes required)
        if len(plaintext_bytes) < 16:
            raise ValueError(f"Input must be at least 16 bytes. Got {len(plaintext_bytes)} bytes.")
        
        if self.mode in ['ECB', 'CBC']:
            # Apply PKCS7 padding for block modes
            block_size = AES.block_size
            padding_length = block_size - (len(plaintext_bytes) % block_size)
            if padding_length == block_size:
                padding_length = 0  # No padding needed if already multiple of block size
            
            if padding_length > 0:
                padding = bytes([padding_length] * padding_length)
                padded_data = plaintext_bytes + padding
                self._log_step("3. Block Mode Processing with Padding",
                              f"Input length: {len(plaintext_bytes)} bytes\n"
                              f"Block size: {block_size} bytes\n"
                              f"Original data: {self._bytes_to_hex(plaintext_bytes)}\n"
                              f"Padding needed: {padding_length} bytes\n"
                              f"Padding bytes: {self._bytes_to_hex(padding)}\n"
                              f"Padded data: {self._bytes_to_hex(padded_data)}\n"
                              f"Final length: {len(padded_data)} bytes\n"
                              f"Mode: {self.mode} - block cipher with PKCS7 padding")
            else:
                padded_data = plaintext_bytes
                self._log_step("3. Block Mode Processing",
                              f"Input length: {len(plaintext_bytes)} bytes (perfect block alignment)\n"
                              f"Block size: {block_size} bytes\n"
                              f"Data: {self._bytes_to_hex(plaintext_bytes)}\n"
                              f"No padding required - already multiple of block size\n"
                              f"Mode: {self.mode} - block cipher without padding")
        else:
            # Stream modes don't need padding
            padded_data = plaintext_bytes
            self._log_step("3. Stream Mode Processing",
                          f"Input length: {len(plaintext_bytes)} bytes\n"
                          f"Data: {self._bytes_to_hex(plaintext_bytes)}\n"
                          f"Mode: {self.mode} is a stream cipher - processes exact input length")
        
        # Step 4: Mode-specific setup
        if self.mode == 'ECB':
            cipher = AES.new(self.key, AES.MODE_ECB)
            self._log_step("4. ECB Mode Setup",
                          f"Mode: Electronic Codebook (ECB)\n"
                          f"No IV required\n"
                          f"Each block encrypted independently\n"
                          f"⚠️ Less secure - identical blocks produce identical ciphertext")
        elif self.mode == 'CBC':
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            self._log_step("4. CBC Mode Setup",
                          f"Mode: Cipher Block Chaining (CBC)\n"
                          f"IV: {self._bytes_to_hex(self.iv)}\n"
                          f"IV length: {len(self.iv)} bytes\n"
                          f"Each block XORed with previous ciphertext block")
        elif self.mode == 'CFB':
            cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
            self._log_step("4. CFB Mode Setup",
                          f"Mode: Cipher Feedback (CFB)\n"
                          f"IV: {self._bytes_to_hex(self.iv)}\n"
                          f"IV length: {len(self.iv)} bytes\n"
                          f"Stream cipher mode - no padding required\n"
                          f"Plaintext XORed with encrypted IV/previous ciphertext")
        elif self.mode == 'OFB':
            cipher = AES.new(self.key, AES.MODE_OFB, self.iv)
            self._log_step("4. OFB Mode Setup",
                          f"Mode: Output Feedback (OFB)\n"
                          f"IV: {self._bytes_to_hex(self.iv)}\n"
                          f"IV length: {len(self.iv)} bytes\n"
                          f"Stream cipher mode - no padding required\n"
                          f"Plaintext XORed with encrypted keystream")
        elif self.mode == 'CTR':
            cipher = AES.new(self.key, AES.MODE_CTR, nonce=self.iv)
            self._log_step("4. CTR Mode Setup",
                          f"Mode: Counter (CTR)\n"
                          f"Nonce: {self._bytes_to_hex(self.iv)}\n"
                          f"Nonce length: {len(self.iv)} bytes\n"
                          f"Stream cipher mode - no padding required\n"
                          f"Plaintext XORed with encrypted counter values")
        else:
            # This should never happen due to validation in __init__, but added for safety
            raise ValueError(f"Unsupported mode: {self.mode}")
        
        # Step 5: Data processing info
        if self.mode in ['ECB', 'CBC']:
            num_blocks = len(padded_data) // AES.block_size
            self._log_step("5. Block Division",
                          f"Total data length: {len(padded_data)} bytes\n"
                          f"Block size: {AES.block_size} bytes\n"
                          f"Number of blocks: {num_blocks}\n"
                          f"Mode: {self.mode} processes data in {AES.block_size}-byte blocks")
        else:
            self._log_step("5. Stream Processing",
                          f"Data length: {len(padded_data)} bytes\n"
                          f"Mode: {self.mode} processes data as a continuous stream\n"
                          f"No block division required")
        
        # Step 6: Detailed Encryption Process
        if self.mode in ['ECB', 'CBC']:
            # Use detailed block processing for educational purposes
            self._detailed_block_processing(padded_data, cipher, is_encryption=True)
        else:
            # Stream cipher modes
            self._log_step("6. Stream Encryption Process",
                          f"Mode: {self.mode} (Stream cipher)\n"
                          f"Input data: {self._bytes_to_hex(padded_data)}\n"
                          f"Process: Keystream generation and XOR\n"
                          f"Length: {len(padded_data)} bytes")
        
        # Perform actual encryption
        ciphertext = cipher.encrypt(padded_data)
        
        # Log final encryption results
        if self.mode in ['ECB', 'CBC']:
            num_blocks = len(padded_data) // AES.block_size
            for i in range(num_blocks):
                block_start = i * AES.block_size
                block_end = block_start + AES.block_size
                input_block = padded_data[block_start:block_end]
                output_block = ciphertext[block_start:block_end]
                
                comparison = self._compare_blocks(input_block, output_block, "encryption")
                self._log_step(f"6.{i+1}.19. Block {i+1} Final Result",
                              f"📥 Original input: {self._bytes_to_hex(input_block)}\n"
                              f"📤 Final ciphertext: {self._bytes_to_hex(output_block)}\n"
                              f"📊 Input matrix:\n{self._format_state(input_block)}\n"
                              f"📊 Output matrix:\n{self._format_state(output_block)}\n"
                              f"{comparison}")
        else:
            # Stream cipher final result
            self._log_step("6.1. Stream Encryption Complete",
                          f"Input data: {self._bytes_to_hex(padded_data)}\n"
                          f"Final ciphertext: {self._bytes_to_hex(ciphertext)}\n"
                          f"Stream encryption successful\n"
                          f"Length: {len(ciphertext)} bytes (same as input)")
        
        # Step 7: Final result
        if self.mode in ['CBC', 'CFB', 'OFB', 'CTR']:
            # Prepend IV/nonce to ciphertext for modes that need it
            final_result = self.iv + ciphertext
            iv_label = "Nonce" if self.mode == 'CTR' else "IV"
        else:
            final_result = ciphertext
            iv_label = ""
            
        result_b64 = base64.b64encode(final_result).decode('utf-8')
        
        if self.mode == 'ECB':
            result_description = "Ciphertext only (no IV needed)"
        else:
            result_description = f"{iv_label} + Ciphertext"
        
        self._log_step("7. Final Output",
                      f"Raw ciphertext: {self._bytes_to_hex(ciphertext)}\n"
                      f"Final result: {result_description}\n"
                      f"Combined data: {self._bytes_to_hex(final_result)}\n"
                      f"Base64 encoded: {result_b64}")
        
        return result_b64
    
    def decrypt(self, ciphertext_b64):
        """
        Decrypt base64 encoded ciphertext
        
        Args:
            ciphertext_b64 (str): Base64 encoded ciphertext
            
        Returns:
            str: Decrypted plaintext
        """
        self.steps = []  # Reset steps
        
        try:
            # Step 1: Decode base64
            try:
                ciphertext_data = base64.b64decode(ciphertext_b64)
            except Exception as e:
                raise ValueError(f"Invalid Base64 input: {str(e)}")
                
            self._log_step("1. Input Preparation",
                          f"Base64 input: {ciphertext_b64}\n"
                          f"Decoded bytes: {self._bytes_to_hex(ciphertext_data)}\n"
                          f"Length: {len(ciphertext_data)} bytes")
            
            # Validate minimum length
            if len(ciphertext_data) == 0:
                raise ValueError("Empty ciphertext data")
            
            # Step 2: Extract IV/nonce and ciphertext based on mode
            if self.mode == 'ECB':
                iv = None
                ciphertext = ciphertext_data
                self._log_step("2. ECB Mode Setup",
                              f"Mode: Electronic Codebook (ECB)\n"
                              f"Ciphertext: {self._bytes_to_hex(ciphertext)}\n"
                              f"Length: {len(ciphertext)} bytes\n"
                              f"No IV required")
            else:
                # All other modes require IV/nonce extraction
                if len(ciphertext_data) < 17:  # At least 16 bytes IV + 1 byte data
                    raise ValueError(f"Invalid ciphertext length for {self.mode} mode: {len(ciphertext_data)} bytes (minimum 17 required)")
                iv = ciphertext_data[:16]
                ciphertext = ciphertext_data[16:]
                iv_label = "Nonce" if self.mode == 'CTR' else "IV"
                self._log_step(f"2. {self.mode} {iv_label} Extraction",
                              f"Mode: {self.mode}\n"
                              f"{iv_label}: {self._bytes_to_hex(iv)}\n"
                              f"Ciphertext: {self._bytes_to_hex(ciphertext)}\n"
                              f"Ciphertext length: {len(ciphertext)} bytes")
            
            # Validate block alignment (only for block modes)
            if self.mode in ['ECB', 'CBC']:
                if len(ciphertext) % AES.block_size != 0:
                    raise ValueError(f"Ciphertext length ({len(ciphertext)} bytes) is not aligned to block boundary ({AES.block_size} bytes)")
            
            if len(ciphertext) == 0:
                raise ValueError("No ciphertext data to decrypt")
            
            # Step 3: Key preparation
            self._log_step("3. Key Preparation",
                          f"Key: {self.key.decode('utf-8', errors='ignore')}\n"
                          f"Key bytes: {self._bytes_to_hex(self.key)}\n"
                          f"Key length: {len(self.key)} bytes (256-bit)")
            
            # Step 4: Cipher setup
            if self.mode == 'ECB':
                cipher = AES.new(self.key, AES.MODE_ECB)
            elif self.mode == 'CBC':
                cipher = AES.new(self.key, AES.MODE_CBC, iv)
            elif self.mode == 'CFB':
                cipher = AES.new(self.key, AES.MODE_CFB, iv)
            elif self.mode == 'OFB':
                cipher = AES.new(self.key, AES.MODE_OFB, iv)
            elif self.mode == 'CTR':
                cipher = AES.new(self.key, AES.MODE_CTR, nonce=iv)
            else:
                # This should never happen due to validation in __init__, but added for safety
                raise ValueError(f"Unsupported mode: {self.mode}")
            
            # Step 5: Processing info based on mode
            if self.mode in ['ECB', 'CBC']:
                num_blocks = len(ciphertext) // AES.block_size
                self._log_step("4. Block Analysis",
                              f"Ciphertext length: {len(ciphertext)} bytes\n"
                              f"Block size: {AES.block_size} bytes\n"
                              f"Number of blocks: {num_blocks}\n"
                              f"Mode: {self.mode} processes data in blocks")
                
                # Step 5: Detailed Block-by-block decryption
                self._detailed_block_processing(ciphertext, cipher, is_encryption=False)
            else:
                self._log_step("4. Stream Analysis",
                              f"Ciphertext length: {len(ciphertext)} bytes\n"
                              f"Mode: {self.mode} processes data as stream\n"
                              f"No block division required")
            
            # Perform actual decryption
            decrypted_data = cipher.decrypt(ciphertext)
            
            # Log final decryption results
            if self.mode in ['ECB', 'CBC']:
                num_blocks = len(ciphertext) // AES.block_size
                for i in range(num_blocks):
                    block_start = i * AES.block_size
                    block_end = block_start + AES.block_size
                    input_block = ciphertext[block_start:block_end]
                    output_block = decrypted_data[block_start:block_end]
                    
                    comparison = self._compare_blocks(input_block, output_block, "decryption")
                    self._log_step(f"5.{i+1}.19. Block {i+1} Decryption Result",
                                  f"📥 Ciphertext input: {self._bytes_to_hex(input_block)}\n"
                                  f"📤 Decrypted output: {self._bytes_to_hex(output_block)}\n"
                                  f"📊 Input matrix:\n{self._format_state(input_block)}\n"
                                  f"📊 Output matrix:\n{self._format_state(output_block)}\n"
                                  f"{comparison}")
                
                self._log_step("6. All Blocks Decrypted",
                              f"Total decrypted data: {self._bytes_to_hex(decrypted_data)}\n"
                              f"Length: {len(decrypted_data)} bytes\n"
                              f"All {num_blocks} blocks processed successfully")
            else:
                self._log_step("5. Stream Decryption Complete",
                              f"Ciphertext input: {self._bytes_to_hex(ciphertext)}\n"
                              f"Decrypted stream: {self._bytes_to_hex(decrypted_data)}\n"
                              f"Stream decryption successful\n"
                              f"Length: {len(decrypted_data)} bytes (same as input)")
            
            # Step 7: Final processing with padding removal for block modes
            if self.mode in ['ECB', 'CBC']:
                # Remove PKCS7 padding
                try:
                    # Check if padding exists
                    if len(decrypted_data) > 0:
                        padding_length = decrypted_data[-1]
                        if padding_length > 0 and padding_length <= AES.block_size:
                            # Verify padding is valid PKCS7
                            padding_bytes = decrypted_data[-padding_length:]
                            if all(b == padding_length for b in padding_bytes):
                                # Valid padding found, remove it
                                plaintext_bytes = decrypted_data[:-padding_length]
                                self._log_step("7. Block Mode Final Processing with Padding Removal",
                                              f"Decrypted data: {self._bytes_to_hex(decrypted_data)}\n"
                                              f"Padding detected: {padding_length} bytes\n"
                                              f"Padding bytes: {self._bytes_to_hex(padding_bytes)}\n"
                                              f"Final data after padding removal: {self._bytes_to_hex(plaintext_bytes)}\n"
                                              f"Final length: {len(plaintext_bytes)} bytes")
                            else:
                                # Invalid padding, keep original data
                                plaintext_bytes = decrypted_data
                                self._log_step("7. Block Mode Final Processing",
                                              f"Decrypted data: {self._bytes_to_hex(plaintext_bytes)}\n"
                                              f"No valid PKCS7 padding found\n"
                                              f"Length: {len(plaintext_bytes)} bytes")
                        else:
                            # No padding or invalid padding length
                            plaintext_bytes = decrypted_data
                            self._log_step("7. Block Mode Final Processing",
                                          f"Decrypted data: {self._bytes_to_hex(plaintext_bytes)}\n"
                                          f"No padding to remove\n"
                                          f"Length: {len(plaintext_bytes)} bytes")
                    else:
                        plaintext_bytes = decrypted_data
                except Exception:
                    # If padding removal fails, keep original data
                    plaintext_bytes = decrypted_data
                    self._log_step("7. Block Mode Final Processing",
                                  f"Decrypted data: {self._bytes_to_hex(plaintext_bytes)}\n"
                                  f"Padding removal failed, keeping original data\n"
                                  f"Length: {len(plaintext_bytes)} bytes")
            else:
                plaintext_bytes = decrypted_data
                self._log_step("6. Stream Mode Final Processing",
                              f"Stream cipher mode - no padding to remove\n"
                              f"Final data: {self._bytes_to_hex(plaintext_bytes)}\n"
                              f"Length: {len(plaintext_bytes)} bytes")
            
            # Convert to string
            try:
                plaintext = plaintext_bytes.decode('utf-8')
            except UnicodeDecodeError as e:
                raise ValueError(f"Cannot decode decrypted data as UTF-8: {str(e)}. This might indicate wrong key.")
            
            final_step = "8" if self.mode in ['ECB', 'CBC'] else "7"
            self._log_step(f"{final_step}. Final Result",
                          f"Plaintext: {plaintext}\n"
                          f"Length: {len(plaintext)} characters\n"
                          f"Decryption successful")
            
            return plaintext
            
        except Exception as e:
            error_msg = f"Decryption failed: {str(e)}"
            self._log_step("Error", error_msg)
            raise ValueError(error_msg)
    
    def get_steps(self):
        """Return the logged steps"""
        return self.steps