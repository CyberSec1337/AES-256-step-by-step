# xmind_exporter.py
import xmind
import os

def export_to_xmind(steps, output_path):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Create new workbook
        if os.path.exists(output_path):
            workbook = xmind.load(output_path)
        else:
            # Create a new workbook
            workbook = xmind.load(output_path)
        
        sheet = workbook.getPrimarySheet()
        if sheet is None:
            # If no primary sheet exists, create one
            sheet = workbook.createSheet()
            sheet.setTitle("AES-256 Process")
        else:
            sheet.setTitle("AES-256 Process")
        
        # Get the root topic
        root_topic = sheet.getRootTopic()
        if root_topic is None:
            from xmind.core.topic import TopicElement
            root_topic = TopicElement(ownerWorkbook=workbook)
            sheet.rootTopic = root_topic
        root_topic.setTitle("AES-256 Encryption/Decryption Steps")
        
        # Add steps as subtopics
        for step in steps:
            subtopic = root_topic.addSubTopic()
            subtopic.setTitle(step["step"])
            subtopic.setPlainNotes(step["detail"])
        
        # Save the workbook
        xmind.save(workbook, output_path)
        print(f"XMind file saved successfully to {output_path}")
            
    except Exception as e:
        # Fallback: create a simple text-based mind map file
        print(f"XMind export failed: {e}")
        create_text_mindmap(steps, output_path.replace('.xmind', '.txt'))

def create_text_mindmap(steps, output_path):
    """Create a simple text-based representation of the mind map"""
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("AES-256 Encryption/Decryption Steps\n")
            f.write("=" * 40 + "\n\n")
            
            for i, step in enumerate(steps, 1):
                f.write(f"{i}. {step['step']}\n")
                f.write("-" * len(f"{i}. {step['step']}") + "\n")
                f.write(f"{step['detail']}\n\n")
        print(f"Text mindmap saved to {output_path}")
    except Exception as e:
        print(f"Failed to create text mindmap: {e}")
